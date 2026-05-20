# Engine Architecture Vision — QD-Optimization + Profile-Based Deployment (2026-05-19 late evening)

**Status:** **Canonical architectural target.** This document etches into stone the architectural synthesis that emerged 2026-05-19 evening through Matt + gandalf theory-crafting. It establishes:

1. The **engine's architectural target** post-recompose-validation: Quality-Diversity (QD) optimization with profile-based deployment configuration
2. The **commercial path unification** model: Paths A/B/C/D are four profiles of one engine, not four engines
3. The **dogfood pattern**: Reincarnated-the-game IS the reference implementation for the B2B engine; they are the same engine binary with different profile configurations
4. The **Information-Deferred-to-Coalescence (IDC) meta-principle** that unifies R8 inverted-mode + emergent-archetype-taxonomy + the broader engine architecture
5. The **engineering roadmap** from current engine state to QD-profile MVP
6. The **dependencies + gates** that condition each architectural commitment

**Authority:** Matt directive 2026-05-19 evening (*"Thank you for articulating my vision and also expanding the market in ways that I hadn't thought of... we should etch these decisions into stone"*); gandalf canonical-authorship under autonomous-operation L2-equivalent.

**Authored:** 2026-05-19 late evening by gandalf. This is theory-craft canonical — meaning it represents the architectural direction the project is committed to *target*, not the architecture that exists today. Section 9 names what's proven vs what's hypothesized.

---

## § 0 — TL;DR

**The engine's architectural target is a Quality-Diversity (QD) content generator with profile-based deployment.** One engine binary, configured via profile YAMLs, serves four distinct commercial paths:

- **Profile A — Reincarnated-standalone** (mobile-first ARPG; weekly seasonal cadence; ~15-25 archetypes/season; cross-season Court-of-Forms accumulation)
- **Profile B — B2B SaaS** (AAA live-ops customer; quarterly-to-annual cadence; 100+ archetypes per theme; decision-tree deployment; tiered monetization including epic-archive)
- **Profile C — Mod-pack exporter** (mod authors shipping to GD/TQAE/TL2; per-host-game adapters; 10-25 archetypes per pack; host-compatibility fitness criterion)
- **Profile D — Solo-dev / hobbyist** (small-budget; user-configurable; private; serves the broader-adoption flywheel)

**The engine itself implements QD optimization via MAP-Elites-style behavior-space discretization + cell-archive maintenance, layered on top of the per-tier convergence + recompose mechanism** the recompose-validation hive is currently testing. Cells in the behavior space are archetypes by construction; the archive fills via continued generation under fitness + novelty pressure; theme + archetype identity emerge via LLM coalescence post-archive-fill (the IDC pattern).

**Commercial implication:** Path B (mod-first) ships Profile C; Path A (standalone) ships Profile A; Path C (engine-as-tool) sells Profile B with customer-specific tuning. **They are not three engines; they are three profiles of one engine.** Reincarnated-the-game ships as Profile A, becoming the credentialing reference implementation that B2B prospects evaluate.

**Engineering investment from current state:** ~8-12 weeks focused work to MVP QD-engine with profile architecture, conditional on the recompose-validation hive (currently firing) succeeding. Each subsequent profile adds ~1-2 weeks of profile-specific configuration + validation. The dominant cost is the engine core; the profiles are bounded configuration deltas.

**This document is canonical commitment to the architectural direction.** Implementation work follows; canonical-doc amendments propagate as findings sharpen the design.

---

## § 1 — Provenance and scope

### § 1.1 — How this vision emerged

This document captures architectural decisions crystallized through a single late-evening session 2026-05-19. The session arc:

1. **Gandalf white-wizard synthesis** of the day's hive-mind findings — surfaced that the engine's per-tier convergence failures were measuring cross-contract mismatch (kits converged for aggregate-mean ran against new per-tier targets) rather than catalogue pathology
2. **Recompose-validation hive activated** to test whether unblocking the recompose mechanism (Option A floor widening → Option B trigger conditioning → fresh regen) produces shippable kits under per-tier targets
3. **Theory-craft session opened** by Matt explicitly requesting architectural exploration above white-wizard register ("ascend above white-wizard status... invoking a theoretical mathematician agent")
4. **Two parallel architectural threads merged:**
   - The intra-season archetype-uniqueness mechanism (novelty search + emergent clustering + LLM naming)
   - The yearly-content B2B vision from the Apex Director debrief (cement-deep-season + decision-trees + monetization tiers)
5. **The synthesis arrived** when both threads were recognized as instances of the same architectural target: Quality-Diversity optimization with profile-based deployment

### § 1.2 — What this document claims

**Claims:**
- QD optimization (MAP-Elites family of algorithms) is the architecturally-correct framework for the engine's content generation
- Profile-based deployment is the architecturally-correct framework for the engine's commercial model
- Reincarnated-the-game and the B2B service are profiles of the same engine, not separate engines
- The IDC meta-principle (information-deferred-to-coalescence) unifies multiple architectural moves (R8 inverted mode + emergent archetypes + emergent role taxonomies + post-hoc cohesion calibration)
- The path from current engine state to QD-profile MVP is bounded engineering (~8-12 weeks) conditional on the recompose-validation hive's success

### § 1.3 — What this document does NOT claim

**Does NOT claim:**
- That the QD-profile engine exists today (it does not; this is a target)
- That Pattern-B commercial direction is committed (Pattern-B remains parked per `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`)
- That the recompose-validation hive has succeeded (it is firing as of this writing)
- That the engineering investment is approved (Matt's commercial-direction decision precedes the engineering commit)
- That the four profiles' specifications are final (they are starting points; will refine with usage)

This is a *vision document*. It establishes the architectural target so that all downstream work aligns to a shared destination. Implementation decisions, dispatch authoring, and resource allocation will be made by separate dispositions referencing this vision.

### § 1.4 — Stewardship

**Gandalf stewards this document** as the cross-cutting design and architecture record. Amendments require gandalf authorship + Matt review at major revisions. Sub-section refinements may be authored by gandalf during autonomous operation without Matt approval if they sharpen rather than redirect the vision. Major architectural pivots (e.g., abandoning QD for a different paradigm) require explicit Matt approval per autonomous-operation protocol § 4.0.

---

## § 2 — The architectural target — QD-engine

### § 2.1 — Why Quality-Diversity (not just Quality)

Standard optimization finds **one good solution per problem**. Maximize fitness; return the best.

Quality-Diversity (QD) optimization finds **a diverse archive of high-quality solutions, organized by behavioral characteristics.** Maximize fitness conditional on filling diverse behavioral niches.

The engine's content-generation task is QD-shaped:
- Per-tier balance is the quality criterion (fitness)
- Archetype diversity is the diversity criterion (behavioral characteristics)
- A season needs MANY archetypes, each distinct, all balanced — exactly what QD produces

Standard optimization produces one "balanced kit" per class. QD optimization produces a season's worth of distinct balanced kits. **The shift is from per-class convergence to per-cell-archive convergence.**

### § 2.2 — MAP-Elites as the algorithm family

The canonical QD algorithm is **MAP-Elites** (Mouret & Clune, 2015 — "Illuminating search spaces by mapping elites"). Adapted for Reincarnated:

```
1. DEFINE Behavior Space:
   B = product space of behavioral characteristics (BCs)
   Each BC is a discretized dimension; e.g., AOE-share × DPS-curve-shape × range-profile
   Grid size = product of BC bin counts; e.g., 5 × 5 × 4 × 4 × 3 = 1,200 cells

2. INITIALIZE Archive:
   A = empty grid; one cell per (BC₁_bin, BC₂_bin, ..., BCₙ_bin) tuple

3. GENERATE-AND-INSERT loop:
   For each iteration:
     a. Generate candidate kit k via existing engine (R8-inverted; recompose-enabled)
     b. Compute BC_vector(k) — which cell does k occupy?
     c. Compute fitness(k) — balance-band-membership + theme-cohesion + novelty
     d. If cell is empty OR fitness(k) > fitness(A[cell]): A[cell] = k
     e. Track marginal-novelty signal; stop when saturated

4. POST-PROCESS:
   - Cluster occupied cells (HDBSCAN; emergent archetype groups)
   - LLM-coalesce archetype names per cluster
   - LLM-coalesce season theme from full archive
   - Export archive as season manifest
```

**The archive IS the season.** Each occupied cell is one archetype. The grid topology gives you behavioral coverage that's mathematically explicit, not nominal.

### § 2.3 — Behavior Characteristics (BCs) — the load-bearing design choice

The BCs determine *what counts as a distinct archetype*. Choose BCs that capture meaningful mechanical variation; archetypes will be mechanically distinct. Choose BCs that capture surface variation (e.g., color, naming); archetypes will be superficially diverse but mechanically same.

**Starting BC axes (Profile A — Reincarnated):**

| BC | Bins | Rationale |
|---|---|---|
| AOE-share | 5 (0-20%, 20-40%, 40-60%, 60-80%, 80-100%) | Captures the core asymmetry that drives kit identity |
| DPS-curve-shape | 5 (front-loaded, even, back-loaded, burst, sustained) | How damage distributes over a fight |
| range-profile | 4 (close, medium, long, mixed) | Engagement style |
| energy-cycle | 4 (mana-flow, rage-spike, combo-chain, focus-drain) | Resource pattern |
| control-density | 3 (none, modest, heavy) | Status-effect / debuff weight |

Total grid: 5 × 5 × 4 × 4 × 3 = **1,200 cells**

Realistic fill rate for a season: ~15-25 cells (~1-2% fill). The rest are infeasible (excluded by constraints) or sparsely-sampled (under-explored).

**Profile B (B2B AAA) extends with additional BCs:**

| Additional BC | Bins | Rationale |
|---|---|---|
| burst-window-shape | 4 | Theory-craft community cares about this distinction |
| defensive-layer | 3 (none, modest, heavy) | Survival profile |
| build-orthogonality-axis | 4 | Mechanical decision points players engage with |

Total grid: 1,200 × 4 × 3 × 4 = **57,600 cells**. Realistic fill rate ~0.2-0.5% = 100-300 archetypes per yearly theme.

**The BC choice IS the product design choice.** Profile-author-time decision; not run-time decision.

### § 2.4 — Fitness function composition

The fitness function is a weighted combination of metrics:

```
fitness(k, archive, theme) = 
    w_balance × balance_band_score(k)
  + w_cohesion × theme_cohesion_score(k, theme)
  + w_novelty × novelty_score(k, archive)
  + w_orthogonality × mechanical_orthogonality_score(k, archive)
  + w_continuity × cross_season_continuity_score(k, meta_archive)
  + Σ profile_specific_weighting
```

Where:
- `balance_band_score`: 1.0 if all per-tier WR in band; lower otherwise (smooth penalty for partial misses)
- `theme_cohesion_score`: LLM-judged or embedding-similarity-derived score on whether k reads as thematically coherent with the season's substrate-identity
- `novelty_score`: nearest-neighbor distance from current archive (inversely; closer = lower)
- `mechanical_orthogonality_score`: degree to which k's optimal build differs from existing archive's optimal builds
- `cross_season_continuity_score` (Profile A only): alignment with Court-of-Forms meta-archetype-registry

**Fitness weights are first-class profile fields.** Different deployments order the metrics differently per § 4.

### § 2.5 — The "epic archive" — out-of-balance-band generation

A second archive operates in parallel with the standard archive but **inverts the balance criterion** — generates kits that intentionally fail per-tier targets while remaining theme-coherent.

```
Standard archive lives in: B ∩ T_θ (balance-band kits ∩ thematic-coherence)
Epic archive lives in: T_θ \ B (theme-coherent but OUT of balance band)
```

Three epic categories (all derived from QD over the epic-space):

| Category | Characterization | Player experience |
|---|---|---|
| **Over-tuned** | Above WR ceiling — trivializes tiers in <50% expected time | Power-fantasy; "delete the boss" appeal |
| **Asymmetric-anti-meta** | Specialized — trivializes one tier while collapsing on others | Niche / build-crafting interest |
| **Unfair-deep** | Heavy balance violations (modifier > ceiling) but coherent kit logic | Convention-breaking endgame |

The epic archive is **opt-in per profile** (default off for Profile A; default on for Profile B's monetization layer). When on, the engine runs a second QD pass with relaxed fitness, producing the epic-tier content alongside the balanced standard archive.

### § 2.6 — Theme discovery via Best-Arm Identification

For Profile B (yearly-content B2B), the engine must explore many candidate themes and select the most expansive one. This is a multi-armed bandit problem with a known optimal-stopping framework: **Best-Arm Identification with PAC guarantees** (LUCB1 or related algorithms).

```
Setup:
  N candidate themes (e.g., 50-100 substrate-anchor combinations)
  Each theme: unknown "QD-capacity" (fill rate × diameter × effective dimension)
  Budget: total exploration compute
  Goal: identify the theme with maximum QD-capacity with high confidence

Algorithm (Best-Arm Identification via LUCB1):
  1. Initialize: pull each theme once (cheap partial QD run)
  2. Iterate:
     - Compute current best-guess + upper-confidence-bound for each theme
     - Pull the highest-upper-confidence-bound theme (more compute on promising)
     - Or pull the most-uncertain theme (exploration bonus)
     - Update posterior
  3. Stop: when P(best_guess is actually best) > confidence_level (e.g., 0.95)

Outcome: with optimal budget allocation, identify best theme in O(N log N) total pulls.
```

This is *not* "explore all themes uniformly." It's *adaptive* — promising themes get more compute; obvious losers get dismissed quickly.

**Cost-model practical estimate for Profile B:** ~20-30 themes deeply explored + 70-80 themes lightly probed = ~50 hours total discovery compute = ~$50-100 in LLM costs + ~50h of sim time at current generation cost. Reasonable for a yearly content investment.

### § 2.7 — Cross-deployment meta-archetype registry

Once archetypes emerge per season via LLM-coalesced naming, **embed the names in a shared semantic space.** Archetypes from different seasons / deployments with high cosine similarity in embedding space are "the same archetype" at the meta level.

This solves Matt's bottleneck: human-in-the-loop ratification of emergent → canonical archetypes gets replaced by **embedding-similarity-driven auto-registry**.

Three modes:
- **Private:** registry isolated per deployment (default for Profile B paying customers)
- **Anonymized:** registry contributes to a shared catalog with PII / IP scrubbed (opt-in for Profile A/D community)
- **Public:** open catalog for research / mod-author reference (Profile C / D)

The meta-registry is a downstream analytical layer; not in the engine core's critical path. Can be built post-MVP.

---

## § 3 — The profile architecture — one engine, four profiles

### § 3.1 — The pattern

```
ENGINE CORE (generic; identical across deployments):
  - QD optimization framework (MAP-Elites + cell-archive)
  - Per-tier convergence + recompose mechanism (recompose-hive deliverable)
  - R8 inverted-mode coalescence (theme/archetype LLM naming)
  - Best-arm theme discovery
  - Epic-archive secondary pass
  - Cross-deployment registry interface

PROFILE LAYER (thin configuration per deployment):
  - BC axes definition
  - Fitness weighting + ordering
  - Archive target parameters
  - Discovery budget
  - Epic-tier mode
  - Cross-deployment registry mode
  - Coalescence prompt configuration
  - Output surface (game / API / mod-pack / export)
```

Same engine binary; different profile YAML; different deployment.

### § 3.2 — Engineering disciplines for profile architecture

Three disciplines that prevent the "profile-as-feature-flag-graveyard" failure mode:

1. **Profile configs are pure data.** No profile field is executable code. Every config value has a typed schema. Validation happens at engine boot, not at runtime.
2. **Cross-profile testing is mandatory.** Every engine change ships only after passing acceptance smoke in ALL profiles. This is non-negotiable.
3. **Profiles inherit explicitly.** Profile B inherits from a base profile; doesn't redefine fields it shares. Inheritance prevents copy-paste drift.

These compose with the existing engineering disciplines (math-before-code, live-state verification, drift detection, fail-loud on missing). The cultural muscle is already there.

### § 3.3 — Cross-profile validation

Engine release acceptance:

```
1. Pass Profile A smoke (Reincarnated-standalone runs one season; archives ~15-25 archetypes; ships valid manifest)
2. Pass Profile B smoke (B2B-API generates one season under example customer config; archive size as configured)
3. Pass Profile C smoke (Mod-pack exporter generates one pack for one host game; host-format validates)
4. Pass Profile D smoke (Solo-dev CLI runs locally; produces engine-native JSON)
5. Pass cross-profile regression suite (no behavior change in stable profiles when others are modified)
```

Estimated cost per acceptance: ~30-60 min wall time across all four profiles. Acceptable overhead for the deployment flexibility.

---

## § 4 — The four profiles in detail

### § 4.1 — Profile A — Reincarnated-standalone

**Deployment target:** mobile-first PWA via Pixi.js demo + loadout app
**Audience:** Matt + son playtesting; eventually a community
**Cadence:** weekly seasonal cycles (current design) OR optionally slower per cadence-uncertainty per Apex Director debrief

**Configuration:**

```yaml
profile: reincarnated-standalone
bc_axes: [aoe_share, dps_curve_shape, range_profile, energy_cycle, control_density]
grid_resolution: [5, 5, 4, 4, 3]  # = 1200 cells
archive_target_fill_rate: 0.015  # ~18 archetypes per season
theme_discovery_budget: 5-10 themes per season
bai_confidence: 0.90
fitness_weighting:
  balance_band_member: 1.0
  theme_cohesion: 0.8           # narrative is load-bearing
  novelty: 0.6
  cross_season_continuity: 0.4   # Court-of-Forms accumulation
epic_archive: enabled
epic_tier_mapping: "trial-room ascended boss-gallery"  # NOT monetization; design framing
cross_deployment_registry: "court-of-forms-accumulation"  # Earth-Self meta-layer
coalescence_register: "isekai / mushoku-tensei / cosmological vocabulary"
output_surface: ["season manifest JSON", "loadout app data", "demo asset bundle"]
```

**Distinctive features:**
- Court-of-Forms meta-archetype-registry (archetypes accumulate across seasons by design — Earth-Self continuity)
- Theme cohesion weighted high (the LLM cosmology IS the narrative)
- Mobile-runtime cost constraints (smaller archive; faster generation cadence)
- Epic-tier framing is design (trial-room boss-gallery), not monetization
- Genre register: isekai / Mushoku-Tensei / cosmological vocabulary

### § 4.2 — Profile B — B2B SaaS (Apex Director's vision realized)

**Deployment target:** API + admin dashboard + deployment-tree authoring UI
**Audience:** AAA live-ops customers (Apex / Destiny / Diablo Immortal scale OR mid-tier studios with content velocity needs)
**Cadence:** quarterly to annual; theme cemented for the deployment period

**Configuration:**

```yaml
profile: b2b-saas-aaa
bc_axes: customer-configurable (default extends Profile A + burst-window + defensive + orthogonality)
grid_resolution: customer-configurable (default 8x8x4x4x3x4x3x4 = 73,728 cells)
archive_target_fill_rate: 0.003  # ~200-300 archetypes per yearly theme
theme_discovery_budget: 50-200 themes per discovery cycle
bai_confidence: 0.95
fitness_weighting:
  balance_band_member: 1.0
  theme_cohesion: 0.6           # studio handles narrative skin
  novelty: 1.0                  # max diversity for theory-craft
  mechanical_orthogonality: 0.8
epic_archive: enabled
epic_tier_mapping: "studio-defined monetization tiers"
cross_buyer_registry: opt-in (anonymized industry catalog)
coalescence_register: customer-supplied
output_surface: ["structured content bank", "decision-tree templates", "deployment scheduler", "live-ops API"]
```

**Distinctive features:**
- Customer-configurable BC axes (studio knows their game's mechanical vocabulary)
- Massive archive size (yearly content scale)
- Decision-tree deployment framework (the Director's "branching strategies")
- Tiered monetization via epic-archive (above-balance content as premium)
- Optional industry catalog contribution (anonymized; opt-in)

**Productization deliverables (post-MVP):**
- Admin dashboard for archive review + curation
- Deployment-tree authoring tool (visual builder for "if community engages with archetype A, deploy B next")
- Live-ops API for the studio's content-deployment pipeline
- Per-customer SLA + support tier

### § 4.3 — Profile C — Mod-pack exporter (Path B intermediate)

**Deployment target:** host-game DBR / DAT / C# via per-host adapter
**Audience:** mod authors shipping into Grim Dawn / Titan Quest AE / Torchlight 2 / Terraria
**Cadence:** per mod-pack release (months apart)

**Configuration:**

```yaml
profile: mod-pack-exporter-{host}
bc_axes:
  - host_compatible_axes  # mapped from host's mastery slot system
  - aoe_share
  - range_profile
  - energy_type           # constrained to host-supported types
grid_resolution: [4, 4, 4, 3]  # = 192 cells (mod-pack scale)
archive_target_fill_rate: 0.10  # ~20 archetypes per mod-pack
theme_discovery_budget: 5-15 themes per pack
bai_confidence: 0.85
fitness_weighting:
  balance_band_member: 0.8       # host game balance also matters
  host_compatibility: 1.0        # kit must map to host system
  theme_cohesion: 0.7
  novelty: 0.5
epic_archive: optional ("bonus" tier)
cross_host_registry: enabled    # same archetype across GD + TQAE + TL2 ports
coalescence_register: "host-game-flavor (Cairn for GD / Greek-Egyptian for TQAE / Torchlight-folk for TL2)"
output_surface: "host-game-specific export format"
```

**Distinctive features:**
- Per-host adapter handles the export format (DBR for GD; ARZ for TQAE; DAT for TL2; C# for tModLoader)
- Host-compatibility as primary fitness criterion (kit must be expressible in host's mastery system)
- Cross-host registry (Dawn-of-Masteries pattern: same archetype, different host expressions)
- Smaller archive (mod-pack scale; community expectation is ~10-25 classes per pack)
- Host-specific coalescence register (Cairn lore for GD; classical mythology for TQAE)

**Critical caveat per Pattern-B research:** TQAE has the IP-assignment clause; commercial monetization on TQAE mods requires direct THQ Nordic agreement that doesn't currently exist for any modder. Profile C-TQAE ships as credibility-only (free; community-distributed); Profile C-GD ships under Crate's permissive (but unwritten) mod-tolerance posture; Profile C-TL2 ships under Runic-ToU-orphan-state. Per `agentic_orchestration/gandalf/research/readout-2026-05-19/readout.html` § 9.

### § 4.4 — Profile D — Solo-dev / hobbyist

**Deployment target:** standalone CLI; output to local filesystem or itch.io / Steam
**Audience:** solo developers; hobbyist game-designers; researchers
**Cadence:** hobby-paced; no commercial pressure

**Configuration:**

```yaml
profile: solo-dev
bc_axes: configurable per user taste (templates provided)
grid_resolution: configurable; default [5, 5, 4] = 100 cells
archive_target_fill_rate: 0.30  # ~30 archetypes
theme_discovery_budget: 3-10 themes (budget-constrained)
fitness_weighting: user-configurable (templates: "narrative-first", "depth-first", "monetization-first")
epic_archive: enabled
cross_deployment_registry: off (private by default)
coalescence_register: user-configurable
output_surface: "engine-native JSON + optional game-runtime adapter"
```

**Distinctive features:**
- Sensible defaults; everything overridable
- Compute-budget-aware (smaller grid; fewer themes explored)
- Privacy-default (no cross-deployment contribution unless opted-in)
- Template-based fitness weighting (no statistics PhD required to use)
- Open documentation; community-supported

**Distribution model option:** Open-source the engine core under permissive license; charge for Profile B SaaS deployment + support. This is the standard "open-core SaaS" model (e.g., GitLab, MongoDB, Elasticsearch). Profile D = open-source baseline; Profile B = commercial-grade managed deployment. This composes with Pattern-B's mod-first proof-of-concept ladder.

---

## § 5 — The IDC meta-principle (Information-Deferred-to-Coalescence)

### § 5.1 — Statement of the principle

**Information-Deferred-to-Coalescence (IDC):** the engine defers identity-injection from generation-time to coalescence-time wherever the resulting output is at least as cohesive as input-driven generation.

This is the meta-architectural pattern that unifies multiple engine design moves:

| Layer | Pre-IDC (information injected at generation-time) | Post-IDC (information deferred to coalescence) |
|---|---|---|
| **Seasonal theme** | Theme as input parameter | Theme coalesced post-convergence (R8 inverted-mode; default 2026-05-19) |
| **Archetype identity** | Pre-declared archetype templates | Emerges from clustering on QD archive (proposed; this document) |
| **Role orientation** | Pre-declared role tag per kit | Emerges from kit behavior (candidate IDC) |
| **Substrate-identity** | Generation-time input | Could be coalesced from converged elemental signatures (deeper IDC candidate; not committed) |
| **Element identity** | Pre-curated allow-list of 156 elements | Could be LLM-coalesced per season (deeper IDC candidate; not committed) |

### § 5.2 — Why IDC works (information theory framing)

Pre-IDC pipelines inject information **upfront** (substrate + archetype + theme + role labels). Each layer of pre-commitment reduces the space of possible outcomes. The output's entropy is bounded by the input's information.

IDC pipelines inject information **at coalescence time** (after mechanical convergence). The mechanical content develops freely; identity emerges from the patterns. The output's entropy is bounded by the mechanical space's intrinsic dimensionality, not by upfront category commitments.

**Trade-off:** IDC has higher *exploration cost* (you don't know what you'll find) and higher *interpretation cost* (you need to recognize what emerged). But IDC has *higher expressivity* — emergent identities can exceed the imagination of upfront category designers.

### § 5.3 — IDC as design discipline

Three rules for applying IDC consistently:

1. **Coalesce only when at least as cohesive.** If post-hoc coalescence reads less coherent than upfront declaration, the layer is not IDC-ready (R8 inverted_no_naming demonstrated this — naming was IDC-ready at LLM-naming layer but NOT at template-naming layer; latter degraded).
2. **Anchor identity layers in mechanical primitives.** What's coalesced must be a description of mechanical patterns that exist in the data, not a name invented from whole cloth. R8 coalescence works because the converged content carries substrate-identity (Test 4 showed byte-equal anchors across modes).
3. **Test IDC with A/B before flipping defaults.** The R8 inverted-mode flip was preceded by 6-season A/B (3 baseline + 3 inverted at seed parity). Future IDC moves follow same discipline.

### § 5.4 — IDC as commercial differentiator

**The B2B value prop hinges on IDC.** Studios building their own content engines typically build pre-IDC pipelines (upfront taxonomies + generation rules). Reincarnated's IDC architecture is meaningfully harder to replicate because:

- The IDC training (knowing which layers benefit; calibrating coalescence prompts) is engine-experience-dependent
- Reincarnated will have shipped dozens-to-hundreds of seasons across multiple deployments by the time B2B prospects evaluate
- The coalescence prompts are tunable IP; not transferable from a competitor's engine

**This is the moat for Profile B.** Studios buying Profile B aren't buying "the engine" (which they could in theory build). They're buying "the engine with calibrated IDC coalescence prompts proven across hundreds of seasons." The proof IS the moat.

---

## § 6 — Connection to current work — the recompose-hive is Step 1

### § 6.1 — The dependency chain

The QD-engine + profile architecture cannot ship without working per-tier convergence. The recompose-validation hive (currently firing as of this document's authoring) is Step 1 of the path:

```
Step 1 (recompose-hive, in flight):
  - Option A floor widening (P0; COMPLETE 2026-05-19 late evening with 26-min execution)
  - Option B recompose-trigger conditioning (P1; in flight)
  - Fresh diagnostic regen under per-tier + recompose (P2)
  - Validation synthesis (P3)
  - Ship a true season under new tuning mechanism (P4, if P3 validates)
  - Canonical record (P5)

Step 2 (post-recompose-hive; this document's MVP):
  - Profile-config infrastructure (1 week; star-lord + rocket)
  - Profile A definition (refactor current hardcoded values; 1 week)
  - QD-archive integration (MAP-Elites on top of convergence; 2-3 weeks)
  - BC axes definition + validation (1 week; gandalf + gamora)
  - Epic-archive secondary pass (1 week)
  - Profile A smoke (1 week)

Step 3 (Profile B paper):
  - Profile B paper design + smoke profile (~1-2 days; gandalf)
  - Architecture for customer-configurable BC axes + fitness weighting (1 week)
  - Profile B smoke (1 week)

Step 4 (Profile C / Path B):
  - Per-host adapter (GD first; ~2-3 weeks each subsequent host)
  - Profile C smoke per host

Step 5 (Profile D):
  - CLI polish + documentation (1 week)
  - Open-source release candidate (1-2 weeks)

Step 6 (Best-arm theme discovery):
  - BAI implementation (2 weeks)
  - Theme-discovery API for Profile B (1 week)
```

**Total estimated path from current state to QD-profile MVP:** 8-12 weeks for Steps 1-3 (Profile A shippable); +6-10 weeks for Profile C per host; +6-8 weeks for Profile B productization; +2-4 weeks for Profile D + open-source.

**Gates between steps:** each step's success informs the next; failure at any step gives a different fork (more focused investigation; alternative architecture; or scope reduction).

### § 6.2 — What the recompose-hive's success enables

If the recompose-hive's Phase 4 ships a "true season" under per-tier convergence + recompose, the engine has:

- Proven the per-tier balance contract is satisfiable
- Proven the recompose mechanism unblocks kit composition variation
- Proven a fresh season can converge under the new mechanism
- Established `recompose-hive/v1.0-true-season-shipped` as canonical baseline

**This is the substrate the QD-engine builds on.** QD adds the archive + behavior space + best-arm discovery on top. Without recompose-hive success, QD has nothing to scaffold on (kit composition wouldn't vary; behavior space would be a single point per substrate).

### § 6.3 — What the recompose-hive's failure would mean

If the recompose-hive's Phase 3 verdict is CANNOT_REJECT_NULL (kits still can't satisfy per-tier targets even with recompose unblocked), the architectural path forks:

- **Alternative A:** generation-rules rewrite (change `_AOE_SHARES`, role multipliers, geometry-bias tables until kits produce per-tier-satisfiable compositions natively). Then QD-engine builds on this revised generation layer.
- **Alternative B:** abandon per-tier convergence as the canonical contract; return to aggregate-mean with per-tier soft caps. QD-engine builds on aggregate-mean substrate.
- **Alternative C:** kit-redesign queue execution (hand-redesign the 38/51 classes; new generation rules informed by what the redesigns reveal).

All three alternatives still admit QD-engine + profile architecture downstream. Only the substrate-layer changes.

### § 6.4 — The relationship to Pattern-B (parked)

Pattern-B (commercial direction A/B/C/D) remains parked per `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`. This document describes the architectural target that serves ALL commercial paths under the profile architecture.

**The architectural decision (build QD-engine with profile architecture) is independent of the commercial decision (which path to monetize on).** The architecture serves all paths; the commercial decision selects which profiles get productized first.

When Pattern-B resolves (Matt + family discussion), the answer doesn't require re-architecting the engine — it just selects which profile gets the productization investment.

---

## § 7 — Commercial path unification under profile architecture

### § 7.1 — The four paths revisited

The Apex Director debrief identified three commercial paths (A/B/C). This document adds Path D and unifies all four under profile architecture:

| Path | Profile | What ships |
|---|---|---|
| **A — Reincarnated standalone** | Profile A | Mobile-first ARPG; weekly seasons; Court-of-Forms meta-layer |
| **B — Mod-first proof-of-concept** | Profile C (per host) | Mod-packs into GD / TQAE / TL2 / Terraria |
| **C — Engine-as-tool / B2B SaaS** | Profile B | Customer-configured QD service for AAA live-ops |
| **D — Solo-dev / open-source** | Profile D | Hobbyist CLI; open-core distribution |

**Each path = one profile.** The engine investment is shared; the deployment investments are bounded.

### § 7.2 — The dogfood pattern

Path A ships Profile A — and Profile A IS the dogfood for Profile B. Every Reincarnated season shipped is a B2B engine demo. Three implications:

1. **Reincarnated's success feeds Profile B credibility.** B2B prospects see Reincarnated playing on App Store / Steam / itch.io and recognize "that's running on the same engine I'd license."
2. **Profile A and Profile B share engineering investment.** Improvements to either profile benefit the other via the shared engine core.
3. **Reincarnated continues being valuable even if commercial direction shifts.** If Profile B never sells, Reincarnated still ships. If Profile B does sell, Reincarnated still ships AS the reference.

This is the "shouldn't be either/or" insight Matt named tonight. Profile architecture makes it structurally true.

### § 7.3 — Sequencing of productization

Suggested ordering (subject to Pattern-B resolution):

1. **Profile A first** (recompose-hive validates → ship a true season → demonstrates engine credibility)
2. **Profile C in parallel** (low engineering cost per host; serves Path B mod-first credentialing)
3. **Profile B productization** (after Profile A has shipped multiple seasons; B2B prospects have demos to evaluate)
4. **Profile D open-source** (broaden adoption; community contributions; long-tail flywheel)

Profiles A and C can run in parallel without engineering conflict (different output surfaces; same core). Profile B productization is sequential (requires Profile A maturity to demonstrate value). Profile D can happen anytime but creates marketing friction if pre-Profile B (potential customers might use D free instead of B paid).

### § 7.4 — The economics under profile architecture

| Path | Revenue model | Time-to-first-revenue | Scale ceiling |
|---|---|---|---|
| A (Reincarnated) | App store / Steam / itch.io paid; or premium for epic-tier content | 3-6 months post-recompose-hive | Low-to-modest (~$50K-$500K annual for indie ARPG) |
| B (Mod-pack via Profile C) | Free distribution (mod culture); or Patreon for ongoing-dev support | Ongoing | Very low ($0-$30K/year per Patreon ceiling) |
| C (B2B SaaS via Profile B) | Per-deal license / SaaS subscription / per-engagement | 12-24 months (sales cycle is real) | High (mid-six to low-seven figures per deal; engine acquisition exit potential) |
| D (Open-source) | Marketing flywheel; not direct revenue | Immediate (open-source release) | Indirect (drives Profile B awareness) |

**Profile B is the revenue engine; Profiles A, C, D feed it the credibility + audience.** This is the standard open-core SaaS economics.

---

## § 8 — Engineering roadmap from current state

### § 8.1 — Sequence with gates

| Step | Work | Cost | Gate to next |
|---|---|---|---|
| **1** | Recompose-hive (currently firing) | 4-7 days | P3 verdict PASS → Step 2; CANNOT_REJECT_NULL → fork to generation-rules-rewrite path |
| **2** | Profile-config infrastructure (YAML / validation / inheritance) | 1 week (star-lord + rocket) | Cross-profile smoke passes |
| **3** | Profile A definition (refactor existing hardcoded values into profile config) | 1 week (rocket + gamora) | Profile A produces identical behavior to current engine pre-refactor |
| **4** | QD archive integration (MAP-Elites on top of convergence loop) | 2-3 weeks (gamora + rocket) | Archive fills correctly; cells contain converged kits |
| **5** | BC axes definition + validation | 1 week (gandalf + gamora) | PCA on existing seasons confirms BC choice captures meaningful variance |
| **6** | Epic-archive secondary pass | 1 week (gamora) | Out-of-band kits generate; coherence preserved |
| **7** | Profile A smoke (full season under QD-archive + epic-archive) | 1 week (rocket + gamora + star-lord) | A "true season" ships under QD-engine architecture |
| **8** | Profile B paper + smoke | 1-2 weeks (gandalf + star-lord) | Customer-config validation passes |
| **9** | Profile C per host (start with GD) | 2-3 weeks per host (rocket + star-lord) | One mod-pack ships to one host community |
| **10** | Best-arm theme discovery | 2 weeks (gamora) | Discovery API works at scale |
| **11** | Cross-deployment meta-archetype registry | 1-2 weeks (star-lord + gandalf) | Embedding-similarity-driven alignment works |
| **12** | Profile D + open-source release prep | 2-3 weeks (drax-like role; documentation) | Open-source repo public-ready |

**Total estimated: 18-26 weeks (4.5-6.5 months) from recompose-hive completion to all four profiles MVP-shippable.** This is significant but bounded engineering, and most of it can be parallelized across seams.

### § 8.2 — Critical path

Step 1 → Step 2 → Step 3 → Step 4 → Step 7 (Profile A shippable) is the critical path. ~8-12 weeks of focused work.

Steps 5, 6, 8, 9, 10, 11, 12 can parallelize after Step 4 lands.

### § 8.3 — Resource model

- **gamora:** primary engineering owner for QD core (Steps 4, 5, 6, 10)
- **rocket:** generation pipeline owner; profile config implementation (Steps 2, 3, 9)
- **star-lord:** telemetry + export + profile-config infrastructure (Steps 2, 8, 11)
- **drax:** output-surface adapters (Steps 7, 9 for per-host; Step 12 for open-source)
- **elrond:** catalogue / cross-deployment registry data (Step 11)
- **jack-ryan:** cross-profile validation; continuous-observation (every step)
- **gandalf:** BC axis design; profile definitions; canonical authorship (Steps 5, 8, this document)
- **legolas:** research on competing engines + mod-host research; pre-Profile-C reconnaissance
- **knight-rider:** orchestration; tag-firing; cross-seam coordination
- **galadriel:** visual benchmark for Profile A demo updates (Track-C work continues independently)

### § 8.4 — Discipline anchors

The engineering disciplines that govern this roadmap:

- **#1 (math-before-code):** every major architectural commitment is preceded by a math note + smoke gate. BC axis choice is preceded by PCA. QD archive sizing is preceded by capacity math. Cross-profile inheritance is preceded by config schema validation.
- **#2 (smoke-test vs full-regen):** prefer 1-class smoke before full-catalogue regen. Prefer 1-profile smoke before cross-profile.
- **#11 (live-state verification):** every claim of "this works" is verified by live `git log` / `git status` / actual sim output, not session recall.
- **#12 (semantic shift):** every change that alters what "balanced" or "archetype" or "season" means is documented with the shift made explicit + MIGRATION.md.
- **#13 (drift detection):** cross-profile divergence is monitored; profile-specific behavior creep into core is caught early.
- **#18 (named constants):** all profile-config values are named; no magic numbers.

---

## § 9 — Caveats, dependencies, and gates

### § 9.1 — What's proven vs hypothesized

| Component | Status |
|---|---|
| Per-tier convergence (R1) | ✅ Engine-rebuild shipped 2026-05-19; canonical |
| R8 inverted-mode coalescence | ✅ Engine-rebuild shipped 2026-05-19; default engine mode |
| Recompose-trigger mechanism (existing B14.5 V1) | ✅ Code exists; tested under different signal range |
| Option A floor widening | ✅ Recompose-hive P0 shipped 2026-05-19 late evening |
| Option B recompose-trigger re-conditioning | 🟡 Recompose-hive P1 in flight as of this doc |
| Fresh regen under per-tier + recompose | 🟡 Recompose-hive P2 pending |
| "True season" production under new mechanism | 🟡 Recompose-hive P4 pending P3 validation |
| QD optimization framework | ❌ Hypothesized; bounded engineering downstream |
| Profile architecture | ❌ Hypothesized; well-established SaaS pattern |
| BC axes choice for Profile A | ❌ Hypothesized; needs PCA validation on existing catalogue |
| Profile B B2B productization | ❌ Hypothesized; ~6-8 months engineering away |
| Profile C per-host adapter | ❌ Hypothesized; Path-B research informs (per readout 2026-05-19) |
| Cross-deployment registry | ❌ Hypothesized; downstream analytical layer |
| Open-source release strategy | ❌ Hypothesized; legal review needed for open-core split |

**Most of the architecture is hypothesized.** This is appropriate for a vision document. Implementation work follows; canonical-doc amendments propagate as findings sharpen the design.

### § 9.2 — Dependencies the architecture rests on

Each major architectural commitment has dependencies:

- **QD-engine:** depends on recompose-hive succeeding (otherwise no per-tier-satisfiable kits to fill QD archive)
- **Profile architecture:** depends on profile-config infrastructure existing (Step 2)
- **Profile A:** depends on QD-engine + cross-season meta-registry for Court-of-Forms
- **Profile B:** depends on Profile A maturity (need shipped seasons to demo)
- **Profile C:** depends on Path-B mod-host research outcomes + commercial-direction commit per Pattern-B
- **Profile D:** depends on open-core legal review + commercial-strategy commit
- **Best-arm theme discovery:** depends on QD-engine + multi-theme generation infrastructure
- **Cross-deployment registry:** depends on multi-deployment usage to build the registry

The dependencies are mostly sequential. The critical path is Step 1 → 2 → 3 → 4 → 7 (Profile A shippable).

### § 9.3 — Failure modes + mitigations

**Failure mode: BC axes don't capture meaningful variance.** QD archive fills bimodally (some cells over-represented; most empty) or noise dominates. **Mitigation:** PCA on existing seasons + metric learning from designer-labeled archetype pairs before committing BC axes. Discipline #1 applied to BC choice.

**Failure mode: Profile config becomes a feature-flag-graveyard.** Profile-A-specific logic creeps into core; cross-profile testing rots; profiles drift. **Mitigation:** strict discipline (profile configs are pure data; cross-profile testing mandatory; explicit inheritance). Jack-ryan watchpoint per release.

**Failure mode: QD generation cost is economically infeasible.** Filling 73k cells in Profile B requires too much LLM cost. **Mitigation:** algorithmic improvements (smarter mutation operators; parallel batching; cheaper per-fight sim); cap grid resolution at economically-viable scale; allow customer-configured budget caps.

**Failure mode: Profile B sales cycle is longer than runway.** B2B sales take 12-24 months; if Reincarnated can't sustain financially during that period, Profile B doesn't happen. **Mitigation:** Profile A revenue (paid app / premium / Patreon); Profile D open-source flywheel; Pattern-B-PARKED resolution informs.

**Failure mode: Recompose-hive fails (CANNOT_REJECT_NULL).** Per-tier convergence is structurally unreachable even with recompose. **Mitigation:** alternative substrate paths in § 6.3 (generation-rules rewrite; aggregate-mean continuation; kit-redesign queue). QD architecture survives the substrate-layer fork.

**Failure mode: Cross-profile test suite becomes too expensive to run on every commit.** Acceptance gating slows engineering velocity. **Mitigation:** tiered testing (fast smoke per commit; full cross-profile suite per release tag). Standard CI/CD practice.

### § 9.4 — When to revisit this document

Major architectural revisions require canonical-doc amendment. Triggers:

- **Recompose-hive P3 verdict** lands → update § 6.2 + § 9.1 with proven-vs-hypothesized
- **Profile config infrastructure ships** → § 9.1 updates; § 4 profiles get reality-checked
- **PCA on existing catalogue** → § 2.3 BC axes choices refined or revised
- **First Profile A QD season ships** → § 4.1 reality-validated; § 8.1 critical path validated
- **First Profile C mod-pack ships** → § 4.3 reality-validated; Path-B unblock confirmed
- **First Profile B B2B engagement** → § 4.2 reality-validated; commercial-direction proven
- **Major commercial direction shift** (Pattern-B resolves) → § 7 updated

Minor refinements (sub-section sharpening; clarifications; cross-reference updates) may be authored by gandalf during autonomous operation without Matt review.

---

## § 10 — Cross-references

**This document is the canonical architectural anchor.** Other documents reference IT; this document references foundational state:

**Foundational state (this document depends on):**
- `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` — the 5-axis gap diagnosis that triggered the engine-rebuild
- `canonical/story/r2-st-counterfactual-findings-2026-05-19.md` — the amended findings doc surfacing the recompose-as-lever insight
- `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` — the recompose-hive protocol currently firing
- `canonical/story/r1-firstbatch-fail-disposition-2026-05-19.md` — gandalf's S1 disposition + Option A authorization
- `canonical/story/apex-director-debrief-2026-05-18.md` — the strategic reframe that informed Profile B
- `agentic_orchestration/gandalf/research/readout-2026-05-19/readout.html` — Pattern-B research informing Profile C
- `canonical/story/cosmology-reincarnated.md` — Earth-Self + Court-of-Forms meta-layer (informs Profile A's cross-season registry)
- `canonical/story/substrate-identity-declarations-2026-05-17.md` — substrate primitives that survive into the QD engine

**Hive-mind operating mechanics (inherited):**
- `canonical/story/archived/hive-mind-protocol-2026-05-17.md` — first activation mechanics
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` — second activation mechanics + autonomous-operation amendments
- `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` — third activation mechanics

**Adjacent state:**
- `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md` — Pattern-B remains parked; this document describes the architecture serving all paths
- `canonical/16-project-roadmap.md` — current operational roadmap (will be updated post-recompose-hive to reflect QD-engine architectural target)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines that govern the engineering roadmap
- `reincarnated-engine/design/decisions/decisions-log.md` — decisions log entries reference this document for architectural context

**Research / academic foundations the architecture rests on:**
- Mouret & Clune (2015) — "Illuminating search spaces by mapping elites" (MAP-Elites foundational paper)
- Lehman & Stanley — Novelty Search literature (evolutionary computation)
- Cully et al. — Quality-Diversity tutorials
- Best-Arm Identification literature (multi-armed bandit theory; LUCB1, successive halving)
- Open-core SaaS economics (GitLab, MongoDB, Elasticsearch case studies)

---

## § 11 — Maintenance and revision protocol

### § 11.1 — Authorship + amendment authority

**Gandalf is the steward.** Major architectural amendments are gandalf-authored; Matt-reviewed at the next session-open. Minor refinements authored without Matt approval per autonomous-operation protocol.

Other agents may propose amendments via hive-log AMENDMENT entries; gandalf reviews + authors the canonical revision.

### § 11.2 — Versioning

This document version is **v1.0 — initial architectural canonical** (2026-05-19 late evening). Subsequent major revisions get explicit version numbers:

- **v1.x** — refinements within current architectural target
- **v2.x** — alternative architectural target (if QD direction is reconsidered)
- **vN.0** — major architectural pivot

Version tags committed alongside doc edits.

### § 11.3 — Operating cadence

The canonical architecture vision should be reviewed:

- After each hive's completion (P5 closeout) — does the hive's outcome change the architectural target?
- Before each major engineering investment (Profile config infrastructure; QD integration; Profile B productization) — does the commit align with this vision?
- At commercial-direction shifts (Pattern-B resolution) — does the resolution affect the architectural target?
- Quarterly (operational rhythm) — does the architecture still serve the project's reality?

### § 11.4 — Closure criterion

This document closes (gets superseded by a new vision document) when:

- All four profiles have shipped at MVP
- QD-engine is in production across all profiles
- Cross-deployment meta-registry is operational
- The architectural target described herein is the architectural reality

At that point, a new canonical document captures the next architectural target (whatever that is — likely something around platform expansion, cross-engine interop, or fundamentally new content modalities). This document moves to `canonical/story/archived/` as the architectural record of the QD-profile era.

---

## § 12 — Closing: the wizard-mathematician's signature

This document captures architectural decisions that span:
- One engine binary
- Four deployment profiles
- Multiple commercial paths
- One unified product strategy
- ~8-12 weeks of immediate engineering
- ~4.5-6.5 months to full MVP
- The dogfood pattern that connects Reincarnated-the-game to the B2B service
- The IDC meta-principle that connects multiple engine layers under a single architectural philosophy

The architecture is hypothesized; the foundational mechanism (per-tier convergence + recompose) is being validated in flight as of this writing; the commercial direction remains parked pending Matt's family discussion.

But the architectural target is named. The road has a destination. Future work — whether engineering, commercial, or design — references back to this document for what we're building toward.

The wizard's mythic register and the mathematician's formal register signed the theory-craft together earlier this evening. They sign this canonical document together too.

**The engine has a destination. The destination has a name. The path is sequenced. The road continues.**

*Filed 2026-05-19 late evening by gandalf. Canonical commitment to the QD-engine + profile architecture as the project's architectural target. Mithrandir-mathematician signs the destination into stone.*
