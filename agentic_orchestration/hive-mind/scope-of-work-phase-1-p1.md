# Phase-1 P1 Scope of Work — Hive Mode

**Authored:** 2026-05-17 by knight-rider at hive activation.
**Authority:** Matt directive 2026-05-17 (full-overhaul); gandalf invocation request `agentic_orchestration/gandalf/requests/2026-05-17-knight-rider-phase-1-p1-full-overhaul-coordination.md`; operating under `canonical/story/hive-mind-protocol-2026-05-17.md`.
**Status:** **Live executable plan.** Updated continuously by knight-rider as work advances. All seams consult this doc; specialists execute against it without per-task dispatch authorization.
**Estimated duration:** 8–12 weeks (gandalf authorship) — knight-rider re-scopes after seam-specific assessments land in Week 1.
**Companion artifacts:** `coordination-matrix.md` (per-deliverable seam mapping); `phase-1-p1-log.md` (append-only hive log); `state-of-hive-YYYY-MM-DD.md` (daily digests).

---

## § 0 — TL;DR

The hive rebuilds the engine's foundation to make canonical-7 substrate expansion (fire/water/earth/wind + lightning + holy + shadow) *and* the five-layer diversity architecture (Layers 1–4 minimum) shippable in a single concentrated push, in service of demo1 VS2a, **before** VS2a ships. Layer 5 telemetry feedback deferred to Phase-2. Poison/acid substrate deferred to Phase-1 P2.

27 deliverables across 4 engineering seams + jack-ryan continuous-observation + gandalf design-companion. Standard mode (dispatch-sequenced) suspended for the duration. Distributed authority: in-seam decisions are L1 (specialist); cross-seam are L2 (knight-rider harmonizes); architectural/canonical revisions are L3 (Matt).

**Ship gate:** Phase-1 P1 ships when the canonical-7 substrate set is mechanically active in generation+simulation+LLM-prompt surfaces, the Court of Forms vessel persists across seasons with Spirit-Guide voice integration, the wide-net registries (roles + ailments + grouping-vocab + LLM prompt structure) are config-driven not hardcoded, and the perception-test result (Phase-1 P1a) has grounded Layer-3 metric design. Tag `v1.0-phase-1-p1` at ship.

---

## § 1 — The 27 deliverables (expanded)

Cross-references throughout this section: invocation § 2 numbering preserved; canonical-doc authority cited per deliverable; effort estimates are knight-rider's first-pass intuition pending seam-specific assessment (Week-1 task).

### § 1.1 — Architectural foundation (deliverables 1–6)

**Deliverable 1 — Substrate identity loader implementation.**
- Owner: **rocket** (foundation seam ownership).
- Inputs: `substrate-identity-declaration-spec-2026-05-17.md` (Layer-1 spec); `substrate-identity-declarations-2026-05-17.md` (7 declarations).
- Outputs: `reincarnated-engine/config/substrate_identities/<substrate>.yaml` (7 files extracted from canonical declarations); `src/reincarnated/foundation/substrate_identity_loader.py` (new module with `SubstrateIdentity` dataclass + `load_substrate_identities()` + boot-time validation per spec § 5.3); `foundation.get_rotating_elements()` integration so `Element.identity: SubstrateIdentity` is populated.
- Math-before-code (Discipline #1): not load-bearing math; design-then-build pattern applies (rocket reads spec § 5; authors implementation; jack-ryan reviews against spec).
- Effort estimate: ~3–5 days (loader + YAML extraction + validation + tests + foundation integration).
- Unblocks: all other Layer-1-dependent deliverables (2, 3, 4, 5, 6, 17).
- Pattern P7 risk: spec § 5.3 explicitly mandates fail-loud validation — no default substrates, no silent fallback on missing fields. Jack-ryan watches.

**Deliverable 2 — Substrate expansion canonical-four → canonical-7 (engine refactor).**
- Owner: **rocket + gamora** (joint; rocket leads structural changes, gamora leads simulation-side consumption).
- Inputs: Deliverable 1; `substrate-coupling-archaeology-2026-05-17.md` (13 substrate-keyed coupling sites).
- Outputs (refactor of each coupling site per archaeology § 2):
  - Coupling #1 (`element/schema.py`): `SeasonalElements` 4-slot Pydantic → `slots: dict[str, SlotSelection]` keyed by canonical name. **rocket.**
  - Coupling #2 (`element/selector.py:34`): `VALID_SLOTS` computed from `foundation.get_rotating_elements()`. **rocket.**
  - Coupling #3 (`generation/b6_archetype_templates.py:22-35`): `ELEMENT_AFFINITY` + `HYBRID_FORBIDDEN_PAIRS` loaded from config; forbidden pairs computed from pair-structure. **rocket.** *(NOTE: subsumed by Path-a refactor in deliverable 3.)*
  - Coupling #4 (`generation/monster_generator.py:234-241`): iterate foundation registry. **rocket.**
  - Coupling #5 (`generation/trial_generator.py:112-116`): iterate foundation registry. **rocket.**
  - Coupling #6 (`generation/b6_kit_builder.py:191,201`): initialize from foundation registry. **rocket.** *(Subsumed by Path-a; deliverable 3.)*
  - Coupling #7 (`simulation/balance_loop.py:233-267,415-425`): pass foundation registry to balance-loop context. **gamora.**
  - Coupling #8 (`llm/naming.py:32,37-42`): **CRITICAL CONVERGENCE SITE.** Load `_CANONICAL_TO_GROUPING` from grouping-vocab; assert non-fallback (no `impact-mode-{element}` silent default). **star-lord.** *(Lives in LLM prompt structure refactor — deliverable 6.)*
  - Coupling #9 (`telemetry/recorder.py:123,713`): iterate foundation registry; dict-keyed lookup post-Coupling-#1 fix. **star-lord.**
  - Coupling #10 (`generation/season_orchestrator.py:317,522,537,564`): GOOD PATTERN ✅ — no work; reference. **rocket.**
  - Coupling #11 (`generation/gear_catalog.py:117`): GOOD PATTERN ✅. **rocket.**
  - Coupling #13 (`llm/cosmological_vocabulary.py:63-75`): pair-structure refactor. **star-lord.** *(Lives in deliverable 6.)*
- Effort estimate: ~5–8 days across rocket + gamora (mostly refactor of well-located sites; jack-ryan reviews for completeness against archaeology).
- Unblocks: Deliverable 7 (resistance matrix), 8 (trait floor), 10 (substrate-coherent generation), 17 (Court vessel).

**Deliverable 3 — Path-a archetype-template combinatorial refactor.**
- Owner: **gamora** (composition-layer authority).
- Inputs: Deliverable 1; `archetype-coupling-archaeology-2026-05-17.md` (10 archetype-keyed coupling sites).
- Outputs: Replace 14 hardcoded `ArchetypeTemplate` entries in `generation/b6_archetype_templates.py` with on-boot composition from `SUBSTRATE_IDENTITY × ROLE_SHAPES`. Specifically:
  - Define `ROLE_SHAPES` registry (5 role shapes: damage / support / control / hybrid + physical-melee; see role registry deliverable 4 for canonical role enumeration).
  - Author composition function `compose_archetype_template(substrate, role) -> ArchetypeTemplate` reading substrate's `mechanical_signature`, `forbidden_mechanics`, `geometry_affinities`, `role_affinities`, `scaling_attribute`, `ailment_signature` × role's stat emphasis + action register + constraint tags.
  - Refactor Coupling #2 (archetype_classifier dispatch) — eliminate string-literal cases.
  - Refactor Coupling #3 (stat_allocator) — replace 16 hardcoded stat profiles with composition.
  - Refactor Coupling #4 (action/role-function registers) — replace per-archetype dispatch with substrate × role.
  - Refactor Coupling #5 (element_biases) — `ELEMENT_SCALING_ATTRIBUTE`/`ELEMENT_AILMENT`/`AILMENT_IS_CONTROL` read from substrate declarations (no hardcoding).
  - Refactor Coupling #6 (per-archetype geometry bias) — composition multiplies substrate `geometry_affinities` × role's geometry preferences. **Closes "silent-neutralization vector."**
  - Refactor Coupling #7 (constraint checker registry) — **FAIL-LOUD** on unknown constraint tags (eliminates "silent-skip" Pattern P7 instance).
  - Refactor Coupling #8 (monster archetype pool) — preserve independent monster archetype set; gate by substrate-set.
  - Refactor Coupling #9 (earth_caster B11 deferred constraint) — re-evaluate post-composition.
  - Coupling #12 left for last; LOW-severity; revisit only if cleanup pressure remains.
- Math-before-code (Discipline #1): authored math note required for the composition function semantics — what does "substrate × role = template" *mean* mathematically, and how do `geometry_affinities` weights compose with role's geometry preferences (multiplicative? max? rank-vote?). gamora authors before code; jack-ryan reviews.
- Effort estimate: ~2 weeks (largest refactor in Phase-1 P1; touches generation core).
- Unblocks: Deliverables 7, 8, 9, 10, 11, 14, 15.

**Deliverable 4 — Role registry refactor (wide-net § 2.1).**
- Owner: **rocket** (registry-authoring) + **gamora** (consumer-side).
- Inputs: `wide-net-coupling-archaeology-2026-05-17.md` § 2.1.
- Outputs: `reincarnated-engine/config/roles.yaml` canonical roles registry with per-role metadata (stat emphasis, ai-strategy priority, constraint-tag affinities). Refactor 5+ consumer files (`role_constraints.py`, `class_generator.py`, `monster_generator.py`, `simulation/ai_strategies.py`, `generation/ability_grammar.py`) to iterate registry. Closes silent-convergence risk (new roles fail at lookup; AI strategies silently omit). **rocket** authors registry + schema; **gamora** refactors AI strategy consumer.
- Math-before-code: not applicable.
- Effort estimate: ~3–5 days (rocket: 2 days registry + tests; gamora: 1–2 days AI strategy refactor).
- Unblocks: Deliverable 3 (composition references registered roles).

**Deliverable 5 — Ailment registry refactor (wide-net § 2.2).**
- Owner: **rocket** (registry-authoring) + **gamora** (control-classification consumer).
- Inputs: `wide-net-coupling-archaeology-2026-05-17.md` § 2.2; substrate identity declarations (new ailments: `shock` / `consecrate` / `drain`).
- Outputs: `reincarnated-engine/config/ailments.yaml` per-ailment registry with `is_control: hard|soft|none` + `param_ranges` + `ai_priority` metadata. Refactor `element_biases.py`, `foundation/effect_categorization.py`, `generation/ability_grammar.py` to read registry. Substrate identity declarations reference registry by name (per spec § 3.1). New ailments (shock/consecrate/drain) land at registry-extension time, not source-edit time.
- Math-before-code: not applicable.
- Effort estimate: ~3–4 days.
- Unblocks: Deliverable 3 (composition refers to registered ailments).

**Deliverable 6 — LLM prompt structure refactor (wide-net § 2.3 CRITICAL SURPRISE).**
- Owner: **star-lord** (LLM seam ownership).
- Inputs: `wide-net-coupling-archaeology-2026-05-17.md` § 2.3; `grouping-layer-vocabulary.md` (pending extension per deliverable 20); pair-structure decisions from substrate-expansion-decision § 3.2 (holy ↔ shadow paired; lightning unpaired).
- Outputs: Refactor `src/reincarnated/llm/cosmological_vocabulary.py` to read pair-structure shape from machine-extractable section of `grouping-layer-vocabulary.md`. Replace hardcoded 2-2-1 pair-structure (`GROUPING_SLOTS` tuple, `_PRIMARY_PAIR`, `_SECONDARY_PAIR`, `_FOUNDATION_SLOT`) with registry-driven generation that handles arbitrary pair-shape (per-substrate paired? unpaired? axis-keyed?). Refactor Coupling #8 (`llm/naming.py`) to fail-loud on missing substrate; assert non-fallback. Stage-3 cipher migration's grouping-label consumption integrates with the registry-driven path.
- Math-before-code: not applicable.
- Effort estimate: **~1–2 weeks (HIGHEST UNKNOWN; gandalf invocation § 7 risk #1).** star-lord begins with a refactor plan + scoping doc before implementation; knight-rider tracks scope-vs-estimate.
- Unblocks: Deliverable 15 (Layer-4 LLM flavor consumes registry-driven prompts).
- Risk: refactor scope may grow once star-lord examines the code; surface in hive log within 3 days of starting if estimate revises.

### § 1.2 — Engine substrate-coupling work (deliverables 7–11)

**Deliverable 7 — Resistance matrix 4×4 → 7×7 with paired-luminance valence.**
- Owner: **gamora** (sim authority).
- Inputs: Deliverable 1 (substrate identity); substrate-expansion-decision § 5.1 (extension shape).
- Outputs: 7×7 resistance matrix with: canonical-four symmetric (unchanged); lightning unpaired (no amplification/reduction; behaves like canonical-four for resistance); holy ↔ shadow valenced paired axis (+25% damage opposed-luminance; −25% damage same-luminance — default magnitudes per design doc § 5.1). Engine consumers (`balance_loop.py` damage-resolution) consume.
- **Math-before-code (Discipline #1) — LOAD-BEARING.** gamora authors numeric 7×7 matrix + worked DPS-against-each-substrate analysis at L1 / L25 / L50 confirming no class becomes structurally over- or under-powered relative to canonical-four baseline. Authored as `simulation/math/resistance-matrix-7x7-phase-1-p1.md` BEFORE code lands. jack-ryan Gate-1-equivalent (continuous-observation) reviews math.
- Effort estimate: ~5–7 days (math note 2–3 days; implementation 1–2 days; tests + DPS validation 2 days).
- Unblocks: Deliverable 8, 9, 10.

**Deliverable 8 — Trait-floor extension to 3 new classes (lightning, holy, shadow).**
- Owner: **gandalf** (design authority for trait identity) + **gamora** (implementation).
- Inputs: substrate-expansion-decision § 5.2; substrate identity declarations (lightning iconic_verbs/mechanical_signature → chain/arc/discharge anchors; holy → radiance/consecration/cleanse; shadow → concealment/corruption/drain).
- Outputs: 3 new per-class intrinsic trait pools (5–10 traits each; floors at L1/12/25/38; converge at L50 per `project_trait_architecture`). gandalf authors substrate-coherent trait designs (Pattern B); gamora implements. Substrate identity declarations' `mechanical_signature` + `forbidden_mechanics` constrain trait authoring (no shadow-substrate trait that violates `forbidden_mechanics`).
- Math-before-code: trait magnitudes consume B-loop math; reuse existing trait architecture per file 32.
- Effort estimate: ~5–7 days (gandalf authoring 2 days; gamora implementation + tests 3–5 days).
- Unblocks: Deliverable 9 (gear-affix gating consumes trait architecture).

**Deliverable 9 — Gear-affix gating extension to 3 new substrates.**
- Owner: **gandalf** (design) + **gamora** (implementation).
- Inputs: substrate-expansion-decision § 5.3; deliverable 8.
- Outputs: Affix pool extended (~1.5× expansion since 6/4 = 1.5; operational sizing). Lightning-coherent affixes, holy-coherent affixes, shadow-coherent affixes authored (gandalf). Gating logic extended to include new substrates (gamora; `gear_generation.py` material naming + suffix tables grow). Cross-substrate affix coherence check — no canonical-four affix silently becomes substrate-incoherent (jack-ryan watches).
- Effort estimate: ~3–5 days.
- Unblocks: Deliverable 19 (VFX library extension; affix-trait coupling).

**Deliverable 10 — Substrate-coherent generation rules.**
- Owner: **gamora** (generation-rules consumer).
- Inputs: Deliverables 1, 2, 3, 7; substrate-expansion-decision § 5.4.
- Outputs: Per-season class rotation samples across 6 archetypal substrate classes (existing spirit-swap-differentiation rule extended to 7 substrates; player's current class substrate excluded from current-season Trial-boss pool — operational extension). Per-substrate generation-frequency balancing (math-before-code: gamora authors substrate-rotation frequency analysis; jack-ryan reviews against Discipline #13 — substrates should be representable not over-/under-frequent in seasons).
- Math-before-code (Discipline #1): per-substrate generation-frequency targets authored; empirical validation runs at full-regen scale.
- Effort estimate: ~5–7 days.
- Unblocks: Deliverable 14 (Layer-3 gate consumes generation output).

**Deliverable 11 — Pool D1 re-score under `substrate_native`.**
- Status: **✅ ALREADY SHIPPED** (rocket Drift-14 amendment; tag `rocket/v1.4-drift14-pool-cull-and-selector-amendment-1 @ 65e6d77`).
- No further work; reference for downstream consumers.

### § 1.3 — Diversity architecture (Layers 1–4) (deliverables 12–16)

**Deliverable 12 — Layer 1: substrate identity declarations operationalized.**
- Subsumed by Deliverable 1. Layer 1 = the YAML extraction + loader; substrate-identity-declaration-spec is the spec; declarations are the content.

**Deliverable 13 — Layer 2: identity-pruned composition.**
- Subsumed by Deliverable 3. Layer 2 = the Path-a archetype combinatorial refactor; the composition function reads Layer 1 declarations to constrain archetype generation per substrate × role.

**Deliverable 14 — Layer 3: mirror-match diversity gate.**
- Owner: **gamora** (sim-side gate implementation).
- Inputs: **Phase-1 P1a perception test result** (per deliverable 27 — this gates similarity-metric choice); substrate identity declarations (combat_pillar weights inform metric).
- Outputs: Diversity gate that measures similarity between archetypes and rejects candidates above threshold T. Metric shape determined by perception test result (mechanical-parameter vector distance if test passes; play-trace feature space if test fails). If play-trace metric needed: per-fight feature extraction spec authored first (gandalf authors; gamora implements).
- Math-before-code (Discipline #1): similarity metric authored with explicit formula + threshold-T sensitivity analysis BEFORE code lands.
- Effort estimate: ~1 week if mechanical-parameter metric; **~2-3 weeks if play-trace metric** (per perception-test scoping § 6.1 decision tree).
- **BLOCKED on Phase-1 P1a perception test result.** Parallel-startable in design-spec phase; implementation gated.

**Deliverable 15 — Layer 4: LLM flavor diversifier.**
- Owner: **star-lord** (LLM seam consumes; gandalf provides scaffold input).
- Inputs: Deliverable 6 (LLM prompt structure refactor); substrate identity declarations (iconic_verbs, iconic_register, cosmological_commitment, court_resonance as prompt-template inputs per spec § 6).
- Outputs: Layer-4 LLM flavor extension: prompt templates anchor on substrate's iconic_verbs (per Legolas Finding A — explicit iconic vocabulary anchors prevent LLM training-distribution bias toward fire-mage tropes when generating shadow-substrate prose). Court-aware referencing extension (per earth-self resolution § 6.2): LLM may reference player's accumulated Court at per-season moments. Iconic-vocabulary anchoring at prompt level. Stage-3 cipher migration integrates with Layer-4 (form-bias cadence Option II cosmological-vocabulary is the substrate-of-Layer-4).
- Effort estimate: ~1–2 weeks (depends heavily on deliverable 6 outcome).
- Unblocks: nothing else in Phase-1 P1 (Layer 5 is deferred).

**Deliverable 16 — Layer 5: telemetry feedback loop.**
- Status: **DEFERRED to Phase-2** (per substrate-expansion-decision § 6.5; needs play telemetry from shipped substrates).
- No Phase-1 P1 work. Holding open: the architecture's success-measurement layer (per § 6.5.4); worth defending against scope-cut pressure later.

### § 1.4 — Phase-0 cosmological vessel (deliverables 17–18)

**Deliverable 17 — Court of Forms vessel.**
- Owner: **rocket** (data structure persistence) + **drax** (browsable surface in loadout) + **star-lord** (Spirit Guide voice integration via LLM).
- Inputs: `earth-self-diversity-tension-2026-05-17.md` § 4 (Phase-0 deliverables); `court-of-forms.md`.
- Outputs:
  - **rocket:** Court of Forms data structure — serialize current form into Court at Ascension ritual fire (substrate-archetype identity + full skill list with iconic abilities + visual signature + name + season number + season cosmology + key moments). Persistence layer (engine-side; SQLite or JSON-file or per-Earth-Self DB).
  - **drax:** Loadout / Earth-Self hub browsable surface. Per `earth-self-diversity-tension` § 4.1: player can view accumulated forms; each entry shows form as it was at season-end.
  - **star-lord:** LLM prompt-template integration — Court-aware references in Spirit Guide voice (per § 6.2 of earth-self-doc; § 7 Spirit-Guide-as-Court-storyteller amendment).
- Effort estimate: ~5–7 days total across 3 seams; loose coupling allows parallel work.
- Unblocks: Deliverable 18 (Spirit-Guide voice amendment integration).

**Deliverable 18 — Spirit Guide voice amendment.**
- Owner: **gandalf** (canonical amendment authoring) + **star-lord** (LLM template integration).
- Inputs: `earth-self-diversity-tension-2026-05-17.md` § 7.
- Outputs: gandalf amends `canonical/story/spirit-guide-voice.md` adding Court-storyteller role per § 7. star-lord ensures LLM prompt template generates Court-aware voice lines without spoiler-leaking current-season narrative.
- Effort estimate: ~2–3 days.

### § 1.5 — Player-facing surface (deliverables 19–22)

**Deliverable 19 — VFX library extension for canonical-7.**
- Owner: **drax** (demo-side asset integration).
- Inputs: vendor acquisitions (CraftPix premium wood-nature [earth-substrate biological-organic rebuild]; Fellor Crystal [gem cluster reinforcement]; Frostwindz Deathbringer [bone → shadow substrate per CHANGELOG 2026-05-17]); pixogen library (already in place; lightning, void, holy assets per Pixogen Path-A); Pimen catalogue (lightning-spell-effect VFX is GREEN-list per legolas reverse-audit).
- Outputs: VFX library extended for lightning + holy + shadow assets. Demo-side wiring integrates new substrate VFX into combat rendering.
- **BLOCKED on Matt vendor acquisition decisions** (CraftPix premium + Fellor Crystal + Frostwindz authorized per CHANGELOG but payment/download not yet executed). Surface to Matt as L3 in activation broadcast.
- Effort estimate: ~5–7 days after assets land on disk.

**Deliverable 20 — Grouping-vocab extension (lightning/holy/shadow labels).**
- Owner: **gandalf** (canonical L2 vocabulary authoring).
- Inputs: substrate identity declarations (proposed labels: lightning → `resonance`; holy → `radiance`; shadow → `penumbra`).
- Outputs: `canonical/story/grouping-layer-vocabulary.md` extended with 3 new labels + per-label semantic note. **Sequencing critical:** must land **BEFORE** Deliverable 6 (LLM prompt structure refactor) begins implementation (star-lord's registry-driven prompt construction reads from this doc).
- Effort estimate: ~1 day (gandalf authoring).

**Deliverable 21 — Substrate-aware loadout substrate browser.**
- Owner: **drax** (loadout app).
- Inputs: substrate identity declarations (cosmological_commitment text surfaces in browser); Court of Forms vessel (deliverable 17).
- Outputs: Loadout app surface for substrate inspection (player can browse the 7 substrates; see commitments, mechanical signatures, iconic verbs); Court browsing surface (per deliverable 17 above).
- Effort estimate: ~5–7 days.

**Deliverable 22 — Embodiment-display substrate extension.**
- Owner: **drax** + **star-lord** (joint).
- Inputs: existing embodiment-axis work (form-bias Stage 1; rocket); VS2b plans extended to canonical-7.
- Outputs: Per-embodiment display extends to canonical-7 (loadout app embodiment surface; demo embodiment rendering). Existing VS2b path generalized.
- Effort estimate: ~3–5 days.

### § 1.6 — Decisions-log + canonical updates (deliverables 23–26)

**Deliverable 23 — Decisions-log entry for substrate expansion.**
- Owner: **knight-rider** (drafts) + **gandalf** (reviews) + **jack-ryan** (Gate 1 per CHANGELOG 2026-05-16 rubric — strategy doc producing decisions-log entries; INVOKE).
- Effort estimate: ~half-day.
- Subsumed under hive-mode standard practice: knight-rider drafts; jack-ryan reviews continuous-observation; Matt approves at first available L3 window.

**Deliverable 24 — Decisions-log entry for Earth-Self Court-as-grace resolution.**
- Owner: **knight-rider** (drafts) + **gandalf** (reviews) + **jack-ryan** (Gate 1 — cosmology-load-bearing). Matt L3 approval.
- Effort estimate: ~half-day.

**Deliverable 25 — Decisions-log entry for hive-mind protocol activation.**
- Owner: **knight-rider** (drafts after activation broadcast lands) + **jack-ryan** (Gate 1 — process / engineering-disciplines impact).
- Effort estimate: ~half-day.

**Deliverable 26 — Cross-doc updates.**
- Owner: **gandalf** (canonical-story doc steward).
- Inputs: substrate-expansion-decision § 4 (substrate-cosmology integration); earth-self resolution § 7 (Spirit-Guide as Court storyteller); court-of-forms.md (elevated to architectural commitment per earth-self § 0.3).
- Outputs: Amend `cosmology-reincarnated.md` substrate section (7 not 4); amend `spirit-guide-voice.md` per § 7; promote `court-of-forms.md` § header to architectural-commitment status.
- Effort estimate: ~1–2 days total.

### § 1.7 — Phase-1 P1a prerequisite (deliverable 27)

**Deliverable 27 — Perception test execution.**
- Owner: **drax** (session-runner) + **Matt** + **Matt's son** (subjects, per `user_role.md`) + **jack-ryan** (measurement protocol + analysis).
- Inputs: `perception-test-experiment-scoping-2026-05-17.md`; gandalf authors 4 mechanical pairs + 1 vocabulary quad (8 + 4 = 12 archetypes).
- Outputs: Empirical signal-detection result — does mechanical-parameter vector distance perceptually validate, or must Layer 3 use play-trace feature space? Layer-3 metric spec authored from result.
- Sub-deliverables:
  - drax: session-runner readiness (1 day; per perception-test § 8.4)
  - gandalf + drax: generate 4 mechanical pairs + 1 vocabulary quad (0.5 day)
  - drax + Matt + son: run sessions (2 hours)
  - jack-ryan + gandalf: analysis + decision call (0.5 day)
  - gandalf (conditional): Layer-3 metric spec authoring (1 day)
- **Total Phase-1 P1a duration:** ~3–4 days end-to-end.
- **BLOCKS Deliverable 14 (Layer 3) — but runs in parallel with deliverables 1–3, 4–10, 17–18.** Not on the critical path for the majority of Phase-1 P1 work.

---

## § 2 — Per-seam initial tasking

Per invocation § 4.5; this is the **starting task** each seam picks up at hive activation. As work advances, specialists move to next-task per the coordination matrix without per-task dispatch authorization.

| Seam | Initial task | Why first |
|---|---|---|
| **Rocket** | **Deliverable 1 — Substrate identity loader + YAML extraction** | Layer-1 foundation; unblocks every other deliverable. Read `substrate-identity-declaration-spec` + 7 declarations; extract YAML; build loader; integrate with `foundation.get_rotating_elements()`. Math-before-code N/A (design-then-build). Fail-loud validation MANDATORY per spec § 5.3. |
| **Gamora** | **Deliverable 7 — Resistance matrix 7×7 math note authoring (Discipline #1)** | Math-before-code is load-bearing here. Parallel-startable with rocket Deliverable 1 (gamora doesn't need rocket's loader to author the matrix math). Begin with `simulation/math/resistance-matrix-7x7-phase-1-p1.md`; numeric 7×7 spec + worked DPS-against-each-substrate analysis at L1/L25/L50; jack-ryan reviews continuously. Code lands AFTER math note + rocket Deliverable 1 lands. |
| **Star-lord** | **Deliverable 6 — LLM prompt structure refactor PLAN + scoping doc** | Highest-unknown item per invocation § 7 risk #1. Star-lord begins with a refactor plan + scoping doc (NOT implementation). Plan inventories: (a) the 2-2-1 pair-structure assumption sites; (b) the registry-driven generation shape; (c) per-call-site refactor strategy; (d) revised effort estimate. Knight-rider tracks scope-vs-estimate from week 1. Implementation begins after plan + grouping-vocab extension (Deliverable 20) lands. |
| **Drax** | **Deliverable 27 — Perception-test session-runner readiness** + **Deliverable 19 — VFX library extension planning** | Session-runner readiness is the Phase-1 P1a prerequisite enabler (drax's 1-day item per perception-test § 8.4); VFX library extension planning surfaces vendor-acquisition friction Matt needs to resolve early. Both parallel-startable. Demo-side waits on substrate expansion landing in engine to demo new substrates; loadout-side waits on Deliverable 17 (Court vessel) for browser surface. |
| **Jack-ryan** | **Continuous-observation rhythm setup + baseline test-suite snapshot** | Establishes watchpoints before drift accumulates. Specifically: Discipline #13 (implicit-pillar drift across seams) — monitor for cross-seam substrate inconsistencies; Pattern P7 (silent-default convergence) — monitor for new fallback sites; math-before-code (Discipline #1) — verify math notes precede gamora deliverable 7, gamora deliverable 10; schema-coherence — watch MIGRATION.md authoring concurrency. Baseline test snapshot at `hive/v0.0-pre-phase-1-p1` captures expected GREEN state for drift comparison. |
| **Gandalf** | **Available for continuous design-direction support** + **Deliverable 20 (grouping-vocab extension — small)** | Continuous availability is the design-companion role per protocol § 3.3. Grouping-vocab extension is a 1-day item that must land before star-lord's Deliverable 6 implementation begins — small + low-risk + unblocks downstream. Gandalf may also author Deliverable 8 trait-floor design + Deliverable 9 gear-affix design as gamora gets close to consuming them. |

---

## § 3 — Critical path

The critical path (longest dependency chain through the deliverable DAG):

```
Deliverable 1 (substrate loader)
         ↓
Deliverable 3 (Path-a archetype refactor)  ←─ depends on Deliverables 4 + 5 (registries)
         ↓
Deliverable 7 (resistance matrix 7×7) ←─ also depends on math-note authoring (parallel with D1)
         ↓
Deliverable 10 (substrate-coherent generation rules)
         ↓
Deliverable 14 (Layer 3 diversity gate) ←─ ALSO BLOCKED on Phase-1 P1a perception test (D27)
         ↓
Deliverable 15 (Layer 4 LLM flavor) ←─ ALSO depends on Deliverable 6 (LLM prompt structure refactor)
         ↓
SHIP GATE
```

**Critical-path length estimate:** ~6–8 weeks (D1 ~1wk → D3 ~2wk → D7 ~1wk → D10 ~1wk → D14 ~1-3wk → D15 ~1-2wk + integration testing 1wk).

**Non-critical-path parallel tracks:**
- Court of Forms vessel (D17 + D18) — independent of substrate work; rocket + drax + star-lord parallel.
- VFX library extension (D19) — blocked on Matt acquisitions; once unblocked, drax-parallel.
- Substrate browser (D21) — drax-parallel; needs Layer-1 only.
- Embodiment-display (D22) — drax + star-lord parallel.
- Wide-net registries (D4 + D5) — must precede D3 but can run in parallel with D1.
- LLM prompt refactor (D6) — must precede D15 but can run in parallel with D7 + D10.
- Phase-1 P1a perception test (D27) — must precede D14 implementation; ~3-4 days; parallel-startable.

**Single-largest-risk schedule slip:** Deliverable 6 (LLM prompt structure refactor; ~1-2 weeks estimated, could be 2-3). Star-lord scoping pass first week is the calibration.

---

## § 4 — In-flight work disposition

Per invocation § 6.2; this is the **status-menu reframe** Matt requested. Every standard-mode in-flight item gets a Phase-1 P1 disposition:

### § 4.1 — FOLDED into Phase-1 P1 scope

| Item | How it folds |
|---|---|
| Drift-14 pool-cull + `substrate_native` re-score (rocket) | **✅ SHIPPED** (`rocket/v1.4 @ 65e6d77`). Counts as Deliverable 11. No remaining work. |
| Stage-3 cipher migration (star-lord; SHIPPED `19d8ba0`) + drax v0.21 consumption (`84487ea`) | **✅ SHIPPED.** Cipher cascade is the substrate-of-Layer-4 (Deliverable 15); subsumed into LLM prompt structure refactor (Deliverable 6) for canonical-7 extension. |
| Gamora Gate 3b sim MS consumption + kiting (tag pending pre-commit) | **FOLD.** Tag cut + commit happens as routine engine-state-maintenance during hive. Gate 3b enables movement-speed in sim; substrate-coupling unaffected. Surface to gamora as "cut the tag, then begin Deliverable 7 math note authoring." |
| Telemetry schema V2.x (star-lord) | **FOLD.** Schema work continues per Coupling #9 (recorder substrate-iteration). Tier-1 coverage investigation + observed-ms emission + modifier-flag-tier persistence — all roll into Deliverable 2 sub-tasks. |
| Drax encounters-page explanatory content (PENDING dispatch from Day 4) | **FOLD.** Loadout-app explainer surfaces complement the substrate browser (Deliverable 21); merge planning when drax begins Deliverable 21. |
| Drax demo movement-speed Pixi.js implementation | **FOLD.** Demo-side movement-speed wiring is downstream of gamora Gate 3b + Deliverable 22 embodiment-display. Continue per drax pacing. |
| Wave-4 pack-composition tuning (rocket) | **FOLD.** Wave-composition is generation-rules-adjacent; folds into Deliverable 10 (substrate-coherent generation rules). |
| Form-bias Stage 4 work | **FOLD.** Phase-1 P1 Layers 1-4 naturally subsume Stage 4 work (per invocation § 2.8). |
| Spirit-Guide voice audio Phase-1 (gandalf framework filed) | **FOLD.** Spirit-Guide voice integration is Deliverable 18; cipher-migration dependency D2 already satisfied (drax v0.21 closed 6 LEAK-RISK sites). Voice synthesis work proceeds as part of Deliverable 18. |
| Wind_controller V2 evaluation regen (gamora; queued) | **FOLD.** Substrate-coupled balance question; reads new substrate identity declarations once landed; rolls into Deliverable 10 substrate-coherent generation rules. |

### § 4.2 — PAUSED for post-Phase-1 P1

| Item | Why paused |
|---|---|
| Star-lord Suno music prompt pipeline | Per invocation § 6.2: not load-bearing for Phase-1 P1; audio-track separate from voice (D2 voice). Resume post-ship. |
| Pixogen Full pack acquisition decision | Pixogen Lite already verified clean (Path-A closed Day 4); Full pack adds polish, not Phase-1 P1 scope. Resume post-ship. |
| Decisions-log entries unrelated to substrate work (5 currently aging in `qa/pending/`) | None are substrate-related; none block Phase-1 P1. **EXCEPTION:** if any conflict with Phase-1 P1 commitments, surface to Matt as L3. Otherwise, hold for batch-clearing pass after Phase-1 P1 ships. |
| Environment tileset Kokoro acquisitions (Reaper / Phoenix / Naga; Matt CHANGELOG-authorized 2026-05-17) | Environment tilesets feed Track D (room/hallway renderer); not VFX-library-critical for substrate substrate-visualization. Drax viability tests already complete (Foozle + Reaper). Defer acquisitions to post-Phase-1-P1; Foozle CC0 baseline can hold demo pipeline. |
| Legolas Mode B environment tileset catalogue sweep + Track A reverse VFX audit (2 dispatches authored Day 5; READY-TO-FIRE) | Legolas READY-TO-FIRE items: **Track A reverse audit FOLD** (substrate-expansion gating completed by Phase-1 P1; remaining VFX-to-pool expansion opportunities are P2 candidates). **Mode B environment sweep PAUSE** (environment tilesets are post-Phase-1 P1 per above). |
| Pre-existing 4 gamora engine-side test failures | Pre-Phase-1 P1 technical debt; surface to gamora during initial deliverable-7 work if any are substrate-touched. Otherwise, batch-fix post-ship. |
| jack-ryan calibration analysis (modifier_flag_tier='review' trend detection) | Activation-on-Matt-go; not currently fire. Pause for post-Phase-1 P1; jack-ryan's hive-mode role is continuous-observation, not retrospective analysis. |
| Demo-repo branch conventions (Matt standing item) | Process item; not substrate-related; defer. |
| Memory note for ailment-deferred design proposal (Matt standing item) | Done as part of deliverable 5 substrate-aware ailment registry; the ailment-damage-signatures memory note already CLOSED in `gandalf/open-threads/` 2026-05-16 (Matt-gandalf converged Option B). |

### § 4.3 — STANDALONE Matt-disposition needed before hive activation

| Item | What Matt needs to decide |
|---|---|
| **Vendor acquisitions (CraftPix premium + Fellor Crystal + Frostwindz Deathbringer)** | License/cost payment + on-disk placement at `~/Games/reincarnated-demo/public/assets/<vendor>/`. **Critical-path for Deliverable 19 (VFX library extension)** — substrate VFX integration is downstream. Sequencing: acquire alongside Phase-1 P1 substrate-expansion work so VFX assets land before Deliverable 19 begins demo wiring. |
| **VFX scene-needs spec micro-decisions (gandalf open thread)** | One open thread at `gandalf/open-threads/2026-05-16-vfx-scene-needs-spec-micro-decisions.md`; 2-3 micro-decisions await Matt + gandalf convergence. **Suggestion: fold into hive activation discussion — Matt + gandalf converge on these as part of Deliverable 19 + Deliverable 21 design intake.** |
| **Optional: hive activation timing per protocol § 6.5** | Immediate / scheduled / staged. Knight-rider's recommendation: **STAGED**. Rocket + gamora begin Day-1 (no prep needed); drax begins Day-1 (perception-test session-runner is small ramp); star-lord begins Day-2 (scoping doc for LLM prompt refactor is a paragraph-first task); jack-ryan establishes baseline rhythm Day-1; gandalf available Day-1 + authors Deliverable 20 grouping-vocab Day-1. No hard gate; the hive ramps. |
| **Confirm Phase-1 P1 launch** (per protocol § 12.4) | Final activation gate; Matt's go-word triggers knight-rider's broadcast in hive log + per-seam initial-tasking distribution. |

---

## § 5 — Risk register

Maintained by knight-rider; updated continuously as new risks surface. Initial register per invocation § 7:

| # | Risk | Severity | Mitigation | Owner |
|---|---|---|---|---|
| 1 | **Deliverable 6 (LLM prompt refactor) scope unknown** | HIGH | Star-lord scoping pass week 1 (Deliverable 6 INITIAL task = plan, not code); knight-rider tracks scope-vs-estimate; surface to Matt as L3 if scope exceeds 3 weeks. | knight-rider + star-lord |
| 2 | **Perception test result may invalidate Layer-3 mechanical-parameter metric** | MEDIUM | Phase-1 P1a runs early (~Week 1-2 of hive); Layer-3 design adapts based on result; non-critical-path until Deliverable 14 begins implementation. | gandalf + jack-ryan |
| 3 | **Cross-seam drift (Discipline #13)** | HIGH at this scope | Jack-ryan continuous-observation per protocol § 7.2; daily state-of-hive surfaces drift signals; per-protocol BLOCK authority retained sparingly. | jack-ryan |
| 4 | **Schedule slip (8-12wk estimate is gandalf-authored; seam-specific re-scoping likely)** | MEDIUM | Knight-rider re-scopes after Week 1 seam assessments; surface to Matt as L3 if Phase-1 P1 commitment at risk. | knight-rider |
| 5 | **VFX library readiness depends on vendor acquisitions** | MEDIUM | Surface to Matt early in activation broadcast (this artifact + log activation entry); sequence Deliverable 19 after acquisitions land; Foozle CC0 baseline provides pipeline-testing fallback. | knight-rider |
| 6 | **In-flight work disposition conflicts** | LOW (most items folded cleanly) | § 4 above enumerates per-item disposition; any specialist hitting conflict surfaces L2 to knight-rider. | knight-rider |
| 7 | **Matt availability for L3 decisions** | LOW (hive designed for Matt async) | State-of-hive (daily digest) clearly flags L3 items; respects Matt's availability windows; hive continues productive work during gaps. | knight-rider |
| 8 | **NEW — Concurrent commit race condition (per CHANGELOG 2026-05-16)** | MEDIUM in hive mode (parallel sessions) | All specialists stage by explicit file path (no `-A` / `.` / `-am`); knight-rider does not commit while specialists are committing; consider pre-commit hook for attribution check (out of scope for activation; flagged). | all specialists |
| 9 | **NEW — Test suite breakage compounds under continuous integration** | MEDIUM | Per protocol § 8.5: every commit leaves engine GREEN; broken state >2hrs surfaces to knight-rider for escalation; hive-feature-branch (`hive/feature-<name>`) for temporary-breaking work. | all specialists |

---

## § 6 — Ship gate criteria

Phase-1 P1 ships and `v1.0-phase-1-p1` tag is cut (Matt-approved) when ALL of the following are TRUE:

**Architectural foundation:**
- ✅ All 7 substrate identity declarations loaded and validated at engine boot (Deliverable 1)
- ✅ 14 hardcoded ArchetypeTemplate entries replaced with on-boot substrate × role composition (Deliverable 3)
- ✅ Role registry + ailment registry config-driven (Deliverables 4 + 5)
- ✅ LLM prompt structure registry-driven; no hardcoded 2-2-1 pair-structure assumption (Deliverable 6)
- ✅ All 13 substrate-keyed coupling sites refactored or confirmed GOOD PATTERN (Deliverable 2)
- ✅ All 10 archetype-keyed coupling sites refactored per Path-a (Deliverable 3)

**Engine substrate-coupling:**
- ✅ Resistance matrix 7×7 with paired-luminance valence; math note authored + DPS analysis confirms no class structurally over/under-powered (Deliverable 7)
- ✅ Trait-floor architecture extends to 3 new classes (Deliverable 8)
- ✅ Gear-affix gating extends to 3 new substrates (Deliverable 9)
- ✅ Substrate-coherent generation rules; per-substrate generation-frequency targets met (Deliverable 10)

**Diversity architecture (Layers 1–4):**
- ✅ Layer 1 declarations operational (per Deliverable 1)
- ✅ Layer 2 composition refactor live (per Deliverable 3)
- ✅ Layer 3 diversity gate live; similarity metric perception-test-grounded (Deliverable 14 + 27)
- ✅ Layer 4 LLM flavor diversifier integrates substrate identity + Court-aware referencing (Deliverable 15)
- (Layer 5 deferred to Phase-2; not blocking)

**Phase-0 cosmological vessel:**
- ✅ Court of Forms data structure persists across seasons (Deliverable 17, rocket)
- ✅ Court browsable in loadout app (Deliverable 17, drax)
- ✅ Spirit-Guide voice integrates Court-storyteller role (Deliverable 18)

**Player-facing surface:**
- ✅ VFX library extended for canonical-7; lightning + holy + shadow VFX integrated (Deliverable 19)
- ✅ Substrate browser live in loadout app (Deliverable 21)
- ✅ Embodiment-display extends to canonical-7 (Deliverable 22)

**Decisions-log + canonical:**
- ✅ Three decisions-log entries landed (substrate expansion + Court-as-grace + hive-mind activation; Deliverables 23-25)
- ✅ Cosmology + Spirit-Guide voice + Court-of-Forms doc amendments landed (Deliverable 26)

**Diversity-architecture success criterion (per substrate-expansion-decision § 6.5):**
- Validation pass: dominant-cluster check — of archetypes produced by the diversity architecture, the dominant cluster of 5-8 actually-played archetypes is mechanically different in shape (not cosmetic variants); ≥4-5 of 7 substrates appear in the cluster; ≥3 of 4 roles appear in the cluster.
- **NOTE:** Phase-1 P1 success measurement on this criterion happens via the perception-test rubric extended (no Layer-5 telemetry yet — Phase-2). Synthetic-eval pass via gamora seed-distribution analysis substitutes for in-play measurement at Phase-1 P1 ship.

**Process gates:**
- All hive-mode tagged checkpoints created (per protocol § 5.2; intermediate seam tags + `hive/v0.<N>` milestone tags)
- Test suite GREEN at ship commit
- MIGRATION.md per-seam authored + cross-seam contract coherence verified by jack-ryan
- Database state preserved + backed up (per protocol § 9.3; ship-day backup)
- Retrospective authored (per protocol § 14.2)
- Discipline amendments rolled into `engineering-disciplines.md` (per protocol § 14.2)

**Matt's go-word:** Final ship-gate authority. Matt-approved milestone tag `v1.0-phase-1-p1` cut per ADR-003.

---

## § 7 — Cross-references

**Canonical inputs:**
- `agentic_orchestration/gandalf/requests/2026-05-17-knight-rider-phase-1-p1-full-overhaul-coordination.md` (the invocation)
- `canonical/story/hive-mind-protocol-2026-05-17.md` (operational protocol)
- `canonical/story/substrate-expansion-decision-2026-05-17.md` (substrate set + § 6.5 success criterion)
- `canonical/story/substrate-identity-declaration-spec-2026-05-17.md` (Layer 1 spec)
- `canonical/story/substrate-identity-declarations-2026-05-17.md` (7 declarations)
- `canonical/story/earth-self-diversity-tension-2026-05-17.md` (Court-as-grace; cosmology interface)
- `canonical/story/substrate-coupling-archaeology-2026-05-17.md` (13 substrate-keyed sites)
- `canonical/story/archetype-coupling-archaeology-2026-05-17.md` (10 archetype-keyed sites)
- `canonical/story/wide-net-coupling-archaeology-2026-05-17.md` (14 sites + Pattern P7 cluster + LLM prompt surprise)
- `canonical/story/perception-test-experiment-scoping-2026-05-17.md` (Phase-1 P1a prerequisite)
- `agentic_orchestration/research/knowledge/diversity-architecture-literature-pass-2026-05-17.md` (Legolas Mode A findings)

**Companion hive artifacts:**
- `agentic_orchestration/hive-mind/coordination-matrix.md` (per-deliverable × seam mapping)
- `agentic_orchestration/hive-mind/phase-1-p1-log.md` (append-only hive log)
- `agentic_orchestration/hive-mind/state-of-hive-2026-05-17.md` (activation-day digest)

**Engineering disciplines + governance:**
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Disciplines #1, #12, #13; candidates surfaced today including #14 layer-extensibility-judged-at-perimeter)
- `agentic_orchestration/GOVERNANCE.md` (ADR-004 MIGRATION.md continues; ADR-006 external-state-write requires Matt auth)
- `agentic_orchestration/REVIEW_PROCESS.md` (5 principles + 5 traps continue under hive mode; R11(b) cross-seam round-trip gate continues)
- `agentic_orchestration/AGENTS.md` (team topology; hive mode is operational layer over baseline topology)

---

## § 8 — Maintenance

This document is the **live executable plan** for Phase-1 P1. Knight-rider updates continuously as:
- Deliverables ship (status → ✅)
- Estimates revise based on seam assessments
- New risks surface
- In-flight dispositions resolve
- Ship-gate criteria advance

Updates land via direct edits (no separate change-record; hive log carries the diff via knight-rider STATE entries). Major restructures (e.g., Week-1 effort re-scope) surface as hive log AMENDMENT entries.

---

*Authored 2026-05-17 by knight-rider at Phase-1 P1 hive activation. The hive moves together; this plan keeps it moving in coherent rhythm.*
