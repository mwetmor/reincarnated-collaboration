# Hypothesis Flow + Pattern Library Architecture — PLACEHOLDER FOR REFINEMENT

> **STATUS:** PLACEHOLDER — pre-commitment architectural draft authored 2026-05-31 for Matt review + refinement before any canonical promotion. Synthesizes 2026-05-29 ARPG community research sprint output + designer-writes-substrate / player-names-experience principle + 5-property substrate framework + 7-mechanism-family taxonomy + experiential cascade architecture recognition + Matt 2026-05-31 hypothesis-flow methodology articulation. **Not a commitment.** Document is the substrate for a Pattern B refinement conversation that produces the committed architecture.

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

**The sequencing:** this work gates on (a) Cycle 14 wave-5 closing, (b) WS1A architectural foundations landing (substrate axis expansion + Phase 5 LLM amendment + flavor-element wiring), (c) the manifestation milestone establishing playtest infrastructure. Pattern-library Phase A-E work begins AFTER these gates resolve. Estimated horizon: 6-12 months from now to begin Phase A; 12-24 months to graduate the first encoded patterns.

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

### 1.4 7 mechanism families

**Canonical anchor:** § 19 of same HTML doc.

Seven distinct mechanism families across genre:

| Family | Pattern | Reincarnated current coverage | Gap |
|---|---|---|---|
| **A** — Intra-skill transformation | LE Skill Specialization Tree; PoE Support Gem; LA Tripod; PoE2 Meta Gem | Partial (skill geometry + T4 scope) | MODERATE |
| **B** — Extractable / imbue-able power | D2 Rune Words; D3 Kanai's Cube; D4 Legendary Aspect; D4 Tempering | NONE | **MAJOR GAP** — dominant genre crystallization surface |
| **C** — Class-identity combo | GD Dual Mastery; D3 Class Set 6pc; LA Class Engraving; PoE Ascendancy | Partial (spirit-swap is temporal not simultaneous) | MODERATE |
| **D** — Passive-tree capstone | PoE Keystone; PoE Ascendancy Capstone; GD Devotion Celestial; D4 Paragon Glyph | YES — Reincarnated T4 architecture | No gap — preserved + extended |
| **E** — Item-slot anchor | Mageblood; Headhunter; Enigma; Infinity; Tyrael's Might | Partial (legendary exists; no Mageblood-class) | MODERATE |
| **F** — Consumable / inventory-resident passive | D2 Charms; LE Idols; LE Blessing | None | MINOR |
| **G** — Proc-attached celestial / secondary | GD Devotion Celestial; PoE Watcher's Eye; D3 Legendary Gem secondary | None (T4 proc-on-condition is partial) | MODERATE |

**Architectural headline:** the genre's most-beloved canonical build-defining moments (Enigma in D2, Marauder 6pc in D3, Aspect assembly in D4) all live in **Family B**. Reincarnated has zero Family B mechanisms. T4 architecture is a genuine Family D innovation that should be preserved + extended; **adding a Family B mechanism is the highest-leverage Cycle 15+ design call**.

**Refinement for this work:** the 7 families are the **mechanism-axis flag enum** for pattern-library cells. A cell carries one or more mechanism family flags. Cells targeting Family B are highest-leverage gap-filling candidates. Cells targeting Family D extend existing strength.

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

---

## 2. The hypothesis-flow methodology (Matt 2026-05-31 framing)

### 2.1 Six-stage cycle

The proposed methodology is a closed loop:

```
┌────────────────────────────────────────────────────────────────┐
│  STAGE 1 — Community-research-led hypothesis generation         │
│  Input:    Empirical seed corpus + ongoing legolas Mode A       │
│            research + Matt genre experience + community         │
│            discourse mining                                     │
│  Output:   Hypothesized mathematical cell (provisional)         │
│  Discipline: Substrate-led (community vocabulary votes)         │
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
| `element` | 8-enum + flavor pool | Canonical 8 + flavor-element vocabulary (per Phase 5 LLM call amendment workstream 1A.5) |
| `attribute` | STR / DEX / INT / WIS | Per `attribute-system-2026-05-24.md` (VIT deferred) |
| `t4_strategy` | 6 current + 15 proposed = 21 | Per doc 47 § 4.6 + § 11 proposed; cell may target specific T4 or T4-family |
| `investment_profile` | low / mid / max | Per doc 51 Patterns 1+2 |

### 3.3 Mechanism-axis coordinates

Specifies what mechanism family the cell instantiates AND the structural relationships between component mechanisms.

| Field | Source | Notes |
|---|---|---|
| `primary_mechanism_family` | A-G (per § 19) | Which of the 7 families the cell's primary mechanism lives in |
| `secondary_mechanism_families` | list of A-G | Additional families involved in cell composition |
| `mechanism_p1_score` | 0 / 0.5 / 1 | Identity-axis transformation |
| `mechanism_p2_score` | 0 / 0.5 / 1 | Multiplicative composition |
| `mechanism_p3_score` | 0 / 0.5 / 1 | System-substitution |
| `mechanism_p4_score` | 0 / 0.5 / 1 / 2 | Acquisition memorability (per § 22.5 refinement candidate; P4 weight may scale with acquisition friction) |
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

### 3.5 Experiential-axis coordinates (Layer 2; player-names-experience)

Specifies the player-experience archetype the cell targets.

| Field | Source | Notes |
|---|---|---|
| `primary_experiential_archetype` | 6 canonical labels | Bossing / Speedfarming / Push / Endgame Generalist / Leveling / League Starter (per research sprint synthesis) |
| `sub_axis_flags` | list | Magic Find / IIR / Currency Farmer / Mapper / Hardcore / etc. |
| `investment_tier` | 5-level | Extreme / Low / Medium / High / Mageblood-required |
| `speedfarm_push_position` | -1.0 to +1.0 | -1.0 = pure Speedfarm; +1.0 = pure Push; 0 = generalist |
| `cognitive_load_target` | low / medium / high | Per § 4.6 CLI (Cognitive Load Index) framework |
| `gear_dependency_index` | low / medium / high | Per § 4.6 GDI framework |
| `execution_skill_floor` | low / medium / high | Per § 4.6 |
| `execution_skill_ceiling` | low / medium / high | Per § 4.6 |
| `playstyle_geometry_tag` | ranged / melee / all-rounder | Per PoE-Vault community vocabulary |

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

---

## 4. The flag enum — what gets attached to generated characters

Flags are the engine-side instrument that connects pattern-library cells to generated characters. When the engine generates a character, the cohesion-judge or post-generation analyzer evaluates which cells the character matches and attaches the corresponding flag set. Downstream stages act on flags.

### 4.1 Primary archetype flags (player-names layer)

| Flag | Source | Notes |
|---|---|---|
| `PRIMARY_BOSSING` | Cross-site STRONG (6 sites) | Single-target high-DPS specialization |
| `PRIMARY_SPEEDFARM` | Cross-site STRONG (6 sites) | Clear-rate optimization |
| `PRIMARY_PUSH` | Cross-site STRONG (4 sites) | Content-depth progression |
| `PRIMARY_ENDGAME_GENERALIST` | Cross-site STRONG (5 sites) | All-rounder |
| `PRIMARY_LEVELING` | Cross-site STRONG (4 sites) | Pre-endgame progression-stage |
| `PRIMARY_LEAGUE_STARTER` | Cross-site STRONG (4 sites) | Self-sufficient early-economy |
| `PRIMARY_MAPPER` | Game-specific MODERATE (PoE-genre) | Reincarnated may absorb into Push or distinguish |
| `PRIMARY_CURRENCY_FARMER` | Game-specific WEAK (PoE-only) | Likely absorb into Speedfarm sub-axis |
| `PRIMARY_HARDCORE` | Mode-specific | Composes with other primary flags |

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

### 4.8 Mechanism family flags (per § 19)

| Flag | Family | Notes |
|---|---|---|
| `MECHANISM_FAMILY_A` | Intra-skill transformation | LE Specialization / PoE Support / LA Tripod |
| `MECHANISM_FAMILY_B` | Extractable / imbue-able power | D2 Runewords / D3 Cube / D4 Aspect; **MAJOR GAP** in Reincarnated |
| `MECHANISM_FAMILY_C` | Class-identity combo | GD Dual Mastery / D3 Class Set / LA Engraving |
| `MECHANISM_FAMILY_D` | Passive-tree capstone | PoE Keystone / Reincarnated T4 |
| `MECHANISM_FAMILY_E` | Item-slot anchor | Mageblood / Headhunter / Enigma |
| `MECHANISM_FAMILY_F` | Consumable / inventory-resident | D2 Charms / LE Idols |
| `MECHANISM_FAMILY_G` | Proc-attached celestial | GD Devotion / PoE Watcher's Eye |

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
    ├── Substrate axis expansion (per § 4-9 of HTML doc; experiential archetype + investment tier + Maxroll 5-axis + playstyle geometry tags + GDI + CLI + skill-floor/ceiling + skill-role distribution)
    ├── Phase 5 LLM call architecture amendment (Workstream 1A.5)
    └── Flavor element vocabulary wiring (canonical 2.5; never previously wired as live LLM call)
    ↓
Manifestation milestone landed
    │
    ├── One realized character (Drifter of the Scattered Reach or equivalent)
    ├── Modular character architecture established (stock mannequin + armor pieces + materials)
    ├── Initial component library (5-10 base bodies + 50-100 heads + 200-500 armor + 100-300 weapons + 100-200 accessories per modular character research)
    ├── Spirit-form sculpting prototype
    ├── Manifestation transition (Spirit → realized character)
    ├── Basic moveset + combat interaction
    └── Glimpse of level-50 future-self
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

### 5.3 Estimated horizon

| Phase | Start | Duration estimate |
|---|---|---|
| WS1A foundations | Post-Cycle-14-close | 4-8 weeks |
| Manifestation milestone | After WS1A | 3-6 months |
| Phase A infrastructure | After manifestation lands | 4-8 weeks |
| Phase B initial library | Concurrent with A's end | 2-4 months |
| Phase C generation integration | After B reaches ~10 locked cells | 2-4 months |
| Phase D validation + iteration | Continuous from C | Ongoing |
| Phase E expansion | Continuous | Ongoing |

**Net horizon to begin Phase A:** 6-12 months from now. **Net horizon to first library-locked cells:** 12-18 months. **Net horizon to commercially-meaningful pattern library:** 24-36 months. The work is substantial but proceeds in increments; value emerges progressively as the first cells graduate.

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

---

## 9. Cross-references

### 9.1 Composes with (existing canon)

- `canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md` — foundational three-layer architecture
- `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` — third coordinate axis
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 41 — substrate-led discipline (with refinement per § 1.2 above)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — T4 architecture
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — BVV
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` — investment scaling
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes
- `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` — Phase 5 prompts (current; Cycle 15+ extension target)
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

**End of placeholder.**
