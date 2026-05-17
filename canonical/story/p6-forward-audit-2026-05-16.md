# Pattern-P6 Forward Audit — Scoped-Work Implicit-Axis Sweep

**Status:** **Canonical — Matt-commissioned 2026-05-16.** Authored 2026-05-16 by gandalf in response to Matt's directive *"do the forward audit now"* following Drift-11 + Pattern P6 entry in `canonical/story/drift-audit.md`.

**Pattern P6 (one-line):** load-bearing dimension deferred to a later milestone (or implicit-bundled into a multi-axis scoping) becomes upstream of a near-term ship before the deferred milestone arrives.

**Two known P6 instances (Drift-11):** movement-speed baseline (B12 deferred → VS2a-gating); geometry × element VFX coverage (substrate-realignment scoped element + embodiment only → B11 demo-integration-gating).

**This doc's job:** sweep currently-scoped-but-not-yet-active milestones for similar implicit-axis assumptions and surface them before they recur as ship-pressure crises.

**Scope of audit:**
- VS2b (Substrate Realignment + Full Pimen Integration) — five sub-items
- Stage A2 B-series — eight remaining items (B6, B7, B10 V2, B11, B12 full, B13, B14, B16)
- Stage A3+ — B9 series, Stage A4 (B5 + B15), Stage A7 progression
- Cross-cutting axes that show up in multiple milestones

**Companion docs:**
- `canonical/story/drift-audit.md` — pattern P6 + Drift-11 source
- `canonical/16-project-roadmap.md` — milestone definitions audited
- `canonical/story/form-bias-cadence-strategy.md` — substrate-realignment scoping
- `canonical/story/movement-speed-baseline.md` — Drift-11 instance A resolution
- `agentic_orchestration/gandalf/requests/2026-05-16-geometry-vfx-coverage-investigation-b11-gating.md` — Drift-11 instance B resolution

---

## Methodology

For each milestone in scope, I asked:

1. **What dimensions are NAMED in the milestone's scoping?**
2. **What dimensions are IMPLICIT** — assumed-addressable but not enumerated?
3. **What is the next near-term ship after this milestone arrives** at which any implicit dimension could become load-bearing?
4. **Severity** — CRITICAL (must address before milestone or next near-term ship; ship gate), WATCH (addressable when milestone authors; needs surface plan + flag), or OK (implicit but not load-bearing OR already structurally addressed)

This is a structured-but-not-exhaustive pass. A multi-week deep audit would surface more; a one-session audit catches the high-severity items and names the patterns. Where uncertainty remains, I flag it explicitly rather than papering over.

---

## VS2b — Substrate Realignment + Full Catalogue Integration

### S1 — Embodiment-axis added as optional Loadout field

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| Schema field on Loadout; warrior/mage/rogue/hunter label vocabulary | (a) Engine consumption — does generation logic READ embodiment, or is it pure cosmetic? (b) Cross-system propagation — does embodiment flow to telemetry / export / Spirit Guide voice? (c) Free-text vs enum — is embodiment a closed set or extensible? | LOW — embodiment is explicitly designed as narrative skin (per `embodiment-narrative-layer.md`); cosmetic-only is intentional. But the cross-system propagation question is real if any consumer expects an enum value. |

**Severity: WATCH.** Cross-system propagation needs explicit naming in the S1 rocket dispatch when authored. Recommend: rocket dispatch for S1 names ALL consumers of embodiment (loadout display only; not engine generation; not sim; not telemetry; not export) so the cosmetic-only intent is structurally enforced. If any consumer is added later, it's a new decision, not implicit drift.

### S2 — Abstract pair-structure layer alongside canonical-four

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| Pair-structure abstract labels; both labels delivered to generators | (a) Sim coupling — does sim consume pair-structure or canonical-four? (b) Damage-type resolver — are pair-structure resistances modeled or only canonical-four resistances? (c) Telemetry — does telemetry emit both? Either? Neither? | MEDIUM — pair-structure is a cipher-width-dependent design; coupling to sim is genuinely TBD until cipher-width lands |

**Severity: WATCH.** This is partially resolved by the cipher-width sub-lock work already in flight (per `form-bias-cadence-strategy.md` § 5.3 + § 6.2). However, the sim-coupling question is gamora-territory and not currently surfaced in any commission. Recommend: when knight-rider authors the S2 gamora dispatch, the dispatch explicitly names which layer (generation / sim / damage resolver) consumes pair-structure vs canonical-four. If sim continues to consume canonical-four scaling while generation emits pair-structure, that's a structural divergence worth naming.

### S3 — Hide canonical-four from LLM (cipher migration)

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| Prompt template changes; no-seed cosmology test; LLM-visible-surface filter | **(a) Telemetry emission paths — do telemetry events emit canonical-four labels that could leak via debug logs / dev tools / community datamining? (b) Export schemas — does the export packet emit canonical-four labels for downstream consumers? (c) Spirit Guide voice — does the in-game voice ever reference canonical-four labels? (d) Loadout app display — does loadout UI ever show canonical-four labels even when game seasons surface per-season vocabulary?** | **HIGH — multiple unaudited paths** |

**Severity: CRITICAL** (for VS2b S3 ship). The cipher migration's value is undermined if canonical-four labels leak through any non-LLM path that touches player or public-facing surfaces. **Recommend: paths-audit dispatch to star-lord** before S3 implementation begins. Inventory every place canonical-four labels appear in: (1) telemetry events; (2) export packet fields; (3) Spirit Guide prompt templates; (4) Spirit Guide voice output; (5) loadout app data display; (6) debug logging at any level. For each, classify as INTENDED-INTERNAL / INTENDED-PUBLIC-AS-CIPHER / LEAK-RISK / TO-BE-FILTERED. Without this audit, S3 ships with the cipher leaking through unaudited paths.

**This is a new P6 instance candidate.** The S3 scoping named "LLM prompt template filter" but did not enumerate "all other surfaces that could emit canonical-four labels." Filing as **Drift-11.5 candidate** — recommend new Drift-12 entry once paths-audit returns concrete findings.

### Embodiment-as-narrative-skin display (loadout + demo)

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| Display layer surface change; per-embodiment narrative rendering | **(a) Per-class portrait/character sprite art — does each embodiment need a unique character visual? (b) Character-animation conventions — does embodiment affect idle/cast/move animations?** | HIGH — character-art axis is known-uncatalogued |

**Severity: CRITICAL** (for VS2b display ship). The `gandalf-pimen-sample-design-review.md` already flagged character/enemy coverage as a separate follow-on commission ("character-only vendors out-of-scope for Step B Tier-1; separate track per Q4"). VS2b's embodiment display surface needs character art that isn't on any current sourcing track. **This is the most likely next P6 instance to bite.**

**Recommended action: surface this NOW** as a sequencing concern for knight-rider, not at VS2b display ship time. Knight-rider should author a sub-commission for character-track vendor sweep (parallel to Step B Tier-1 substrate sweep already in flight) targeting completion in the same window as VS2b S1/S2/S3 so character coverage is known when VS2b display work activates. If character coverage is found inadequate, options surface BEFORE VS2b display ship rather than AT VS2b display ship.

### Full Pimen catalogue integration

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| Broader VFX coverage; multi-season visual diversity; character sprites where catalogue supports | **(a) Cross-pack animation consistency — frame rates / hold-times / loop boundaries vary between Pimen packs (verified in sample review); drax compositing must harmonize. (b) Audio companion assets — does Pimen ship audio? Does ANY vendor in Tier-1 ship audio? Is audio entirely unscoped at the catalogue layer? (c) Palette consistency within element — do Fire 01 / Fire 02 / Fire 03 share a color palette, or are they three different fire palettes? Does the cipher-width / per-season-vocabulary architecture have a stance on this?** | HIGH — audio axis is **completely uncatalogued and unscoped** |

**Severity: CRITICAL** (for VS2b Pimen full ship — audio specifically). **Audio is entirely absent from the entire catalogue / form-bias / substrate-realignment / pitch-positioning corpus.** Demo VS2a will presumably ship without sound; that's a defensible Phase-0 demo choice. But Phase-0 will not stay silent forever — at some point audio is needed, and **zero current scoping considers whether Tier-1 VFX vendors ship audio companions, what register audio should be in, or whether audio is a separate sourcing axis.**

**This is the largest P6 instance the forward audit surfaces.** Audio is not a single dimension — it's a parallel catalogue (sound effects per geometry; ambient audio per season; spirit-guide voice synthesis; combat-feedback audio; UI audio). All entirely unscoped.

**Recommended action: Matt-direct decision needed** — is audio in scope for any pre-Phase-1 ship? If yes, audio-strategy doc + audio-catalogue commission warrants its own thread. If no, **name "audio scoped to Phase-1+" explicitly in the canonical corpus** so the assumption is structural rather than implicit. Either way, no longer implicit.

The cross-pack animation consistency point is WATCH — drax already noted canvas-size discipline in pimen sample review; compositing harmonization will need a drax design pass when full integration activates.

---

## Stage A2 — Remaining B-series

### B6 — Class kit composition + Hierarchical Skill Tree + energy-type-aware tier assignment

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| Kit composition rules; tree structure (4 tiers × 2-4 chains); hierarchical unlock gates; cross-chain asymmetry; rage/physical tier-bound compensation | **(a) Skill tree UI — engine emits tree structure; demo/loadout need UI to RENDER tree. Per-class visual identity for trees. (b) Tree-node icons — each skill in the tree needs an icon; where does icon art come from? (c) Tree-progression VFX — when player unlocks a tier or chain, is there a feedback effect?** | HIGH — UI surfaces systematically under-scoped |

**Severity: CRITICAL** (for VS2a ship — UI specifically). B6 is in VS2a scope. The engine + balance work is named; the corresponding demo/loadout UI surface to render the tree is implicit-bundled into "drax work" without dimension-decomposition.

**Recommended action:** knight-rider authors a drax UI-scoping sub-commission for B6 skill-tree display BEFORE B6 engine work ships. Scope: tree rendering shape (vertical / horizontal / radial); node icon strategy (custom art / procedural / placeholder); unlock-feedback affordance. Without this, B6 ships with engine tree data and no UI to display it.

### B7 — Gear-percentile variance check

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| Pass/fail gate at percentiles; runs at endgame L50 | (a) Depends on B16 (drop architecture) for actual gear-distribution data; (b) Depends on (eventually) gear-equip system per Priority 02 / B12 full | LOW — sequencing already implicit-named in roadmap |

**Severity: OK.** B7 cleanly depends on B16; the dependency is named in roadmap. No P6 risk surface here.

### B10 V2 — Sequential-room semantics

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| HP/resource carryover between encounters; gauntlet structure | (a) Demo arena restructure — sequential rooms imply room-to-room transitions; current arena is single-ellipse; (b) Save state / persistence — does HP carryover persist if player exits/re-enters? | MEDIUM — arena restructure is demo work; not yet scoped |

**Severity: WATCH.** B10 V2 is in VS2a scope but the demo arena restructure to support multi-room sequential play is implicit. Recommend: drax dispatch for B10 V2 demo work explicitly names arena restructure scope (do current `arena.ts` ellipse bounds extend or get replaced; what visual cue distinguishes rooms; how does player traverse rooms).

### B11 — Geometry palette expansion

Already gated per Drift-11 instance B. **Severity: OK** (resolved).

### B12 — Full audit (boots/gloves/belt + +% MS affixes + hard-cap)

Baseline subset shipped in VS2a per Drift-11 instance A. Full audit remains Stage A2.

| Named dimensions (full audit) | Implicit dimensions | Risk |
|---|---|---|
| Boots/gloves/belt gear slots; +% MS affix; hard cap +25% from gear | **(a) Gear DROP integration — does B12 produce gear that B16 drops, or is sequencing reversed? (b) Gear EQUIP UX in demo/loadout — equip flow; affix display; tooltip; (c) +% MS affix VFX — does a sprint-affixed player visibly speed up? Particle trail? (d) Hard-cap UX — when player hits 125% MS cap, is there a UI indication?** | HIGH — multiple implicit axes |

**Severity: WATCH.** Stage A2 isn't immediate but is the next sprint after VS2a/VS2b. Recommend: when knight-rider authors B12 full dispatch, decomposition explicitly enumerates (a)-(d) as named dimensions; each gets scope or explicit defer-with-acknowledgement.

### B13 — Active mobility + telegraphs + i-frames + emergence observability

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| 5 new defensive geometries (covered by geometry-coverage investigation); cast_time + damage_resolution_time + i_frame_window fields; telegraphs; asymmetric indicator scaling | **(a) Telegraph art convention — what SHAPE does a telegraph take (circle? cone? line?)? Is telegraph art primitive-shape-rendered or sprite-based? Where does it come from? (b) i-frame visual feedback — when player is in i-frames, is there a visual indication (flicker? glow?)? (c) Emergence-observability instrumentation — what does the observability surface look like (telemetry events? export packet field? gandalf-readable summary)?** | MEDIUM — telegraph art is a real gap |

**Severity: WATCH.** Telegraph art is its own implicit dimension. Most ARPGs use primitive-shape-rendered telegraphs (circles, lines, cones) that don't require vendor sourcing — but stylistic consistency with the cipher-substrate-VFX register matters. Recommend: when knight-rider authors B13 dispatch, telegraph-art convention is an explicit decision (primitive-rendered vs vendor-sourced); if primitive-rendered, color/opacity/animation conventions named.

### B14 — Multi-band convergence simulator

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| 3-band convergence at L17/L33/L50; 9 runs per class; per-band kit composition emission | (a) Engine-internal only; no obvious demo/UI surface; (b) Telemetry expansion — does telemetry emit per-band data? | LOW |

**Severity: OK.** B14 is engine-internal; telemetry expansion is a small naming-not-blocker issue.

### B16 — Loot drop architecture

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| Drop event mechanism; rarity tables; smart-loot 70/30; ilvl tracking; demo drop rendering + auto-pickup | **(a) Drop ANIMATION — loot dropping from monster as a visible event; impact sprite when loot hits ground; (b) Loot BEAM/PILLAR — Diablo-staple visual indicator over high-rarity drops; explicit visual element needing art; (c) Loot rarity COLORS — well-established convention (white/blue/yellow/orange/green) but needs locking + accessibility check; (d) Loot tooltip design — affix display; comparison-to-equipped; (e) Auto-pickup ANIMATION — when pet/auto picks up loot, is there a visual feedback?** | HIGH — multiple visual axes that aren't on any sourcing track |

**Severity: CRITICAL** (for B16 ship). The drop architecture is named extensively at the data layer (rarity tables; ilvl; drop pools) but the entire visual presentation layer is implicit-bundled into "demo: drops render in world + auto-pickup." Loot-pillar art alone is a recognizable Diablo-staple that's not on any catalogue or art-sourcing track. **This is a P6 instance in waiting.**

**Recommended action:** when B16 work activates (post-VS2a), knight-rider's dispatch enumeration must include (a)-(e). Some are primitive-rendered (rarity colors, loot beams); some need sourcing (drop animation, impact sprite). Filing as **Drift-12 candidate** — surface to drift-audit when B16 dispatch authoring begins.

---

## Stage A3+ — Forward-look

### B9 series — Traits + skill points + reset + Spirit Guide coach

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| Per-class trait pool; level gating; per-rank power curves; skill point distribution; reset mechanism; Spirit Guide coaching | **(a) Trait display UI in loadout/demo — how does player see their traits? (b) Trait icons — each trait needs visual identity; (c) Spirit Guide UI presentation — voice is canonical, UI presentation is implicit; (d) Build-reset UX — confirmation flow; warning copy; (e) Doppelganger encounter visuals (B9-adjacent) — visual continuity with the player's prior self** | HIGH — multiple UI axes |

**Severity: WATCH.** B9 series is Stage A3, post-A2; not immediately blocking. But UI surfaces follow the same pattern as B6 skill tree — implicit-bundled into "demo/loadout work." Recommend: same prevention prescription as B6 — when B9 dispatches author, UI decomposition explicit.

Specifically the **doppelganger visual identity** is load-bearing per `cosmology-reincarnated.md` and the Earth Meta-Layer framing — doppelgangers carry trophy-value for body library accumulation. Visual continuity with the player's prior incarnations is not implicit-render-the-same-character; it's a designed moment that needs explicit visual scoping.

### Stage A4 — B5 Legendary abilities + B15 Seasonal Sets

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| Legendary affixes (granted_ability / aura / on_hit / cast_on_attack); seasonal sets (one per class per season; L50-only drops; 2/4/full-set bonuses) | **(a) Legendary VISUAL IDENTITY — does a legendary gear-piece have unique visual? Glow? Particle effect? (b) Set BONUS visual feedback — when full set equipped, is there a feedback effect? Aura? (c) Legendary tooltip design — affix display; legendary-specific framing; (d) Set collection UI — gather-your-favorite-set seasonal goal needs UI surface** | HIGH — Diablo-staple visuals + entire set-collection UI implicit |

**Severity: WATCH.** Stage A4 is well downstream of current work. But this is exactly where P6 instances breed in scoping docs — the "Stage A4 ships legendary affixes" line item carries multiple implicit visual + UI axes. Recommend: forward-flag now so Stage A4 authoring decomposes explicitly. Legendary visual identity and set-collection UI are both player-facing in ways that fundamentally affect Stage A4's playtest cycle (Playtest #3 per roadmap).

### Stage A7 — Progression system implementation

| Named dimensions | Implicit dimensions | Risk |
|---|---|---|
| XP/leveling, stats, body-swap pool tracking, doppelganger encounters, end-game quest, ilvl, Spirit Guide cross-phase coaching, form library ascension | **(a) Body-swap TRANSITION VFX — the moment of swap is canonical per `cosmology-reincarnated.md` + `ascension-moment-ritual.md`; engine/demo coupling is implicit. (b) Form library UI — gacha-style accumulation surface; (c) End-game quest narrative + visual presentation; (d) Earth Meta-Layer surface — the canvas where player returns post-Phase-0; not even scoped at the demo/UI level** | VERY HIGH — multiple narrative moments + Earth Meta-Layer UI |

**Severity: WATCH.** Stage A7 is the deepest forward-look in current roadmap. The body-swap moment and Earth-Self return are CANONICAL DESIGN PILLARS (per `cosmology-reincarnated.md`, `ascension-moment-ritual.md`, `passage-moment-ritual.md`, Earth Meta-Layer thread) — but their implementation surface in engine + demo + loadout is implicit-bundled into Stage A7's omnibus "progression system implementation" line. **This is the largest forward P6 risk surface.**

Recommended action: when Stage A7 design + implementation activates (post-Stage A4), the dispatch authoring must decompose by named ritual moment. Each ritual already has its own canonical doc; the Stage A7 implementation scope should explicitly name which docs each implementation phase consumes.

---

## Cross-cutting P6 sub-patterns observed

The per-milestone sweep surfaced several patterns that cut across multiple milestones. Naming them helps future prevention:

### Sub-pattern P6.a — UI surfaces are systematically implicit-bundled into "demo/loadout work"

**Instances:** B6 skill tree UI; B9 trait display UI + Spirit Guide UI; B12 gear equip UX; B16 loot tooltip + filter; Stage A4 legendary tooltip + set collection UI; Stage A7 form library UI

**Pattern:** every engine-side data feature implies a corresponding demo/loadout UI surface to render that data for the player. Roadmap entries name the engine work explicitly; UI work is implicit-bundled into a generic "demo work" line.

**Prevention prescription:** every B-series dispatch authoring should produce a paired UI scope decomposition. Recommend adding to engineering-disciplines as candidate Discipline #15 — *"UI scope decomposition for every player-facing engine feature."*

### Sub-pattern P6.b — Audio is entirely unscoped at every milestone layer

**Instances:** none, because audio doesn't appear in ANY current scoping doc

**Pattern:** Phase-0 demo will presumably ship silent. At some point audio is needed. Zero current scoping considers vendor coverage, register, audio-VFX coupling, or audio-source strategy. The substrate-realignment work has not been audited for audio companion catalogues.

**Prevention prescription:** Matt-direct decision needed — name when audio enters scope (Phase 1? VS2c? deferred indefinitely?). Until named, this is the largest single P6 risk in the corpus.

**🟢 RESOLVED 2026-05-16 — Matt delegated, gandalf decided.** See `canonical/story/audio-strategy-phase0.md`. Music deferred to Phase 1+ (Matt's AI-music-generator workflow IS the Phase-0 strategy). SFX deferred to Phase 1+ at production scope; near-zero-cost `audio_companion_availability` audit amendment added to in-flight Step B Tier-1 crawl so Phase 1 has data ready. Phase-1 promotion triggers explicitly named (playtest signal / external-facing moment / Phase 1 start).

### Sub-pattern P6.c — Telegraph / feedback / indicator art has no source plan

**Instances:** B13 telegraphs; B16 loot pillars; Stage A4 set-bonus feedback; Stage A7 ritual moments

**Pattern:** game-feel feedback visuals (telegraphs, indicators, ritual moments, set bonuses) are conceptually load-bearing but never sourced from the catalogue work. The catalogue investigation targets SKILL-effect VFX; feedback-VFX is a different category entirely.

**Prevention prescription:** treat feedback-VFX as a distinct art category with explicit decision on primitive-rendered vs vendor-sourced vs hand-author. Decision needed before B13 ships at minimum.

### Sub-pattern P6.d — Character-art axis is known-gap but VS2b needs it

**Instance:** VS2b embodiment-as-narrative-skin display

**Pattern:** character art was flagged out-of-scope for Step B Tier-1 substrate sweep (Q4 of original commission); separate character-track sub-commission has not yet been authored. VS2b display work needs character art.

**Prevention prescription:** knight-rider authors character-track vendor sweep NOW (parallel to Step B Tier-1) targeting completion in VS2b S1/S2/S3 window. Already partially named in pimen-sample-design-review; needs operationalization.

### Sub-pattern P6.e — Cipher migration paths-audit is missing

**Instance:** VS2b S3

**Pattern:** S3 scoping named the LLM-prompt-template filter but did not enumerate all other paths through which canonical-four labels could surface (telemetry, export, loadout, debug logs, Spirit Guide voice).

**Prevention prescription:** star-lord paths-audit dispatch BEFORE S3 implementation begins.

---

## Severity summary + recommended commissions

| Finding | Severity | Recommended commission | Sequence |
|---|---|---|---|
| VS2b S3 cipher migration — paths-audit missing | **CRITICAL** | Star-lord paths-audit dispatch | Before S3 implementation begins |
| VS2b embodiment-display — character art axis | **CRITICAL** | Legolas character-track vendor sweep (parallel to Step B Tier-1) | Before VS2b display work activates |
| ~~VS2b Pimen full — audio scoping~~ | **🟢 RESOLVED 2026-05-16** | Matt delegated → gandalf decided: audio Phase 1+; see `canonical/story/audio-strategy-phase0.md` | Closed |
| B6 skill tree UI surface | **CRITICAL** | Knight-rider drax UI-scoping sub-commission for B6 | Before B6 engine work ships in VS2a |
| B16 loot visual presentation layer | **CRITICAL (timing-shifted)** | Decomposition required at B16 dispatch authoring (post-VS2a) — file as Drift-12 candidate | When B16 authoring begins |
| VS2b S1 cross-system propagation of embodiment | WATCH | Name explicitly in S1 rocket dispatch | At S1 authoring |
| VS2b S2 sim-coupling of pair-structure | WATCH | Name explicitly in S2 gamora dispatch | At S2 authoring |
| B10 V2 arena restructure for sequential rooms | WATCH | Name explicitly in B10 V2 drax dispatch | At B10 V2 demo authoring |
| B12 full audit visual/UX axes | WATCH | Decomposition required at B12 full dispatch | At B12 full authoring (post-VS2a) |
| B13 telegraph art convention | WATCH | Explicit decision in B13 dispatch (primitive vs sourced) | At B13 authoring |
| B9 trait UI + doppelganger visual identity | WATCH | Decomposition at B9 series authoring | At B9 authoring |
| Stage A4 legendary visual + set collection UI | WATCH | Decomposition at Stage A4 authoring | At Stage A4 authoring |
| Stage A7 ritual moments + Earth Meta-Layer | WATCH | Decomposition by named ritual when Stage A7 activates | At Stage A7 authoring |

**Total CRITICAL findings: 5.** Three address VS2b directly (S3 paths-audit; embodiment character art; audio decision); one addresses B6 VS2a-scope; one is timing-shifted to B16 authoring.

**Total WATCH findings: 8.** Each carries a prescription for the eventual milestone authoring.

---

## What this audit does NOT do

- Does not author the recommended commissions — that's knight-rider per ADR-002
- Does not run the recommended paths-audit or vendor sweeps — those are downstream specialist work
- Does not amend scopes unilaterally — surfaces findings; Matt approves commission cascade
- Does not claim exhaustive coverage — explicitly named as structured-but-not-exhaustive; deeper audit would surface more
- Does not address Phase-1+ scope items not in current roadmap
- Does not assess whether any current CRITICAL finding's mitigation introduces a new P6 instance (recursive audit is out of scope; if recursion needed, surface as separate sweep)

---

## Recommended next actions

For Matt (decisions):
1. **Audio scope decision** — name when audio enters the corpus. Recommendation: name "Phase 1+" if no near-term need; commission audio-strategy doc if any pre-Phase-1 work uses audio.

For knight-rider (commission authoring):
1. **Star-lord paths-audit dispatch** for cipher migration leak risks — BEFORE VS2b S3 implementation begins
2. **Legolas character-track vendor sweep** — parallel to Step B Tier-1; targets VS2b display window
3. **Drax UI-scoping sub-commission for B6 skill tree** — before B6 engine work ships in VS2a
4. **Surface Drift-12 candidate** to gandalf when B16 dispatch authoring begins

For gandalf (self):
1. Surface Drift-11.5 / Drift-12 candidates to `drift-audit.md` when paths-audit + B16-decomposition findings return
2. Re-run this forward audit after Stage A2 completes (likely surfaces new P6 instances as new scoping accumulates)
3. Author Discipline #15 candidate ("UI scope decomposition for every player-facing engine feature") for jack-ryan engineering-disciplines consideration

---

— gandalf, 2026-05-16 (Day 4)
