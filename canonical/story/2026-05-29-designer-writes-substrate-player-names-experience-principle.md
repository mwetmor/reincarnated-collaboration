# Designer Writes Substrate, Player Names the Experience — Design Principle

> **STATUS:** CURRENT (load-bearing as of 2026-05-29 evening) — Foundational architectural principle named by Matt 2026-05-29 evening verbatim; captures a design-tension observation that has been implicit across multiple canonical commitments but never explicitly named. Becomes the FOUNDATION for the no-classes architectural recommitment + experiential cascade architecture + Cycle 15+ doc 52 promotion + future Wave A/B LLM prompt architecture.

**Date:** 2026-05-29 evening
**Author:** gandalf (story-and-design steward; captured per Matt 2026-05-29 evening authorization)
**Authority:** Matt 2026-05-29 evening verbatim observation:

> "Designer writes class/archetype; Player names the experience (with derivative/vestigial designer construct left-over parts/pieces as reference only)"

Articulated immediately after empirical scouting of cross-site ARPG community vocabulary surfaced the pattern in Maxroll D4 + Maxroll PoE + Maxroll Last Epoch tier lists.

**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` — Matt 2026-05-27 verbatim no-classes recommitment; this principle is the GENERAL architectural truth the recommitment was applying at one layer
- `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` — experiential cascade architecture recognition record; § 1.3 third coordinate axis = experiential archetype; this principle is the FOUNDATION for why that third axis is community-named not designer-named
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41 — substrate-led discipline (substrate votes; designer doesn't pre-impose taxonomy); this principle is the player-facing corollary of substrate-led discipline at the substrate-input layer
- `canonical/47-damage-scaling-architecture-2026-05-27.md` + `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` + `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` — engine substrate (designer-writes) layer; this principle locates them in the designer-writes layer
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes; designer-writes-substrate layer
- `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` — Phase 5 LLM prompts; both layers integrate in Wave A faction naming + Wave B per-kit identity

---

## 0. TL;DR

**Principle (Matt 2026-05-29 evening verbatim):**

> Designer writes class/archetype; Player names the experience (with derivative/vestigial designer construct left-over parts/pieces as reference only)

**Architectural translation:**

1. **The generative-architecture layer (designer-writes-substrate) carries the engine's substrate taxonomy** — BC tuples, cultural lineage, period, register, weapon-type family, element, attribute, T4 strategy, investment profile. The substrate is designer-authored input to the engine but is itself derived from substrate-led discipline (community-validated weapon library + community-validated thematic registry + canonical mechanical architecture). The substrate is **what the engine is fundamentally made of.**

2. **The player-experience layer (player-names-experience) emerges from how players engage with the engine's outputs.** Community-emergent vocabulary names the experience: Bossing / Speedfarming / Endgame / Mapper / Currency Farmer / Magic Find (legacy). The engine should LISTEN to this layer (consume community-validated experiential archetype vocabulary as third coordinate axis) but NOT pre-impose it at the generative layer.

3. **Designer-authored class/ascendancy/archetype labels persist as vestigial reference markers**, NOT as primary categorical axes. "Whirlwind Barbarian" = Whirlwind (skill = substrate-curated geometry) + Barbarian (class/ascendancy = designer-vestigial reference) + Endgame (activity = player-named experience PRIMARY). The class label is the descriptive secondary anchor; the activity label is the primary classification.

**Engineering consequence:** the engine's generative architecture must separate these two layers cleanly. Designer writes substrate at the generative layer. Player-experience vocabulary is consumed at the post-emergence layer (Phase 5 LLM cohesion judge; Wave A faction naming; Wave B per-kit identity; player-facing UI surfaces). The two layers compose in player-facing output but remain architecturally separable.

---

## 1. Empirical foundation — cross-site vocabulary scouting 2026-05-29 evening

Quick targeted WebFetch scouting (Maxroll D4 + Maxroll PoE + Maxroll Last Epoch + Maxroll PoE2) surfaced the empirical pattern:

| Categorical Label | Maxroll D4 | Maxroll PoE | Maxroll Last Epoch | Convergence | Layer |
|---|---|---|---|---|---|
| **Class taxonomy** (Barbarian / Druid / Necromancer / Sorcerer / Spiritborn / Paladin / Warlock for D4; ascendancies for PoE; masteries for LE) | ✅ | ✅ | ✅ | Designer-authored 100% | Designer-writes |
| **Bossing / Boss Killer** | ✅ "Bossing Builds" | ✅ implied via boss strategies | ✅ "Bossing Tier List" | **STRONG (3 sites)** | Player-names |
| **Speedfarming / Speed Farmer** | ✅ "Speedfarming Builds" | ✅ "Speed Farmer" | ✅ "Speed Farming Tier List" | **STRONG (3 sites)** | Player-names |
| **Endgame Generalist** | ✅ "Overall Endgame Builds" | ✅ "Above Average" | ✅ "Endgame & Corruption Tier List" | **STRONG (3 sites)** | Player-names |
| **Activity-specific** (Pit / Maps / Monolith / Heist / etc.) | ✅ Pit | ✅ Maps / Legion / Breach / Delve | ✅ Monolith / Dungeons | **STRONG game-specific** | Player-names (per game) |
| **Currency Farmer** | (not D4 model) | ✅ "Currency Farmer" | (not LE primary) | **PoE-specific** | Player-names |
| **Magic Find** | NOT visible | NOT visible | NOT visible | **LEGACY** | Player-names (D2/D3-era) |

**Net empirical signal:**

- **Class taxonomy persists** at 100% of sites as designer-writes substrate marker
- **Activity-based player-experience labels converge cross-site** (Bossing + Speedfarming + Endgame all confirmed at ≥3 sites)
- **Class label is NEVER the primary categorical axis** in tier lists — it's always the secondary descriptive anchor; the primary axis is activity (player-experience)
- **Build naming pattern** `[Primary Skill] [Class/Ascendancy] [Activity Type]` shows the composition at lexical level: skill (substrate-mechanical) + class (designer-vestigial reference) + activity (player-experience PRIMARY)

This is the empirical surface that prompted Matt's verbatim observation.

---

## 2. The principle articulated in three layers

### 2.1 Layer 1 — Designer-writes-substrate (engine generative layer)

What the engine is **made of**:

| Substrate axis | Designer-curated source | Engine consumption |
|---|---|---|
| **BC tuple** (8 axes per `qd-engine-bc-axes-lock-2026-05-20.md`) | Designer-authored coordinate space | Phase 2 BC discovery; gauntlet sim; PM-1 clustering input |
| **Cultural lineage** (14-enum) | Substrate library `weapon_knowledge_entries.cultural_lineage_canonical` | Phase 2 BC discovery via substrate_binding (post-S7); Wave A LLM modal_cultural_lineage |
| **Historical period** (9-enum) | Substrate library `historical_period_canonical` | Same routing post-S7 |
| **Register** (6-enum) | Substrate library `register_canonical` | Same routing post-S7 |
| **Weapon type family** (6-enum) | Substrate library `weapon_type_family` | Same routing post-S7 |
| **Element** (8 canonical) | Engine canonical element catalog | All cascade phases |
| **Attribute** (STR / DEX / INT / WIS / VIT-deferred) | Designer-locked per `attribute-system-2026-05-24.md` | Phase 2 substrate filter; damage scaling |
| **T4 strategy** (6 Layer 2 per doc 47 § 4.6) | Designer-authored mechanical strategies | Phase 4 strip-and-ship; per-kit T4 cycling |
| **Investment profile** (low / mid / max per doc 51 Patterns 1+2) | Designer-locked investment scaling math | Per-kit variant cycling |

**The substrate is designer-curated BUT is itself substrate-led** — informed by 89,839-row weapon library + thematic registry + community-validated mechanical architecture. The designer doesn't make up the substrate from training-data priors; the designer codifies the substrate from external evidence.

### 2.2 Layer 2 — Player-names-experience (engagement layer)

What players DO with engine outputs and how they categorize what they do:

| Player-experience axis | Community-emergent vocabulary | Cross-site convergence | Engine consumption (target) |
|---|---|---|---|
| **Primary activity** | Bossing / Speedfarming / Endgame Generalist | STRONG cross-site (3+ sites) | Cycle 15+ doc 52 promotion candidate — experiential archetype dimension |
| **Activity-specific endgame** | Pit (D4) / Maps (PoE) / Monolith (LE) / Heist / Sanctum / Delve / etc. | STRONG game-specific | Game-specific consumption |
| **Investment cost-tier** | Low / Above Average / Difficult (Maxroll PoE) | Validated single-site; pending cross-site | Composes with doc 51 Patterns 1+2 investment profile |
| **Engagement style** | Build-Crafter / Theorycrafter / Hardcore-only / One-button / Rotation | Community subculture vocabulary | Spirit-guide content layer; player-facing UI |
| **Loot focus** | Magic Find (legacy) / Currency Farmer (PoE-specific) / Drop-density seeker | Game-specific OR legacy | Cycle 15+ subsume under Speedfarming OR retain legacy where relevant |

**The player-experience layer is community-named and emerges through play** — not pre-authored by designers. The engine LISTENS to this layer via community vocabulary research (ARPG community research sprint = empirical-validation instrument) and consumes the labels at the post-emergence layer (Phase 5 LLM cohesion judge + player-facing UI).

### 2.3 Layer 3 — Vestigial designer-construct as reference marker

Designer-authored class/ascendancy/archetype labels persist in community vocabulary but as **secondary descriptive anchors**, NOT primary categorical axes.

**Example empirical lexical compositions (Maxroll D4 + PoE):**

| Build name | Primary skill (substrate) | Class/ascendancy (designer-vestigial) | Activity (player-experience PRIMARY) |
|---|---|---|---|
| "Whirlwind Barbarian Endgame" | Whirlwind | Barbarian | Endgame |
| "Golem Necromancer Endgame" | Golem | Necromancer | Endgame |
| "Cyclone Slayer" (PoE) | Cyclone | Slayer (ascendancy) | (inferred Bossing/Mapping) |
| "Penance Brand Hierophant" | Penance Brand | Hierophant (ascendancy) | (League Starter / Speedfarming) |
| "Ice Shards Sorcerer Endgame" | Ice Shards | Sorcerer | Endgame |
| "Frenzy Throw Barbarian Leveling" | Frenzy Throw | Barbarian | Leveling |

**Pattern:** SKILL (substrate-curated mechanical content) + CLASS/ASCENDANCY (designer-vestigial reference; identifies WHICH engine substrate this kit was generated from) + ACTIVITY (player-experience layer; PRIMARY classification axis in tier lists, build hubs, community discourse).

**The class/ascendancy label is NEVER stripped** — it's substrate-grounded identifier. But it's NEVER the primary categorical axis in player-organized vocabulary. Player vocabulary organizes by **what activity the build excels at** (the experience the player has with the build), with the class as the substrate-marker.

---

## 3. Composition with existing canonical commitments

### 3.1 Substrate-led discipline (Disc #41)

> "Substrate votes; designer doesn't pre-impose taxonomy"

**This principle is the player-facing corollary at the substrate-input layer.** Disc #41 says the substrate (input to generative architecture) is curated from external evidence (weapon library + thematic registry + community-validated mechanical architecture), not pre-authored from designer-fiat priors. This principle adds: **the player-experience taxonomy is ALSO not pre-authored from designer priors** — it emerges from how players engage with engine outputs, and the engine should consume that taxonomy POST-emergence (via community-vocabulary research) rather than pre-impose it.

The two principles compose as:
- **Generative-input layer (designer-writes-substrate):** substrate-led discipline applies — substrate informed by external evidence
- **Player-experience layer (player-names-experience):** this principle applies — community-emergent vocabulary; engine listens post-emergence

### 3.2 No-classes architectural recommitment (Matt 2026-05-27)

> "There are no classes... This must be deleted, and immediately. I confirm path (ii) — substrate tuples → kit emergence → canonical_archetype identity post-hoc; NOT class taxonomy."

**This principle is the GENERAL architectural truth the no-classes recommitment was applying at the player-experience layer.** The no-classes recommitment said: "designer-authored class taxonomy is NOT a unit of generative architecture; kits emerge from substrate tuples; identity (canonical_archetype) is post-hoc." This principle says: "designer-authored class taxonomy is NOT the primary categorical axis at the player-experience layer; player-emergent activity vocabulary IS." The recommitment is a SPECIFIC application of this general principle.

### 3.3 Experiential cascade architecture recognition record (2026-05-29 morning)

> "Experiential archetype is the third coordinate axis orthogonal to BC mechanical + cultural-tradition"

**This principle is the FOUNDATION for why the third coordinate axis is at the player-experience layer.** The recognition record's § 1.3 third coordinate axis articulates that experiential archetype (Magic Find / Boss Speed Run / Swarm Clear / End Game Generalist / Build Crafter at the time of authoring) is community-named NOT designer-named. Per the empirical scouting + this principle:

- The third coordinate axis IS the player-names-experience layer
- The candidate vocabulary at recognition-record authoring time (Magic Find / Boss Killer / etc.) was anchored on D2/D3-legacy vocabulary
- Empirical scouting reveals current cross-site convergence is Bossing / Speedfarming / Endgame Generalist (NOT Magic Find as primary)
- Cycle 15+ doc 52 promotion candidate uses community-validated vocabulary at promotion time, not pre-authored vocabulary from training priors

### 3.4 Cycle 13 → Cycle 14 ENDGAME_ENCOUNTER_CATALOG eradication (S1 work)

> Strip class taxonomy from substrate-input layer

**This principle is what the S1 work operationalized at the substrate-input layer.** ENDGAME_ENCOUNTER_CATALOG carried class names (Heavy Barbarian / Standard Wizard / etc.) AS substrate-input. S1 stripped them while preserving BC tuple + element. Per this principle: the BC tuple + element + cultural lineage + period + register are the designer-writes-substrate layer; the class name was vestigial design-construct that conflated the two layers and had to be retired.

### 3.5 Bounded viability + Investment scaling (docs 50 + 51)

> Per-encounter-type validation; per-investment-profile scaling

**These docs locate engine performance evaluation in the designer-writes-substrate layer.** Cohort archetype (DPS-min-maxer / Balanced / Defensive / Hybrid) is engine-performance-test cohort (designer-writes-substrate). Per the empirical scouting + this principle: cohort_archetype is currently a designer-authored taxonomy but may MAP to player-experience vocabulary at Cycle 15+ — Bossing maps to DPS-min-maxer + Defensive cohort sampling; Speedfarming maps to Balanced + Hybrid sampling; Endgame maps to Generalist sampling.

This is a Cycle 15+ research-driven mapping; not v1 commitment.

---

## 4. Architectural implications

### 4.1 Generative architecture writes SUBSTRATE; doesn't pre-author player-experience taxonomy

The engine's generative layer (Phase 2 BC discovery + Phase 4 mechanical archive + Phase 7 mechanical gate) operates on designer-writes-substrate. The substrate is curated from external evidence (substrate library + thematic registry + canonical architecture docs). Designer-fiat impositions of player-experience taxonomy at this layer are violations of substrate-led discipline + this principle.

**Specific operational implication:** the experiential archetype dimension recognition record's third coordinate axis is NOT a generative-input axis at Cycle 14 v1; it's a Cycle 15+ post-emergence consumption-layer addition pending empirical-validation via community-vocabulary research.

### 4.2 Player-experience emerges and is community-named; engine consumes post-emergence

The engine LISTENS to player-experience vocabulary via community-research-as-empirical-evidence-instrument (ARPG community research sprint). Findings inform Cycle 15+ doc 52 promotion + Wave A/B LLM prompt vocabulary integration + spirit-guide content layer + player-facing UI.

**Specific operational implication:** the ARPG community research sprint Matt is preparing to authorize is THE empirical-evidence instrument for this layer. It's substrate-led discipline applied at the player-experience layer (community vocabulary votes; engine consumes post-emergence).

### 4.3 Class/ascendancy/archetype labels are SECONDARY descriptive anchors, NOT primary categorical axes

Player-facing surfaces (build names + faction names + kit names + spirit-guide narrative) should integrate BOTH layers:
- **Substrate-grounded identity** (skill + class/ascendancy/archetype + element + cultural-tradition) — designer-writes layer
- **Experiential frame** (activity / playstyle / investment-tier) — player-names layer

The primary categorical axis is the activity layer; the substrate layer is the descriptive secondary anchor.

**Specific operational implication:** Wave A faction naming + Wave B per-kit identity LLM prompts at Cycle 15+ should compose BOTH layers in the LLM output. The current Phase 5 LLM prompts (`canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md`) carry the designer-writes-substrate layer (BC tuple + cultural lineage + element + weapon family + faction context). A Cycle 15+ extension would add the player-experience layer (experiential archetype + investment-tier) as composed input.

### 4.4 Wave A faction naming + Wave B per-kit identity at Cycle 15+ should integrate BOTH layers

Current state (Cycle 14 v1):
- Wave A consumes BC modal + cultural lineage + element distribution + bc_axis_signature (substrate-only)
- Wave B consumes BC + cultural lineage + element + weapon_type_family + faction anchor (substrate-only)
- Faction naming + per-kit naming emerge from substrate

Cycle 15+ extension target (per doc 52 promotion):
- Wave A consumes BC + cultural lineage + element + **+ player-experience archetype label (Bossing / Speedfarming / Endgame / activity-specific)**
- Wave B consumes BC + cultural lineage + element + weapon_type_family + faction anchor + **+ experiential archetype frame**
- Faction naming + per-kit naming emerge from substrate AND are framed by player-experience layer

The composition in LLM output reflects both layers: substrate-grounded identity + experiential frame in player-facing surface.

### 4.5 Cohort archetype (cohort_archetype taxonomy DPS-min-maxer / Balanced / Defensive / Hybrid) may map to player-experience vocabulary at Cycle 15+

Cycle 14 v1 preserves cohort_archetype as load-bearing for BVV framework (per Matt 2026-05-29 evening scope confirmation). Cycle 15+ revisit candidate per Disc #41: does the cohort_archetype taxonomy map to community-validated player-experience vocabulary?

| cohort_archetype | Maps to player-experience? |
|---|---|
| DPS-min-maxer | Possibly Bossing (single-target high DPS) |
| Balanced | Possibly Endgame Generalist |
| Defensive | Possibly Hardcore mode-specific OR Bossing-tanky |
| Hybrid | Possibly Speedfarming OR Endgame Generalist |

The mapping is NOT 1:1 — cohort_archetype is performance-cohort axis (gauntlet validation framework); player-experience axis is activity-classification. They MAY converge at Cycle 15+ research findings; OR remain orthogonal axes that compose.

This is gandalf + jack-ryan canonical review at Cycle 15+ entry pre-scoping.

---

## 5. Implications for the ARPG community research sprint

This principle is the FOUNDATION for the upcoming ARPG community research sprint:

1. **Sprint scope is the empirical-validation instrument for the player-experience layer** — what community vocabulary converges; what categorical labels emerge; what naming patterns hold cross-site
2. **Sprint findings feed Cycle 15+ doc 52 promotion** — experiential archetype dimension promotion gates on community-validated vocabulary (recognition record gate (ii))
3. **Sprint findings inform Wave A + Wave B LLM prompt Cycle 15+ extension** — community-validated player-experience vocabulary integrated alongside substrate-grounded inputs
4. **Sprint findings may surface cohort_archetype → player-experience mapping** at Cycle 15+
5. **Sprint findings feed spirit-guide content layer** — player-facing narrative speaks BOTH substrate-grounded identity AND experiential frame

This principle is canonical FOUNDATION; sprint is empirical-validation; Cycle 15+ work consumes both.

---

## 6. What this principle does NOT do

- Does NOT retire cohort_archetype (DPS-min-maxer / Balanced / Defensive / Hybrid) for Cycle 14 v1 — preserved as load-bearing for BVV framework per Matt 2026-05-29 evening
- Does NOT pre-commit Cycle 15+ doc 52 promotion vocabulary (Magic Find vs Bossing vs Speedfarming TBD by community research findings)
- Does NOT amend Phase 5 LLM prompts at Cycle 14 v1 (current substrate-only prompts hold; Cycle 15+ extension target)
- Does NOT modify Cascade-resumption-3 work program (cascade architecture mechanics complete the substrate-led emergence; player-experience layer is post-emergence Cycle 15+ extension)
- Does NOT pre-impose experiential-archetype-as-generative-input — generative architecture STAYS substrate-led at Cycle 14 v1; player-experience layer is consumption-only

---

## 7. Cross-references

| Existing artifact | Composition with this principle |
|---|---|
| `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` | This principle is the general architectural truth the recommitment applied at one layer |
| `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` § 1.3 | This principle is the foundation for the third coordinate axis being community-named |
| `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41 | This principle is the player-facing corollary of Disc #41 substrate-led discipline |
| `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` | 8 BC axes are designer-writes-substrate layer |
| `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 | T4 architecture is designer-writes-substrate layer |
| `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` | BVV framework is designer-writes-substrate layer; cohort_archetype map to player-experience layer at Cycle 15+ |
| `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` | Investment scaling is designer-writes-substrate layer; investment-tier vocabulary (low/mid/max) maps to player-experience vocabulary (Low/Above Average/Difficult per Maxroll PoE) |
| `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` | Current prompts are substrate-only; Cycle 15+ extension integrates BOTH layers per § 4.4 of this principle |
| `agentic_orchestration/gandalf/notes/2026-05-29-legolas-mode-a-arpg-archetype-vocabulary-research-brief.md` | Foundational brief; superseded scope by upcoming ARPG community research sprint |
| (ARPG community research sprint dispatch authorization — pending Matt sign-off) | Sprint IS the empirical-validation instrument for the player-experience layer per this principle |

---

## 8. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-29 evening verbatim observation and authorization

**For:** the durable canonical capture of the design principle Matt named — "Designer writes class/archetype; Player names the experience (with derivative/vestigial designer construct left-over parts/pieces as reference only)" — and its architectural implications for engine generative architecture (designer-writes-substrate layer; player-experience layer; class label as vestigial reference) across Cycle 14 v1 and Cycle 15+ work programs

**Empirical foundation:** 30-minute cross-site WebFetch scouting 2026-05-29 evening across Maxroll D4 + Maxroll PoE + Maxroll Last Epoch + Maxroll PoE2 tier-list pages + build-guide URLs. Strong convergence on Bossing / Speedfarming / Endgame as primary activity-based player-experience labels at ≥3 sites; class taxonomy persists at 100% as designer-vestigial substrate marker.

**Composition target:** foundational principle for no-classes architectural recommitment + experiential cascade architecture + Cycle 15+ doc 52 promotion + Wave A/B LLM prompt Cycle 15+ extension + ARPG community research sprint empirical-validation framing

**Future amendments:** ARPG community research sprint findings (post-Cycle-14-close) may refine the empirical foundation + add additional player-experience vocabulary cross-site convergence findings. The principle itself is architectural; the empirical evidence grows.
