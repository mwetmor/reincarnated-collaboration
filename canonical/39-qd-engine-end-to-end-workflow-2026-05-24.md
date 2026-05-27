# 39 — QD-Engine End-to-End Workflow (Architecture B — Substrate-Bound at Phase 2 + Content Lifecycle; Production Canonical)

> **STATUS:** CURRENT (load-bearing as of 2026-05-24; promoted to numbered canonical + expanded with end-to-end content lifecycle 2026-05-26) — supersedes `canonical/story/historical/qd-engine-end-to-end-workflow-A-substrate-agnostic-developer-tool-2026-05-21.md` (Architecture A; now developer-tool reference)

**Date:** 2026-05-24 (initial authoring); 2026-05-26 (promotion to numbered canonical + § 0.5 end-to-end content lifecycle expansion)
**Author:** gandalf (story-and-design steward)
**Status:** ACTIVE — production canonical engine architecture; locks Architecture B (substrate-bound at Phase 2) + substrate-genre-flagging unified-architecture pattern per Matt 2026-05-24 design dialogue during Cycle 10 Stage 3; promoted from `canonical/story/` to numbered canonical (doc 39) per Matt 2026-05-26 directive following doc 40 authoring (gear/balance/guide architecture composes with this workflow at Phase 2 substrate-binding + Phase 5 cohesion + § 0.5 content lifecycle)
**Authority:** Matt 2026-05-24 — Architecture B selected as primary production canonical; Matt 2026-05-26 — promotion to numbered canonical + § 0.5 expansion to capture full end-to-end content lifecycle including T4-and-gear dependency chain (one-way; NO circular dependency)
**Companion docs:**
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` (Cycle 13 architectural foundation; gear/balance/guide/multi-T4 architecture composes with this engine workflow at Phase 2 + Phase 5; § 0.5 of this doc captures the content lifecycle dependency chain that doc 40 architecture operates within)
- `canonical/story/historical/qd-engine-end-to-end-workflow-A-substrate-agnostic-developer-tool-2026-05-21.md` (Architecture A; now developer-tool reference per Matt 2026-05-24 unified-architecture refinement)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (operational 8-axis BC spec)
- `canonical/story/skill-system-2026-05-24.md` (Phase 2 skill composition; algorithmic mechanic-alteration; spirit-guide explainer; nested mythology naming; faction-generated proxies)
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute system STR/INT/WIS/DEX)
- `canonical/story/off-hand-items-2026-05-24.md` (Main/Secondary slot architecture)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 cell-targeting intent)
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` (Pattern 6 retirement — role-shape constraint removed per this discipline)
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` (genre context)
- `canonical/00-ground-state.md` (current truth oracle)

---

## 0. TL;DR

Architecture B is the production engine flow for Reincarnated v1 and all commercial profiles via substrate-genre-flagging unified-architecture pattern. Key locks:

1. **Substrate-bound at Phase 2** — engine pulls specific substrate row at generation time (genre-canonical pattern; matches D2/D3/D4/PoE/LE/GD)
2. **Substrate-genre-flagging** — substrate library partitioned by genre tag; engine pulls from genre-appropriate subset per product (Reincarnated = fantasy-tagged; future sci-fi cyberpunk = sci-fi-tagged; etc.); single engine architecture serves all commercial profiles
3. **NO pre-imposed role-shape constraints** — per Pattern 6 retirement; roles EMERGE from BC-coordinates implicitly (Axis 2A proxy_density + Axis 2B control_density + Axis 4 defensive_profile + amplitude variance)
4. **Phase 2 substrate-binding policy per cell-type:**
   - **Option α — Martial cells (STR/DEX primary, physical-element):** weapon-slot requires 5-tuple mechanical-fingerprint match
   - **Option β — Caster cells (INT/WIS primary, non-physical-element):** weapon-slot requires ATTRIBUTE-LEVEL match only
   - **Option C — Cross-attribute hybrid cells (Red Mage / Monk / Holy Knight):** weapon-slot permits cross-attribute wielding with ω-penalty per BDI ω-field resource-dimension
5. **Phase 5 cohesion-coalescence handles flavor + naming** — sub-element flavor mapping (renamed 2026-05-24 from "element canonical-pair flavor" to disambiguate from retired seasonal-realm-mapping concept AND from legendary canonical-pair set-bonuses); archetypal player-facing naming per universal naming discipline; spirit-guide explainer integration; bi-modal form library + nested mythology naming + faction-generated-proxy templates
6. **Empirical-trigger discipline** — explicit triggers for potential switch to Architecture A (developer-tool) or Architecture C (mid-bind hybrid) if Architecture B's hypothesized benefits don't materialize

---

## 0.5 End-to-end content lifecycle (dependency chain — one-way; NO circular dependency)

The 8-phase workflow (§ 1) describes a SINGLE KIT's journey through generation → sim → archive → cohesion → visual → gate → export. This § 0.5 describes the BIG-PICTURE CONTENT LIFECYCLE — how kits + T4 nodes + skill trees + gear specifications + legendary instances + sim validation interrelate across the engine's full content generation activity.

**The dependency chain is strictly one-way. No artifact downstream regenerates an artifact upstream. Sim validation CONSUMES kits + T4 nodes + legendaries; it does NOT generate any of them.**

### 0.5.1 The six-step content lifecycle

| Step | Artifact | Generated from | Depends on | Generation algorithm / source |
|---|---|---|---|---|
| **1** | **Kits** | Class architecture + BC-target subspace + substrate (per § 1 Phase 1 + Phase 2 cell-targeting) | Nothing in this chain | Phase 1 BC-target queue + Phase 2 cell-composition |
| **2** | **T4 nodes** (skill capstones) | **Algorithm § 8 scored-candidate strategy registry** (RESOURCE_CONVERSION, TRADE_OFF, ELEMENT_CONVERSION, DEFENSIVE_CONVERSION, GEOMETRY_COLLAPSE, DEFENSIVE_TRADEOFF) operating on **kit mechanics** | Kits only (Step 1) | Algorithm § 8 strategies; INDEPENDENT of gear and legendaries; per doc 40 § 8.1 |
| **3** | **Skill tree structure** (chains organized around T4 capstones) | Chain architecture per class chain count - 1 formula (doc 40 D83) | Kits + T4 nodes (Steps 1-2) | Per-class chain composition; supporting chains may exist without T4 capstones (hybrid/multi-element builds) |
| **4** | **Gear specifications** (per slot per cell) | **Spec-driven gear gen** (doc 40 D7): kit + T4 selection produces gear spec; scored-candidate strategy registry produces candidates | Kits + T4 nodes (Steps 1-2) | Mirrors Algorithm § 8 pattern but operates on gear-stat surface; spec defined by kit+T4; candidates generated to fit |
| **5** | **Legendary instances** (and other rarity instances) | Strategy registry generates candidates to fit gear specs; legendary tier carries capability toolkit (doc 40 D9 + D54) | Kits + T4 nodes + gear specs (Steps 1-4) | T4-attunement on tier 1+2 legendaries (doc 40 D33 + D51); rarity escalation across Common→Legendary (doc 40 D8) |
| **6** | **Sim validation** | Hybrid cohort + edge-case sampling with per-legendary cohort anchoring (doc 40 D84) | All upstream artifacts (Steps 1-5) | Cycles tier-2 legendaries × cohort archetypes × **pre-existing node configurations**; CONSUMES upstream artifacts; does NOT generate any of them |

### 0.5.2 Why this is unambiguous (no circular dependency)

The apparent loop risk would be: legendaries → T4 nodes → legendaries. But the actual flow is:

- **T4 nodes are generated by Algorithm § 8 (Step 2) from kit mechanics — INDEPENDENT of legendaries.** Algorithm § 8 strategies operate on the kit's mechanical signature; gear is not an input.
- **Gear specifications (Step 4) depend on T4 nodes (Step 2)** — gear is generated to fit pre-existing T4 nodes, not the other way around.
- **Legendary instances (Step 5) depend on gear specs (Step 4)** — legendaries are downstream from gear specifications.
- **Sim validation (Step 6) CONSUMES nodes + legendaries** — it samples pre-existing nodes that cohort+weapon configurations would invest in; it does NOT generate new nodes from legendaries.

The phrase in doc 40 § 8.7 sim methodology "Map appropriate node configurations for cohort × weapon combinations" means: **sample from pre-existing nodes** (generated at Step 2) for cohort × weapon scenarios. Sim is a CONSUMER of nodes; not a generator.

### 0.5.3 How this composes with the 8-phase per-kit workflow

The 8-phase workflow (§ 1) operates within Step 2 + Step 4 + Step 6 of the content lifecycle:

| Lifecycle step | Per-kit workflow phase | Note |
|---|---|---|
| Step 1 (Kits) | Phase 1 + Phase 2 cell-composition | Per-kit composition; substrate-bound at Phase 2 |
| Step 2 (T4 nodes) | Phase 2 skill composition (algorithm § 8 if T4 cell) | Per-kit T4 generation; one T4 set per kit; per doc 40 D81 phasing all 4 phases of T4 algorithm wrap into Cycle 13 |
| Step 3 (Skill tree) | Phase 2 skill composition output | Per-kit skill tree; chains organized around T4 capstones; supporting chains per doc 40 D83 |
| Step 4 (Gear specs) | Phase 2 substrate-binding output produces gear-spec inputs; gear specifications derived per doc 40 D7 | Specs flow from per-kit composition |
| Step 5 (Legendary instances) | Cross-kit generation step; legendaries generated against gear specs per doc 40 D7 + D9 + D54 | Legendaries reference T4 nodes via T4-attunement (doc 40 D33 + D51) |
| Step 6 (Sim validation) | Phase 3 convergence + measurement + Phase 4 archive insertion | Sim validates kit + bound substrate; multi-T4 sim methodology per doc 40 D84 cycles legendaries against cohort-mapped node configurations |
| (Other phases) | Phase 5 cohesion + Phase 6 visual + Phase 7 gate + Phase 8 export | Downstream from sim validation; cohesion enriches; visual + gate + export complete pipeline |

### 0.5.4 What this enables for Cycle 13 stat-sheet partition design

The stat-sheet partition cycle (doc 40 D14 — early-Cycle-13 milestone) operates at Step 4 (gear specifications). The partition design determines:

- Which modifier types exist on the character stat sheet (Step 4 surface)
- Which slots roll which modifier types (Step 4 spec structure)
- Probability distribution per slot per modifier (Step 4 spec instantiation)
- Tier-restricted modifier availability (Step 4 + Step 5 — some modifiers only on legendaries; some only at endgame tiers per doc 40 D51 + D54)
- Node-count + chain-distribution interaction math (Step 4 ↔ Step 3 interaction)

**The partition design lands BEFORE Step 5 (legendary instances) generation runs at scale, and BEFORE Step 6 (sim validation) executes against the full architecture.** Partition design is upstream foundation; legendaries + sim are downstream consumers.

### 0.5.5 Cycle 13 work-cycle scope per content lifecycle

Per doc 40 § 8.5 + § 9 Cycle 13 scope mapping, Cycle 13 work touches all 6 lifecycle steps:

| Step | Cycle 13 work-cycle owner(s) |
|---|---|
| Step 1 (Kits) | rocket (composition) + gandalf (cell-targeting design) |
| Step 2 (T4 nodes — all 4 phases per doc 40 D81) | rocket (Algorithm § 8 + 4-phase T4 implementation) + gandalf (design support) + jack-ryan (Gate-1 per phase) |
| Step 3 (Skill tree) | rocket (implementation) + gandalf (chain architecture design per doc 40 D83) + T4 PM1 outputs |
| Step 4 (Gear specs — stat-sheet partition design) | **Multi-seam early-Cycle-13 milestone:** gandalf intent + gamora methodology (Discipline #18) + rocket implementation + jack-ryan critique + legolas Mode A research |
| Step 5 (Legendary instances) | rocket (generation against gear specs); also includes weapon damage spec completeness check + non-weapon gear baseline stats per doc 40 § 3.6 D14 scope expansion |
| Step 6 (Sim validation) | gamora (gauntlet sim against full architecture per doc 40 D84 hybrid cohort + edge-case + per-legendary anchoring methodology) |

---

## 1. The full workflow — visual flow (Architecture B + doc 40 + Cycle 13 integrated)

> **2026-05-26 update:** § 1 visual flow now integrates doc 40 (gear/balance/guide/multi-T4 architecture) + Cycle 13 architectural foundation commitments inline. Phase 2 expanded with multi-T4 algorithm (all 4 phases per doc 40 D81) + spec-driven gear gen (D7) + tier structure (D50-D52) + capability toolkit (D9, D54-D56) + T4-attunement annotation (D33, D51). Phase 3 expanded with combat sim node-population methodology (D84) + playability criterion (D61). Phase 5 expanded with spirit-guide data-oracle integration (D28-D32) + T4-attuned gear cohesion. Per § 0.5 dependency chain — all expansions preserve one-way generation flow with NO circular dependency.

```
┌──────────────────────────────────────────────────────────────────────────┐
│ SUBSTRATE LIBRARY (multi-genre via genre-flagging)                        │
│  - weapon_knowledge_entries + off-hand items (Sidecar B integrated)       │
│  - genre tag per row (fantasy / sci-fi / cyberpunk / post-apoc / etc.)    │
│  - cultural_lineage_canonical + historical_period_canonical               │
│  - named-bearer attribution (Track M1 / sub-agent gandalf seed list)      │
│  - Tier S/A/B/C composite quality scoring                                 │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │ (CONSUMED at Phase 2; substrate-bound generation)
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: ARCHIVE STATE INSPECTION (gamora)                                │
│  Input:  current mechanical-BC archive state + substrate-coverage status  │
│  Action: identify sparse cells; compute novelty + diversity needs;        │
│          check substrate-coverage at 4-tuple level per cell                │
│          + check 4 progression-node coverage (doc 40 D27): early game /   │
│          mid game / endgame start / endgame [85% target]                  │
│  Output: BC-target queue (cells to fill, ranked by priority + substrate-  │
│          coverage feasibility + progression-node coverage)                │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: GENERATION (BC-TARGET-DRIVEN + SUBSTRATE-BOUND + DOC-40         │
│         MULTI-T4 + SPEC-DRIVEN GEAR) (rocket)                             │
│                                                                            │
│  Input:  BC-target coordinate [5-tuple: range × tempo × amplitude ×       │
│          attribute × proxy-density] + genre filter (per product)          │
│          + class chain count (doc 40 D83: T4 count = chain count - 1)    │
│          + progression-node target (doc 40 D27)                          │
│                                                                            │
│  Action:                                                                  │
│    ┌─────────── 2a. KIT COMPOSITION ───────────────────────────────────┐ │
│    │ 1. Compose skill kit matching cell                                  │ │
│    │    - 10-15 node skill tree budget (skill-system § 1)                │ │
│    │    - Element coupling per attribute (element_biases.py)             │ │
│    │    - Mechanic-altering passives only (no filler)                    │ │
│    │    - Tier-1 rotation + tier-2 β-pair + tier-3 build-defining        │ │
│    │    - Max 8 active skills (doc 40 D82; flat budget)                  │ │
│    │    - Chains organized for class chain count (doc 40 D63-D64)        │ │
│    │      • 3-chain class: 2 chains with T4 + 1 supporting T3 chain      │ │
│    │      • 4-chain class: 3 chains with T4 + 1 supporting T3 chain      │ │
│    │      • Supporting chains enable hybrid/multi-element builds         │ │
│    └─────────────────────────────────────────────────────────────────────┘ │
│    ┌─────────── 2b. T4 ALGORITHM (Algorithm § 8) ─────────────────────┐ │
│    │ 2. Generate T4 nodes per class chain count (doc 40 D81 phased):    │ │
│    │    - All 4 phases of T4 algorithm wrap into Cycle 13:               │ │
│    │      • Phase 1: T4s into chains as capstones                        │ │
│    │      • Phase 2: Multiple T4 options per chain                       │ │
│    │      • Phase 3: Character-wide vs chain-wide scope dimension        │ │
│    │      • Phase 4: Full sim cycling through all T4 configurations      │ │
│    │    - Scored-candidate strategy registry (6 v1 strategies):          │ │
│    │      RESOURCE_CONVERSION / TRADE_OFF / ELEMENT_CONVERSION /         │ │
│    │      DEFENSIVE_CONVERSION / GEOMETRY_COLLAPSE / DEFENSIVE_TRADEOFF  │ │
│    │    - DUAL mechanical impact per T4 (doc 40 D76):                    │ │
│    │      • Character-wide effect (kit-wide play feel shift)             │ │
│    │      • Within-chain (or parallel-chain) effect                      │ │
│    │    - INDEPENDENT of gear/legendaries (per § 0.5 dependency chain)   │ │
│    └─────────────────────────────────────────────────────────────────────┘ │
│    ┌─────────── 2c. SUBSTRATE BINDING ────────────────────────────────┐ │
│    │ 3. PULL specific substrate weapon from genre-filtered v1_scope:    │ │
│    │    - Martial cell (Option α): 5-tuple mechanical-fingerprint match │ │
│    │    - Caster cell (Option β): attribute-level match only            │ │
│    │    - Hybrid cell (Option C): cross-attribute with ω-penalty        │ │
│    │ 4. PULL specific substrate secondary item per off-hand-items doc:  │ │
│    │    (shield / tome / banner / focus / horn / talisman /              │ │
│    │     weapon-integrated accessory / dual-wield secondary weapon)     │ │
│    └─────────────────────────────────────────────────────────────────────┘ │
│    ┌─────────── 2d. SPEC-DRIVEN GEAR GEN (doc 40 D7) ─────────────────┐ │
│    │ 5. Derive gear specifications from kit + T4 selection:              │ │
│    │    - Per-slot specification (which modifier types; what magnitudes) │ │
│    │    - Stat-sheet partition design applies (doc 40 D13-D14 + § 3.6   │ │
│    │      7-item scope: modifier enum + per-slot partition + per-slot    │ │
│    │      probability + node-count interaction + weapon damage specs +   │ │
│    │      non-weapon baseline + main_weapon routing cleanup)             │ │
│    │ 6. Generate gear instances at all rarity tiers (doc 40 D8):         │ │
│    │    - Common / Uncommon / Rare / Epic baseline (kit-attuned;         │ │
│    │      chain-aware; spec-driven)                                      │ │
│    │    - Legendary instances at 4 tiers (doc 40 D50; tier 0/0.5/1/2):  │ │
│    │      ┌─ Capability TOOLKIT at all tiers (doc 40 D9 + D54):         │ │
│    │      │  multiplicative / mechanic-adjusting / spatial-adjusting /  │ │
│    │      │  axis-adjusting / added-skill                                │ │
│    │      ├─ HIGH PROBABILITY triggered-passive on weapons (doc 40 D55): │ │
│    │      │  (e.g., "spawns tornadoes on wind hit"; "shrapnel on phys") │ │
│    │      │  - True actives EXTREMELY RARE + additive (weapons only)    │ │
│    │      ├─ Modifier-surface expansion over scalar (doc 40 D56):       │ │
│    │      │  legendaries unlock NEW stat types Epic cannot roll         │ │
│    │      └─ T4-ATTUNEMENT annotation gate (doc 40 D33 + D51):           │ │
│    │         ONLY tier 1+2 legendaries carry T4-attunement;              │ │
│    │         tier 0+0.5 carry capability toolkit but no T4-attunement;  │ │
│    │         attunement = multiplicative + mechanic-alteration on        │ │
│    │         matching T4 path                                            │ │
│    │    - Unique instances at 4 tiers (doc 40 D49)                       │ │
│    │    - Set instances at 2 tiers (doc 40 D48; endgame-only;            │ │
│    │      always T4-attuned per D35)                                     │ │
│    │ 7. Drop pool restriction by content-tier (doc 40 D50):              │ │
│    │    - Tier 0 content: tier 0 legendaries only                        │ │
│    │    - Tier 0.5 content: tier 0 + 0.5 legendaries                     │ │
│    │    - Tier 1+2 content (endgame): all 4 tiers of legendaries         │ │
│    └─────────────────────────────────────────────────────────────────────┘ │
│    ┌─────────── 2e. COHERENCE + FACTION ──────────────────────────────┐ │
│    │ 8. Compose trait constellation                                      │ │
│    │ 9. Apply ω-field + τ-field mechanical-coherence constraints         │ │
│    │ 10. Generate faction-proxy spawn-template per algorithm § 8.6       │ │
│    │     (faction-anchor derived from substrate weapon's cultural-       │ │
│    │      tradition + period — IMMEDIATELY AVAILABLE at Phase 2)         │ │
│    └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  Output: complete mechanical kit + multi-T4 capstones + skill tree         │
│          structure + bound substrate weapon + bound secondary item +       │
│          gear specifications + gear instances at all rarities (incl.       │
│          T4-attuned tier 1+2 legendaries + sets) + proxy-spawn-template +  │
│          algorithm output bundle                                          │
│                                                                            │
│  Disciplines:                                                              │
│  - NO pre-imposed role-shape constraints (per Pattern 6 retirement)       │
│  - Roles EMERGE from BC-coordinates implicitly                             │
│  - One-way dependency chain (per § 0.5): T4 nodes INDEPENDENT of gear      │
│  - Balance as PROPERTY not PROCESS (per doc 40 D1)                         │
│  - Spec-driven generation; sim validates at generation time                │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: CONVERGENCE + MECHANICAL MEASUREMENT (gamora)                    │
│         + MULTI-T4 SIM METHODOLOGY (per doc 40 D84) + PLAYABILITY GATE   │
│                                                                            │
│  Input:  complete kit + multi-T4 capstones + bound substrate +            │
│          gear instances at all rarities                                   │
│                                                                            │
│  Action: run simulation with SPECIFIC bound weapon's mechanical            │
│          signature (specific damage range, attack speed, geometry, etc.); │
│          converge modifier; measure 8 BC axes per kit                     │
│          ┌─ Axis 1 — Engagement profile (range × mobility)                │
│          ├─ Axis 2 — Damage geometry (single/AOE/chain/multi-spawn)       │
│          ├─ Axis 2A — Proxy density                                       │
│          ├─ Axis 2B — Control density                                     │
│          ├─ Axis 3A — Damage tempo                                        │
│          ├─ Axis 3B — Damage amplitude variance                           │
│          ├─ Axis 4 — Defensive profile                                    │
│          └─ Axis 5 — Resource economy                                     │
│                                                                            │
│  Multi-T4 sim methodology (doc 40 D84 — hybrid cohort + edge-case):       │
│    - Cycle each tier-2 legendary/set weapon                               │
│    - Determine cohort archetypes that would equip it                      │
│      (DPS-min-maxer / balanced / defensive / hybrid)                      │
│    - Map appropriate node configurations for cohort × weapon              │
│      (Sub-option A: per-weapon cohort coverage — primary)                 │
│      (Sub-option B: per-legendary cohort selection — compute fallback)    │
│      (Hybrid-within-hybrid: A for ambiguous; B for cohort-clear)          │
│    - Sample PRE-EXISTING nodes (per § 0.5 — sim CONSUMES, doesn't gen)    │
│    - Validate each attuned-T4 configuration independently per node        │
│                                                                            │
│  Multi-node calibration (doc 40 D27):                                     │
│    - Validate against power-band appropriate for kit's progression node   │
│    - early game / mid game / endgame start / endgame [85% target]         │
│                                                                            │
│  Playability gate (doc 40 D61 — load-bearing validation criterion):       │
│    - KPM in target band for progression node                              │
│    - Coherent skill rotation (not degenerate; not chaotic)                │
│    - Resource flow functional (mana/energy/cooldowns sustained-but-       │
│      non-trivial)                                                          │
│    - Defensive uptime adequate                                            │
│    - No degenerate states (stunlock / zero-damage void / mandatory locks) │
│    - Visual/cognitive load manageable                                     │
│    - PLAYABLE-AND-IN-BAND is the validation criterion                     │
│                                                                            │
│  Compute discipline (doc 40 D62):                                         │
│    - Low-compute-yet-meaningful sim cycle is constraint                   │
│    - Stratified sampling / tiered validation / quick-estimate hybrid /    │
│      caching per gamora methodology consultation (Discipline #18)          │
│                                                                            │
│  Output: kit + multi-T4 capstones + bound substrate + 8-axis BC           │
│          coordinate per attuned-T4 configuration + per-tier WR +          │
│          convergence data + playability gate disposition per cohort       │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: MECHANICAL ARCHIVE INSERTION (gamora)                            │
│  Input:  kit + bound substrate + 8-axis BC coordinate                     │
│  Action: math gates determine archive disposition                         │
│          ┌─ Pareto dominance check (kit+substrate as unit)                │
│          ├─ Crowding distance / hypervolume contribution                  │
│          ├─ Mahalanobis distance (duplicate detection)                    │
│          ├─ Information gain (KL) for novelty score                       │
│          └─ Eviction rules if cell at capacity                            │
│  Output: kit+substrate ACCEPTED (in archive) or REJECTED                  │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │ (if ACCEPTED)
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ PHASE 5: COHESION COALESCENCE (gandalf cohesion + rocket LLM call) +     │
│         SPIRIT-GUIDE DATA-ORACLE INTEGRATION (doc 40 D28-D32) +          │
│         T4-ATTUNED GEAR COHESION (doc 40 D33-D39)                        │
│                                                                            │
│  Input:  accepted kit + multi-T4 capstones + gear instances at all       │
│          rarities + bound substrate + mechanical-BC coordinate            │
│                                                                            │
│  Action: LLM cohesion-judge confirms identity-narrative coherence +       │
│          assigns flavor + naming (substrate identity ALREADY BOUND from   │
│          Phase 2; cohesion-judge confirms + enriches):                    │
│          ┌─ confirm substrate-thematic fit (cultural-tradition coherence) │
│          ├─ sub-element flavor mapping per element + bound substrate's   │
│          │  cultural-tradition                                            │
│          ├─ bi-modal form-library assignment (per Sketch F + Matt 2026-   │
│          │  05-24 lock — engine-internal named-personage substrate-       │
│          │  anchor; player-facing layer UNIFORM archetypal naming)        │
│          ├─ naming-space partitioning per engine-anchor                   │
│          ├─ nested mythology naming (Tier-2 invokes Tier-1 per skill-     │
│          │  system § 12.4)                                                │
│          ├─ archetypal form name + skill names per D7 AI-tell discipline  │
│          └─ commit theme + flavor per loot-architecture tier              │
│                                                                            │
│  Spirit-guide data-oracle integration (doc 40 D28-D32):                   │
│    - Generate spirit-guide projection templates for kit+gear:             │
│      • Per-T4 projection: "T4-A projects KPM X at progression node Y"    │
│      • Per-content-tier projection: "tier-1 content yields KPM, gear-    │
│        pwr, set-prob tradeoffs"                                           │
│      • Per-legendary projection: "legendary L advocates T4-Z; projected  │
│        KPM if attuned is X (currently X')"                                │
│    - Voice: NEUTRAL OBSERVATION (data oracle), not evaluative counselor  │
│    - Language: "projected to / typically / estimated" (D31 honesty)       │
│    - Throne-resident framing per existing spirit-guide canon (D30)        │
│                                                                            │
│  T4-attuned gear cohesion (doc 40 D33-D39):                              │
│    - Tier-1+2 legendary/set: confirm T4-attunement aligns with kit's     │
│      T4 paths (multiplicative + mechanic-alteration per matching T4)     │
│    - Heroic Spirit narrative cohesion: T4 paths = aspects of Spirit;     │
│      T4-attuned gear = evidence of latent aspects                         │
│    - Sets: confirm set-level T4 attunement; multi-piece commitment        │
│      for full bonuses                                                     │
│    - Persuasion-to-experiment surface: spirit guide will use these        │
│      cohesion outputs to present respec opportunities to players          │
│      (per doc 40 D65 respec-with-legendary-trigger mechanism)             │
│                                                                            │
│  Acquisition curve calibration (doc 40 D21):                              │
│    - Generate Option A calibrated drop rates per content tier             │
│    - Drop rate = f(expected KPM × engagement distribution × target       │
│      saturation curve per 85th-percentile cumulative target D18)         │
│    - Pure RNG with calibrated rate (no smart-loot pity per D21)          │
│    - Gap-filling discipline applies (D80) — drop calibration considers   │
│      stat-sheet gap-filling probability per player accumulated loadout   │
│                                                                            │
│  Output: kit + multi-T4 capstones + bound substrate + coalesced identity  │
│          + archetypal naming + spirit-guide projection templates + T4-    │
│          attuned gear cohesion + acquisition curve calibration + flavor   │
│          + element-pair mapping                                           │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ PHASE 6: VISUAL COALESCENCE (galadriel)                                   │
│  Input:  fully-coalesced kit                                              │
│  Action: CV-pipeline visual identity assignment                           │
│          - image-pass-through-to-Meshy OR ChatGPT-gen-to-Meshy per       │
│            asset-pipeline § 3.6 verdict                                   │
│          - Control Rig / Niagara / PCG asset generation                  │
│  Output: kit + visual assets                                              │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ PHASE 7: JOINT-GATE EVALUATION (gandalf + jack-ryan + Matt)               │
│  Input:  fully-coalesced + visualized kit                                 │
│  Action: Discipline #18 mechanical AND cohesion AND visual pass           │
│  Output: kit APPROVED for production or returned to specific phase        │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ PHASE 8: PROFILE ASSEMBLY + EXPORT (rocket + star-lord)                   │
│  Input:  approved kit                                                     │
│  Action: filter by profile config (Reincarnated v1 vs future commercial   │
│          profile); format and ship                                        │
│  Output: shipped content                                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Why Architecture B (and not A) — the architectural reasoning

Per Matt 2026-05-24 design dialogue, Architecture B is selected with the following hypothesis:

**Substrate-context (period/culture/named-personage) at engine level brings weight to clustering + algorithmic outcomes.**

### 2.1 What Architecture B enables at Phase 2 (immediately available)

| Signal | What it enables at Phase 2 |
|---|---|
| **Bound weapon's cultural-tradition** | Algorithm § 8 mechanic-alteration informed by cultural canon (Mexica-anchored kit gets "Obsidian-Edge Cascade" regime-change, not generic mid-INT-spike); algorithm § 8.6 faction-spawn-template derives faction-anchor immediately; sub-element flavor mapping has cultural signal |
| **Bound weapon's historical period** | Engine generation period-coheres at kit-spawn (medieval-european forms get medieval-period weapons + skills); avoids anachronistic mix |
| **Bound weapon's named-bearer attribution** | Bi-modal form-library engine-anchor assigned at Phase 2 (per Sketch F ~32% named-personage); per skill-system § 12.4 nested mythology naming triggers in Phase 5 |
| **Bound weapon's mechanical signature** | Phase 3 sim runs with REAL combat fidelity (specific damage range / attack speed / etc.) |
| **Genre-tag (per substrate-genre-flagging)** | Engine pulls from genre-appropriate substrate subset for each product (Reincarnated = fantasy; future sci-fi = sci-fi-tagged); unified-architecture supports all commercial profiles |

### 2.2 Genre-canonical alignment

Every major ARPG (D2/D3/D4/PoE/LE/GD) substrate-binds at generation. The common pattern:

| Game | Substrate-binding pattern |
|---|---|
| D2 | Item drop → pull base from substrate pool → roll quality + affixes → instantiate complete item with substrate identity |
| D3 | Roll quality → if legendary, pull specific named substrate → roll affixes → instantiate |
| D4 | Similar; substrate-bound at drop |
| PoE | Drop → pull item-base from substrate → roll mods → unique drops pull named substrate |
| LE | Same pattern |
| GD | Same pattern |

**Architecture B follows this genre-canonical pattern.** New contributors + designers find this intuitive. Architecture A explicitly DEVIATES from genre canon (more sophisticated decoupling but counter-intuitive).

### 2.3 Substrate-led discipline preservation

Critical clarification: **Architecture B preserves substrate-led discipline.** Substrate-led discipline says substrate VOTES on design decisions (doesn't get pre-imposed); the PHASE TIMING of substrate-voting changes between A and B but both honor the discipline:

- **Architecture A:** substrate votes at Phase 5 cohesion-coalescence (mechanical kit generated first; substrate selected based on accepted kit's signature)
- **Architecture B:** substrate votes at Phase 2 generation (substrate row pulled at generation time; informs all downstream decisions)

Both are substrate-led. Architecture B's substrate-voting happens EARLIER and provides RICHER signal throughout the pipeline.

Pattern 6 retirement (pre-imposed categorical axes) is satisfied by Architecture B because role-shape constraints have been REMOVED (per § 3 below). Pattern 6 was about pre-imposed categorical bias, not about substrate-binding timing.

### 2.4 Unified-architecture via substrate-genre-flagging (per Matt 2026-05-24 refinement)

Originally framed as dual-architecture (B for Reincarnated; A for marketable-product variant). Refined to: **Architecture B serves ALL products via substrate-genre-flagging.**

| Product | Substrate genre filter |
|---|---|
| Reincarnated v1 | `genre IN ('fantasy', 'mythological', 'historical')` |
| Future sci-fi cyberpunk product | `genre IN ('sci_fi', 'cyberpunk', 'modern_military')` |
| Future post-apoc product | `genre IN ('modern_military', 'post_apoc', 'survival')` |
| Profile B B2B SaaS | Client-provided genre-tagged substrate; engine flag controls |

Engine architecture stays single (Architecture B). Substrate library expansion + categorical genre-flagging supports all commercial profiles.

Cross-genre crossover (pirate-samurai-style cross-cultural in Reincarnated; cybered-samurai cross-genre in future product) handled by Pan-Fantasy / Hybrid bucket per Sketch D § 5.3.

---

## 3. Pattern 6 alignment — NO pre-imposed role-shape constraints

The previous Architecture A doc (now historical) included "role-shape constraints (damage/control/support/hybrid)" in Phase 2 generation. This was a pre-imposed categorical axis that contradicted Pattern 6 retirement (`canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md`).

**Architecture B removes role-shape constraints from Phase 2 generation.** Roles EMERGE from BC-coordinates implicitly:

| BC axis | Role-signal contribution |
|---|---|
| Axis 2A — Proxy density | High → summoner / proxy-master role |
| Axis 2B — Control density | High → control role |
| Axis 4 — Defensive profile | High + low damage → support / tank role |
| Axis 3B — Damage amplitude variance | High spiky → burst-damage role; low flat → sustained-damage role |
| Mixed signatures | → hybrid roles emerge from combinatorial profile |

**Role labels can be DESCRIPTIVELY assigned post-generation** via BC-cluster analysis if needed for player UI / strategy guides / etc. They are NOT pre-imposed generation constraints.

---

## 4. Empirical-trigger discipline for potential architecture switch

Architecture B is locked based on **hypothesis** (substrate-context-weight improves clustering + algorithmic outcomes). The hypothesis is reasonable + genre-canonical but not empirically validated yet. Per recognition-validate-commit discipline (gandalf OP § 3.4), we MUST design empirical triggers for potential future switch to Architecture A (developer-tool) or Architecture C (mid-bind hybrid).

### 4.1 Empirical triggers (post-engine-form-generation evidence)

| Trigger | What we'd observe |
|---|---|
| **Faction-emergence clustering quality** | Post-form generation cluster analysis: do bound-substrate forms cluster MORE coherently per cultural-tradition than mechanical-only would have? If NO, Architecture A's mechanical-only clustering may be sufficient |
| **Algorithm § 8 cultural-fit** | jack-ryan Gate-2 assessment + spot-check: do algorithm-derived mechanic-alterations feel cultural-tradition-fitted under B? If algorithm output feels MECHANICAL-ONLY (substrate-context not improving cultural-fit), B's benefit unconfirmed |
| **Player-experience signal (post-W1.13 baseline + post-T4-B post-mortem)** | Does player-perceived cultural-coherence improve under B vs hypothetical A baseline? Subjective signal; assessed at T4-B post-mortem |
| **Substrate-enrichment cost (v1.1+)** | Empirical cost of archive re-coalescence when substrate refreshes (Sidecar B / Track M1 / v1.1+). If cost is prohibitive, B's substrate-bound architecture may need refinement |
| **Phase 5 cohesion-judge LLM cost** | Per-form LLM cost at Phase 5 under B vs hypothetical A. If B's Phase 5 lighter LLM load doesn't materialize, B's benefit reduced |

### 4.2 Action on trigger fire

If any empirical trigger fires:
1. Recognition record authored at `canonical/story/architecture-b-empirical-trigger-fire-<YYYY-MM-DD>.md`
2. Pattern B design call (Matt + gandalf) re-evaluates architectural lock
3. Options at re-evaluation:
   - (a) Refine Architecture B (per-axis adjustment without architecture switch)
   - (b) Switch to Architecture C (mid-bind hybrid — substrate-cluster pulled at Phase 2; specific weapon at Phase 5)
   - (c) Switch to Architecture A (full substrate-agnostic)
   - (d) Hybrid implementation (use A in some scenarios; B in others)

### 4.3 Default — Architecture B holds

Without empirical-trigger fire, Architecture B stays locked. v1 ships under Architecture B; future products use Architecture B with genre-flagging.

---

## 5. Phase-by-phase deep dive

### 5.1 Phase 1 — Archive State Inspection

**Owner:** gamora

**Input:**
- Current mechanical-BC archive state (kits in archive per BC-coordinate)
- Substrate-coverage status per cell (v1_scope substrate availability per genre + cell-target)

**Action:**
- Identify sparse BC cells (cells under-represented in archive)
- Compute novelty + diversity needs
- Cross-reference substrate-coverage: cells with substrate-shortage flag for Sidecar B / Stage 3.5 enrichment

**Output:** BC-target queue (cells to fill, ranked by priority + substrate-coverage feasibility)

**Discipline:**
- Phase 1 doesn't queue cells where substrate-coverage is empty (Architecture B specific: if cell has no substrate to bind, engine can't generate — surface as enrichment-need feedback to substrate-curation)
- Architecture A's "explore mechanical-design space unconstrained" benefit is partially preserved here: Phase 1 outputs "BC-cells with mechanical-design feasibility but substrate-shortage" as separate signal for substrate-acquisition prioritization

### 5.2 Phase 2 — Generation (Substrate-Bound + Multi-T4 + Spec-Driven Gear)

**Owner:** rocket (with gandalf design-spec for cell-targeting + algorithm § 8 implementation + doc 40 gear/balance/guide commitments)

**Input:**
- BC-target coordinate [5-tuple: range × tempo × amplitude × attribute × proxy-density]
- Genre filter (per product configuration)
- v1_scope substrate (filtered by genre tag)
- Class chain count (doc 40 D83: T4 count = chain count - 1)
- Progression-node target (doc 40 D27 — early game / mid game / endgame start / endgame [85% target])

**Action (5 sub-phases per § 1 visual flow):**

#### 2a. Kit composition

1. **Compose skill kit matching cell**
   - Element coupling per attribute (per element_biases.py)
   - 10-15 node skill tree budget (skill-system § 1)
   - Mechanic-altering passives only (no filler)
   - Tier-1 rotation + tier-2 β-pair + tier-3 build-defining
   - **Max 8 active skills** (doc 40 D82 — flat budget)
   - **Chains organized for class chain count** (doc 40 D63-D64):
     - 3-chain class: 2 chains with T4 + 1 supporting T3 chain
     - 4-chain class: 3 chains with T4 + 1 supporting T3 chain
     - Supporting chains enable hybrid/multi-element builds per doc 40 D83

#### 2b. T4 algorithm (Algorithm § 8 — INDEPENDENT of gear per § 0.5 dependency chain)

2. **Generate T4 nodes per class chain count** (doc 40 D81 phased — all 4 phases wrap into Cycle 13):
   - **Phase 1:** T4s into chains as capstones; single T4 per chain initially
   - **Phase 2:** Multiple T4 options per chain with selection mechanic
   - **Phase 3:** Character-wide vs chain-wide scope dimension (biggest design risk)
   - **Phase 4:** Full simulation cycling through all T4 configurations during convergence
   - **Scored-candidate strategy registry (6 v1 strategies):** RESOURCE_CONVERSION / TRADE_OFF / ELEMENT_CONVERSION / DEFENSIVE_CONVERSION / GEOMETRY_COLLAPSE / DEFENSIVE_TRADEOFF
   - **DUAL mechanical impact per T4** (doc 40 D76):
     - Character-wide effect (kit-wide play feel shift)
     - Within-chain (or parallel-chain) effect
   - **INDEPENDENT of gear/legendaries** (per § 0.5 — algorithm operates on kit mechanics; gear is not an input)

#### 2c. Substrate binding (substrate weapon + secondary item)

3. **PULL specific substrate weapon from genre-filtered v1_scope** per cell-type matching policy:
   - **Option α (Martial cells — STR/DEX primary, physical-element):** 5-tuple mechanical-fingerprint match required; weapon-attack IS combat delivery
   - **Option β (Caster cells — INT/WIS primary, non-physical-element):** attribute-level match only; skills deliver kit BC-target; weapon scales
   - **Option C (Cross-attribute hybrid cells — Red Mage / Monk / Holy Knight):** cross-attribute wielding permitted with ω-penalty per BDI ω-field resource-dimension

4. **PULL specific substrate secondary item** (per off-hand-items canonical doc):
   - Categories: shield / tome / banner / focus / horn / talisman / weapon-integrated accessory / dual-wield secondary weapon
   - Per Main/Secondary slot architecture
   - Substrate-fit per parent-weapon compatibility (e.g., tsuba goes with katana)

#### 2d. Spec-driven gear generation (doc 40 D7 — depends on kit + T4 from 2a + 2b)

5. **Derive gear specifications from kit + T4 selection:**
   - Per-slot specification (which modifier types; what magnitudes)
   - Stat-sheet partition design applies (doc 40 D13-D14 + § 3.6 7-item scope per Matt 2026-05-26 amendment):
     1. Modifier surface enumeration
     2. Per-slot partition design
     3. Probability distribution per slot per modifier (gap-filling per D80)
     4. Node-count + chain-distribution interaction math
     5. Weapon damage spec completeness check (main + off-hand)
     6. Non-weapon gear baseline stats for common variants
     7. Main_weapon routing cleanup (substrate curation pollution)

6. **Generate gear instances at all rarity tiers** (doc 40 D8 — rarity IS power escalation):
   - **Common / Uncommon / Rare / Epic baseline** (kit-attuned; chain-aware; spec-driven; no T4-attunement)
   - **Legendary instances at 4 tiers** (doc 40 D50; tier 0 / 0.5 / 1 / 2):
     - Capability TOOLKIT at all tiers (doc 40 D9 + D54): multiplicative / mechanic-adjusting / spatial-adjusting / axis-adjusting / added-skill
     - HIGH PROBABILITY triggered-passive on weapons (doc 40 D55): "spawns tornadoes on wind hit", "shrapnel on physical hit", etc.
     - True actives EXTREMELY RARE + additive (weapons only)
     - Modifier-surface expansion over scalar (doc 40 D56): legendaries unlock NEW stat types Epic cannot roll
     - **T4-ATTUNEMENT annotation gate** (doc 40 D33 + D51): ONLY tier 1+2 legendaries carry T4-attunement; tier 0+0.5 carry capability toolkit but no T4-attunement
     - T4-attunement = multiplicative + mechanic-alteration on matching T4 path
   - **Unique instances at 4 tiers** (doc 40 D49)
   - **Set instances at 2 tiers** (doc 40 D48; endgame-only; always T4-attuned per D35)

7. **Apply drop pool restriction by content-tier** (doc 40 D50):
   - Tier 0 content: tier 0 legendaries only
   - Tier 0.5 content: tier 0 + 0.5 legendaries
   - Tier 1+2 content (endgame): all 4 tiers of legendaries

#### 2e. Coherence + faction

8. **Compose trait constellation**
9. **Apply ω-field + τ-field mechanical-coherence constraints** (per BDI ω/τ tables; skill-system § 11)
10. **Generate faction-proxy spawn-template per algorithm § 8.6**
    - Faction-anchor derived IMMEDIATELY from bound substrate weapon's cultural-tradition + period
    - Proxy-unit-pool enumerated per faction-anchor lookup
    - Available at Phase 2 because substrate is bound (key Architecture B benefit)

**Output:** complete mechanical kit + multi-T4 capstones + skill tree structure + bound substrate weapon + bound secondary item + gear specifications + gear instances at all rarities (incl. T4-attuned tier 1+2 legendaries + sets) + proxy-spawn-template + algorithm output bundle

**Disciplines:**
- **NO pre-imposed role-shape constraints** (per Pattern 6 retirement; per § 3 above)
- Substrate-agnostic mechanic pool at COMPOSITION level (skills + traits drawn from universal mechanical pool); substrate-binding at WEAPON+SECONDARY level
- Genre filter per product configuration; engine works for any genre-tagged substrate library
- **One-way dependency chain** (per § 0.5): T4 nodes INDEPENDENT of gear; gear depends on T4; legendaries depend on gear specs
- **Balance as PROPERTY not PROCESS** (per doc 40 D1): spec-driven generation; sim validates at generation time

### 5.3 Phase 3 — Convergence + Mechanical Measurement + Multi-T4 Sim Methodology + Playability Gate

**Owner:** gamora (with methodology consultation per Discipline #18; consultation fires BEFORE sim runs at scale)

**Input:** complete kit + multi-T4 capstones + bound substrate weapon + bound secondary item + gear instances at all rarities

**Action:** run simulation with SPECIFIC bound weapon's mechanical signature:
- Specific damage range / attack speed / geometry / amplitude variance / resource cost
- Converge modifier
- Measure 8 BC axes per BC-axes-lock doc

**Multi-T4 sim methodology** (doc 40 D84 — hybrid cohort + edge-case sampling with per-legendary anchoring):

1. Cycle each tier-2 legendary/set weapon
2. Determine cohort archetypes that would equip it (DPS-min-maxer / balanced / defensive / hybrid)
3. Map appropriate node configurations for cohort × weapon combinations:
   - **Sub-option A (per-weapon cohort coverage):** validate each legendary across all plausible cohorts. Higher compute, higher fidelity, lower bias risk. **Primary methodology.**
   - **Sub-option B (per-legendary cohort selection):** for each legendary, infer most-likely cohort from mechanics/stats; validate against that cohort only. Lower compute, higher bias risk. Fallback for compute-constrained scenarios.
   - **Hybrid-within-hybrid:** Sub-option A for ambiguous legendaries; Sub-option B for cohort-clear legendaries. Recommended starting point.
4. Sample PRE-EXISTING nodes (per § 0.5 — sim CONSUMES nodes; doesn't generate them)
5. Validate each attuned-T4 configuration independently per progression node

**Multi-node calibration** (doc 40 D27 — applies per kit's progression node target):
- Validate against power-band appropriate for kit's progression node
- Early game / mid game / endgame start / endgame [85% target]
- Multi-node WORK is post-Cycle-13 engine extension; Cycle 13 lays the foundations + validates per-node

**Playability gate** (doc 40 D61 — load-bearing validation criterion):
- KPM in target band for progression node
- Coherent skill rotation (not degenerate; not chaotic)
- Resource flow functional (mana/energy/cooldowns sustained-but-non-trivial)
- Defensive uptime adequate
- No degenerate states (stunlock / zero-damage void / mandatory-skill-locks)
- Visual/cognitive load manageable
- **PLAYABLE-AND-IN-BAND is the validation criterion** (not just numerical balance)

**Compute discipline** (doc 40 D62):
- Low-compute-yet-meaningful sim cycle is real constraint
- Stratified sampling / tiered validation / quick-estimate hybrid (per B14.5 V1 pattern) / caching
- Per gamora methodology consultation (Discipline #18 + OP § 4.2 refinement)

**Output:** kit + multi-T4 capstones + bound substrate + 8-axis BC coordinate per attuned-T4 configuration + per-tier WR + convergence data + playability gate disposition per cohort

**Discipline:**
- Sim realism = HIGHER than Architecture A (specific weapon vs abstract slot)
- Convergence per B14.5 V1 primary loop pattern
- Sim is CONSUMER per § 0.5 dependency chain (consumes pre-existing nodes + legendaries; does NOT generate them)

### 5.4 Phase 4 — Mechanical Archive Insertion

**Owner:** gamora

**Input:** kit + bound substrate + 8-axis BC coordinate

**Action:** math gates determine archive disposition (kit+substrate as unit):
- Pareto dominance check
- Crowding distance / hypervolume contribution
- Mahalanobis distance (duplicate detection)
- Information gain (KL) for novelty score
- Eviction rules if cell at capacity

**Output:** kit+substrate ACCEPTED (in archive) or REJECTED

**Discipline:**
- Archive entries include bound substrate (NOT just mechanical signature)
- Cluster analysis on archive uses bound substrate's cultural-tradition + period for faction-emergence (Architecture B specific benefit)

### 5.5 Phase 5 — Cohesion Coalescence

**Owner:** gandalf (cohesion-judge design + naming spec) + rocket (LLM call execution) + star-lord (LLM infrastructure)

**Input:** accepted kit + bound substrate + mechanical-BC coordinate

**Action:** LLM cohesion-judge confirms identity-narrative coherence + assigns flavor + naming. Substrate identity is ALREADY BOUND from Phase 2; cohesion-judge confirms + enriches:

1. **Confirm substrate-thematic fit** — cultural-tradition coherence between bound substrate and kit composition (mechanical signature + skill kit + traits should fit substrate's cultural-tradition; if mismatch, cohesion-judge can re-coalesce per Matt 2026-05-24 graduated-alignment discipline — drop named-bearer attribution if low alignment; engine-name original form)

2. **Sub-element flavor mapping** per Matt 2026-05-24 sub-element lock (renamed from "element canonical-pair" to disambiguate from retired seasonal-realm-mapping concept AND from legendary canonical-pair set-bonuses):
   - Core element stays stable (8 elements: physical / fire / water / earth / wind / lightning / holy / shadow)
   - Per-form sub-element manifestation at LLM-runtime per bound substrate's cultural-tradition
   - Examples: earth-element + necromancer engine-anchor → "Bone Spear / Bone Wall" (bone sub-element of earth); earth + Mexica engine-anchor → "Obsidian-Edge Cascade" (obsidian sub-element of earth); shadow + vampire engine-anchor → "Bat-Form Strike / Vampiric Drain" (vampiric sub-element of shadow)

3. **Bi-modal form-library assignment** per Sketch F + Matt 2026-05-24 universal-archetypal-naming lock:
   - Engine-internal named-personage substrate-anchor assigned at Phase 2 (per substrate's named-bearer attribution if applicable; ~32% named-personage / ~68% engine-named-original per bi-modal lock)
   - Player-facing layer UNIFORM archetypal naming regardless of engine-internal anchor

4. **Naming-space partitioning** per engine-anchor:
   - Cohesion-judge knows form's engine-internal anchor
   - Archetypal player-facing name avoids aggregate-signal-convergence to named-bearer canon
   - For Moctezuma-anchored form: avoid "Obsidian-Jaguar-Shadow-Eagle-Walker" piling up Aztec signals
   - For engine-named-original in adjacent cultural-tradition: use non-reserved naming patterns

5. **Nested mythology naming** (per skill-system § 12.4):
   - Tier-2 real-historical-person engine-anchor can invoke Tier-1 broadly-fictionalized mythological proxies
   - Example: engine-internal Moctezuma-anchor form summons Quetzalcoatl as Tier-1 named proxy (player sees "Lightning-Bird Deity" archetypal name at form layer + may see "Quetzalcoatl" or archetypal alternative at proxy-summon layer per per-tier discipline)

6. **Archetypal form name + skill names + spirit-guide explainer dialogue** per D7 AI-tell discipline:
   - Templated LLM with narrow blanks
   - Human-curated
   - Spirit-guide explainer fires if algorithmic mechanic-alteration is novel-to-this-kit (per skill-system § 9)

7. **Commit theme + flavor** (name, description, lore) per loot-architecture tier per bound substrate's Tier S/A/B/C:
   - Tier-S substrate → form instance is legendary-tier exemplar (named-mythological if Tier 1 Sketch F anchor; archetypal-rendered per universal naming)
   - Tier-A → rare-tier exemplar
   - Tier-B → magic-tier
   - Tier-C → common-tier

**Spirit-guide data-oracle integration** (doc 40 D28-D32 — additive to existing spirit-guide canon):

8. **Generate spirit-guide projection templates for kit+gear:**
   - **Per-T4 projection:** "T4-A projects KPM X at progression node Y"
   - **Per-content-tier projection:** "tier-1 content yields KPM, gear-power, set-probability tradeoffs"
   - **Per-legendary projection:** "legendary L advocates T4-Z; projected KPM if attuned is X (currently X')"
   - **Voice:** NEUTRAL OBSERVATION (data-oracle voice per D28), NOT evaluative counselor
   - **Language:** "projected to / typically / estimated" (D31 — projection honesty)
   - **Throne-resident framing** (D30) — composes with existing Heroic Spirit / spirit-guide canon
   - **Universal pattern across decision spaces** (D29) — content selection / T4 selection / gear loadout / etc. all use same data-presentation interface

**T4-attuned gear cohesion** (doc 40 D33-D39):

9. **Tier-1+2 legendary/set T4-attunement confirmation:**
   - Confirm T4-attunement aligns with kit's T4 paths (multiplicative + mechanic-alteration per matching T4)
   - Heroic Spirit narrative cohesion (D36): T4 paths = aspects of Spirit; T4-attuned gear = evidence of latent aspects
   - Sets: confirm set-level T4 attunement; multi-piece commitment for full bonuses (D35)
   - Persuasion-to-experiment surface (D34): spirit guide will use these cohesion outputs to present respec opportunities to players per doc 40 D65 mechanism

**Acquisition curve calibration** (doc 40 D21 — Option A):

10. **Generate calibrated drop rates per content tier:**
    - Drop rate = f(expected KPM × engagement distribution × target saturation curve per 85th-percentile cumulative target D18)
    - Pure RNG with calibrated rate (no smart-loot pity per D21)
    - Gap-filling discipline applies (D80) — drop calibration considers stat-sheet gap-filling probability per player accumulated loadout

**Output:** kit + multi-T4 capstones + bound substrate + coalesced identity + archetypal naming + spirit-guide projection templates + T4-attuned gear cohesion + acquisition curve calibration + flavor + element-pair mapping

### 5.6 Phase 6 — Visual Coalescence

**Owner:** galadriel

**Input:** fully-coalesced kit (mechanical + bound substrate + element-flavor + naming)

**Action:** CV-pipeline visual identity assignment:
- Per asset-pipeline § 3.6 verdict (Sidecar A MIXED outcome): image-pass-through-to-Meshy primary; ChatGPT-gen-to-Meshy fallback for substrate coverage gaps
- Per polearm aspect-ratio gate (v1.1+ Recognition 5)
- Per Meshy polygon-count delta diagnostic (v1.1+ Recognition 6)
- Control Rig / Niagara / PCG asset generation per architecture-validation spike acceptance

**Output:** kit + visual assets

### 5.7 Phase 7 — Joint-Gate Evaluation

**Owner:** gandalf + jack-ryan + Matt

**Input:** fully-coalesced + visualized kit

**Action:** Discipline #18 mechanical AND cohesion AND visual pass

**Output:** kit APPROVED for production or returned to specific phase for refinement

### 5.8 Phase 8 — Profile Assembly + Export

**Owner:** rocket (export pipeline) + star-lord (output / telemetry / LLM)

**Input:** approved kit

**Action:** filter by profile config (Reincarnated v1 vs future commercial profile per Variant C); format and ship

**Output:** shipped content (Reincarnated v1 player content; or future commercial profile content)

---

## 6. Composition with all session locks (per 2026-05-24)

This architecture composes with all 18 architectural locks from the Cycle 10 Stage 3 design call session:

| Lock | Where it integrates in Architecture B |
|---|---|
| 4-attribute system (STR/INT/WIS/DEX) | Phase 2 substrate-binding policy (Option α/β/C per attribute coupling) |
| 5-tuple BC-target subspace | Phase 1 BC-target queue + Phase 2 cell-targeting |
| 10-15 node skill tree | Phase 2 skill composition |
| Mechanic-altering passives only | Phase 2 passive composition |
| Algorithmic mechanic-alteration (skill-system § 8) | Phase 2 T4-build-defining-if-applicable |
| 8 core elements | Phase 2 element coupling + Phase 5 sub-element flavor |
| Architecture B substrate-as-base-type-templates + tiered-instance-loot | Phase 5 loot-architecture tier assignment per bound substrate's Tier S/A/B/C |
| Universal archetypal player-facing naming | Phase 5 cohesion-judge archetypal-naming discipline |
| Bi-modal form library (engine-layer discipline) | Phase 5 engine-internal vs player-facing layer separation |
| Sub-element flavor at LLM-runtime (renamed from "element canonical-pair flavor" 2026-05-24) | Phase 5 sub-element flavor mapping per substrate cultural-tradition |
| Legendary canonical-pair set-bonuses (DISTINCT concept from sub-element flavor; legitimate "canonical pair" usage for paired legendary items per Matt 2026-05-24 lock) | Phase 5 + loot-architecture (player-choice equip-both triggers set-bonus regime-change at gameplay) |
| Option α / Option β / Option C per cell-type matching | Phase 2 substrate-binding policy |
| Caster kit definition | Phase 2 Option β attribute-level match |
| Faction-generated proxies (skill-system § 8.6) | Phase 2 proxy-spawn-template (substrate's cultural-tradition + period immediately available) |
| Nested mythology naming (skill-system § 12.4) | Phase 5 per-tier discipline at proxy-named-entity level |
| Spirit-guide explainer pattern (skill-system § 9) | Phase 5 templated LLM call for algorithmic mechanic-alteration explainer |
| Naming-space partitioning per engine-anchor | Phase 5 cohesion-judge constraint at archetypal-naming layer |
| Substrate-genre-flagging | Phase 2 genre filter per product configuration (unified-architecture pattern per Matt 2026-05-24 refinement) |
| **Doc 40 — Balance as property (D1-D6)** | **Cross-cutting; Phase 2 spec-driven generation; Phase 3 validation-at-generation-time; balance-as-property principle propagates to every seam** |
| **Doc 40 — Spec-driven gear gen + rarity escalation + capability toolkit + tier structure (D7-D17, D48-D57)** | **Phase 2d (spec-driven gear generation sub-phase); gear specs derived from kit+T4; capability toolkit at all 4 legendary tiers; T4-attunement annotation gate on tier 1+2** |
| **Doc 40 — 85th-percentile cumulative target + Option A acquisition + multi-node calibration (D18-D27)** | **Phase 3 multi-node validation per kit's progression-node target; Phase 5 acquisition curve calibration** |
| **Doc 40 — Spirit guide as data-oracle (D28-D32)** | **Phase 5 spirit-guide projection template generation; universal data-presentation pattern across decision spaces** |
| **Doc 40 — T4-attuned gear intent (D33-D39)** | **Phase 2d T4-attunement annotation; Phase 5 T4-attuned gear cohesion; persuasion-to-experiment surface for spirit guide** |
| **Doc 40 — Peak-moment community layer (D40-D43)** | **Architectural intent; implementation phasing post-launch (NOT in Cycle 13 work scope)** |
| **Doc 40 — Auto-combat attribution correction (D44-D47)** | **Cross-cutting canonical correction; auto-combat NOT canonical for primary game; reserved as mobile-variant deferred option** |
| **Doc 40 — Multi-T4 architecture + T4 algorithm canonical form (D63-D86)** | **Phase 2a chain composition (3-chain class: 2+1 supporting; 4-chain class: 3+1 supporting per D83); Phase 2b T4 algorithm (all 4 phases in Cycle 13 per D81); Phase 3 multi-T4 sim methodology per D84; D65 respec-with-legendary-trigger mechanism integrates at Phase 5 cohesion → gameplay layer** |

---

## 7. What this doc does NOT do

- NOT a Phase 2 implementation spec — that's rocket-seam implementation work post-Cycle-10
- NOT a Phase 5 cohesion-judge calibration spec — that's P5 cohesion-judge calibration work
- NOT an algorithm § 8 implementation spec — that's rocket-seam algorithm-implementation work; per `agentic_orchestration/gandalf/requests/2026-05-24-knight-rider-t4-reframing-and-loadout-readiness.md`
- NOT a Phase 6 visual-coalescence implementation spec — that's drax + galadriel + Meshy/Niagara/PCG integration
- NOT a Phase 7-8 export/telemetry spec — that's star-lord + jack-ryan
- NOT a substrate-genre-flagging schema spec — that's elrond schema-design work post-Cycle-10
- NOT a final lock — Architecture B is empirically tested; per § 4 empirical-trigger discipline, switch to A or C remains possible

---

## 8. Cross-references

### Active project canon this doc grounds in
- `canonical/00-ground-state.md` § 1 (current truth oracle)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes; Phase 1 + 3 measure these)
- `canonical/story/skill-system-2026-05-24.md` (Phase 2 skill composition; algorithm § 8; § 8.6 faction-proxies; § 9 spirit-guide; § 12.4 nested mythology; § 13 Phase 2 generation flow — needs amendment to substrate-bound per this doc)
- `canonical/story/attribute-system-2026-05-24.md` (4-attribute system; Phase 2 element-attribute coupling)
- `canonical/story/off-hand-items-2026-05-24.md` (Phase 2 secondary-slot binding; companion-ref needs amendment to substrate-bound)
- `canonical/story/v1-bc-target-intent-2026-05-24.md` (Stage 0 cell-targeting; Phase 1 BC-target queue)
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` (Pattern 6 retirement — role-shape removal per § 3)
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` (genre context)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 7 (D7 AI-tell discipline; Phase 5 LLM curation)
- `canonical/37-engine-and-game-two-products.md` (Variant C engine-as-general-product; substrate-genre-flagging supports this)

### Historical / superseded
- `canonical/story/historical/qd-engine-end-to-end-workflow-A-substrate-agnostic-developer-tool-2026-05-21.md` (Architecture A; now developer-tool / R&D reference; superseded as production canonical by this doc)
- `canonical/story/historical/engine-architecture-vision-qd-profile-2026-05-19.md` (pre-Pattern-6-retirement vision)

### Live state references
- `~/Games/reincarnated-loadout/data/telemetry.db` — substrate DB with weapon_knowledge_entries + new fields per Cycle 10
- `~/Games/reincarnated-engine/src/reincarnated/generation/` — rocket-seam Phase 2 implementation territory (post-Cycle-10)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/` — gamora-seam Phase 3-4 territory
- `~/Games/reincarnated-engine/src/reincarnated/llm/` — star-lord-seam Phase 5 LLM-call infrastructure

### Downstream artifacts this doc anchors
- Composition policy canonical doc (post-D6 Stage 3 lock) — substrate-bound v1_scope per Architecture B
- Loot architecture canonical doc (post-Cycle-10 authoring) — Architecture B + loot-tier composition per § 5.5
- Sub-element architecture canonical doc (post-Cycle-10 authoring; renamed from "element canonical-pair flavor architecture") — Phase 5 sub-element flavor mapping per § 5.5
- Naming-space partitioning canonical doc (post-Cycle-10 authoring) — Phase 5 cohesion-judge constraint
- Algorithm § 8 implementation dispatch (post-Cycle-10 rocket seam) — substrate-bound at Phase 2
- Phase 5 cohesion-judge calibration spec (P5 territory) — per § 5.5

---

## 9. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-24 — Architecture B selected as primary production canonical with explicit hypothesis (substrate-context-weight benefit) + substrate-genre-flagging unified-architecture refinement; A archived as developer-tool / R&D reference
**Status:** CURRENT — production canonical engine architecture for Reincarnated v1 + all future commercial profiles via substrate-genre-flagging
**Re-engagement gate:** Empirical-trigger fire (per § 4) → Pattern B design call (Matt + gandalf) re-evaluates architectural lock

---

**Signed:** gandalf
**For:** the canonical production engine architecture (Architecture B — substrate-bound at Phase 2 + substrate-genre-flagging unified-architecture pattern) for Reincarnated v1 and all future commercial profiles per Matt 2026-05-24 architectural reversal during Cycle 10 Stage 3 design call. Supersedes Architecture A (substrate-AGNOSTIC) as production architecture; A retained as developer-tool / R&D reference.
