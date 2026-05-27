# 02 — Engine Build Roadmap (Visual-Flow Progress Tracker — Cycle 13 → Engine Completion → Reincarnated-Game Unlock)

> **STATUS:** CURRENT (load-bearing, **LIVING OPERATIONAL TRACKER**) — see `canonical/00-ground-state.md`
>
> **Living-doc protocol:** **knight-rider updates this doc at every commit during cycle execution** through engine build completion. gandalf authors structural changes (new phases, sub-phases, decision points landing in canonical architecture). jack-ryan reviews status transitions for discipline compliance.

**Date:** 2026-05-26 (initial authoring as engine build visual-flow tracker)
**Author:** gandalf (story-and-design steward; structural author)
**Operator:** knight-rider (cycle orchestrator; status updater)
**Authority:** Matt 2026-05-26 — directive to retire prior workstream-tracker roadmap and replace with operational engine-build-progress tracker structured around QD-engine workflow visual flow (per doc 39 § 1); knight-rider references and updates from hive-mind sessions through engine build completion and reincarnated-game unlock
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle; first read for every agent
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` — authoritative source for workflow architecture; this doc tracks EXECUTION against it
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — Cycle 13 architectural foundation; provides per-phase commitments tracked here
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone
- `canonical/historical/02-roadmap-workstream-tracker-2026-05-23.md` — predecessor (workstream-tracking layer; HISTORICAL — superseded by this doc)

---

## 0. TL;DR — what this doc is + how to read it

This doc is the **operational engine-build progress tracker** for Reincarnated. It mirrors the QD-engine workflow visual flow (per doc 39 § 1) and tracks per-phase + per-sub-phase execution status across the engine build through completion. Every commit during a hive-mind cycle updates this doc; over time it becomes the single-glance view of "how close are we to engine completion + reincarnated-game unlock."

**Read order for status check:**
1. § 1 Legend (icon meanings)
2. § 2 Top-line summary table (overall progress at a glance)
3. § 3 Full visual flow with per-phase + per-sub-phase status (detail)
4. § 4 Active workstream sequencing (what's in flight RIGHT NOW)
5. § 5 Deferred commitments + empirical-evidence gates (post-cycle-13 items)

**Read order for update (knight-rider):**
1. § 6 Update protocol (cadence + status-transition rules + commit-message conventions)
2. Update relevant row(s) in § 2 top-line + § 3 detail per commit
3. If structural change (new phase / new decision lands): flag gandalf for canonical authoring

---

## 1. Legend

| Icon | State | Meaning |
|---|---|---|
| ✅ | **COMPLETE** | Landed and verified (Gate-2 PASS or empirical-criterion satisfied) |
| ⏳ | **IN FLIGHT** | Currently being worked on; in-progress within a cycle |
| 🔄 | **ITERATING** | Initial landing complete; iteration / refinement continuing |
| ⚠️ | **NEEDS ATTENTION** | Blocker surfaced / pending decision / risk flagged / partial outcome requiring Tier-2 ratification |
| ❌ | **NOT YET STARTED** | Queued for future work; gated on upstream completion or Matt direction |
| 🔒 | **DEFERRED** | Architectural commitment locked but execution explicitly deferred (post-Cycle-13 or empirical-gated) |
| ⛔ | **BLOCKED** | Cannot proceed; explicit blocker requiring intervention |

---

## 2. Top-line summary — phase-level status

Quick status check at a glance. Detail per phase in § 3.

| # | Phase | Status | Owner(s) | Notes |
|---|---|---|---|---|
| — | Substrate Library | ✅ | elrond | v1_scope = 2,293 items LOCKED per Cycle 10 close 2026-05-25; tag `v1.0-weapon-substrate-cycle-10-shipped` |
| 1 | Archive State Inspection | ⏳ | gamora | Existing infrastructure operational; 4-progression-node coverage check (doc 40 D27) NOT YET added |
| 2 | Generation (5 sub-phases) | ⏳ | rocket | Cycle 12 Wave 2 in-flight; doc 40 commitments not yet implemented |
| 2a | — Kit Composition | ⏳ | rocket | Existing composition working; max-8-actives (D82) + chain architecture (D63-D64, D83) NOT YET applied |
| 2b | — T4 Algorithm (Algorithm § 8) | ⚠️ | rocket | § 8 implemented (Cycle 11); BC-shift sweep FAILED; Tier 2 ratified (ships as intent metadata); all 4 phases per D81 wrap into Cycle 13 |
| 2c | — Substrate Binding | ⏳ | rocket | Architecture B in-progress per Cycle 12 Layer 2 |
| 2d | — Spec-Driven Gear Gen | ❌ | rocket | Cycle 13 work; gates on stat-sheet partition cycle (D14 — early Cycle 13 milestone) |
| 2e | — Coherence + Faction | ⏳ | rocket | Cycle 12 Layer 4 (W1.13 multi-dim convergence) gates faction-proxy spawn-template integration |
| 3 | Convergence + Sim + Playability | ⏳ | gamora | W1.13 H1-H5 baseline DEFERRED to v1.1/Cycle 13+; multi-T4 sim methodology (D84) + playability gate (D61) NOT YET |
| 4 | Mechanical Archive Insertion | ⏳ | gamora | Existing math gates operational; integration with multi-T4 archive entries pending |
| 5 | Cohesion Coalescence | ❌ | gandalf + rocket + star-lord | P5 cohesion-judge calibration spec QUEUED post-Cycle-10; spirit-guide data-oracle integration (D28-D32) + T4-attuned gear cohesion (D33-D39) + acquisition curve calibration (D21) NOT YET |
| 6 | Visual Coalescence | ⏳ | galadriel | Asset pipeline partial; image-pass-through-to-Meshy verdict from Sidecar A; remaining acceptance criteria QUEUED |
| 7 | Joint-Gate Evaluation | 🔄 | gandalf + jack-ryan + Matt | Ongoing per cycle; iterative |
| 8 | Profile Assembly + Export | ⏳ | rocket + star-lord | Loadout app M3 + M4 + M6 landed Cycle 11; M1 + M2 + M5 pending Cycle 12 Layer 2 schema extensions |

**Overall engine completion status (2026-05-26):** Cycle 12 in-flight (Wave 2). Cycle 13 architectural foundation locked (docs 39 + 40). T4 PM1 gated on Cycle 12 close. Cycle 13 execution gated on T4 PM1.

**CYCLE-TO-PHASE MAPPING (per Matt 2026-05-26 clarification):**

| Cycle | Phases addressed | Output milestone |
|---|---|---|
| **Cycle 13** | Phase 1 + Phase 2 (all sub-phases) + Phase 3 + Phase 4 (archive insertion auto on sim PASS) | **Mechanical validation complete: gauntlet sim PASS against full new architecture + initial mechanical season generation (kits + T4 + gear + sim-validated; no cohesion / no visuals / no export). All characters produced within WR bracket per Matt 2026-05-26 Q10 amendment.** |
| **Cycle 14** (LOCKED Pattern A per Matt 2026-05-26) | Phase 5 Cohesion Coalescence (P5 calibration + spirit-guide data-oracle + T4-attuned gear cohesion + acquisition curve calibration) | Cohesion layer complete; content has narrative identity + naming + spirit-guide projections |
| **Cycle 15** (LOCKED Pattern A) | Phase 6 Visual Coalescence (CV pipeline + Meshy + Control Rig / Niagara / PCG) | Visual layer complete; content has assets |
| **Cycle 16** (LOCKED Pattern A) | Phase 7 Joint-Gate Evaluation + Phase 8 Profile Assembly + Export | Full pipeline; engine ships content |
| **Engine build COMPLETE** | All Phases 1-8 = ✅ | **REINCARNATED-GAME UNLOCK** milestone fires |

Cycle 13 produces **mechanically-validated content** but NOT **game-ready content**. Reincarnated-game unlock requires the full pipeline (phases 5-8) to land in subsequent cycles.

---

## 3. Full visual flow with per-line status (ASCII visual format per Matt 2026-05-26 directive)

The complete QD-engine workflow per doc 39 § 1, with status icons inline at each line + completion dates on green checks where known. **Update rule:** find the line, replace the icon, add date if ✅. When sub-phase status aggregates change, update § 2 top-line summary also.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ ✅ 2026-05-25  SUBSTRATE LIBRARY (multi-genre via genre-flagging)                            │
│  ✅ 2026-05-22  - weapon_knowledge_entries (89,839 rows) + off-hand items (Sidecar B)        │
│  ✅            - genre tag per row (fantasy / sci-fi / cyberpunk / post-apoc / etc.)         │
│  ✅            - cultural_lineage_canonical + historical_period_canonical                    │
│  ✅            - named-bearer attribution (Track M1 / sub-agent gandalf seed list)           │
│  ✅            - Tier S/A/B/C composite quality scoring                                      │
│  ✅ 2026-05-25  - v1_scope = 2,293 items LOCKED (tag v1.0-weapon-substrate-cycle-10-shipped) │
└────────────────────────────────────┬─────────────────────────────────────────────────────────┘
                                     │ (CONSUMED at Phase 2; substrate-bound generation)
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⏳  PHASE 1: ARCHIVE STATE INSPECTION (gamora)                                               │
│  Input:                                                                                      │
│    ✅            - current mechanical-BC archive state                                       │
│    ✅            - substrate-coverage status                                                 │
│  Action:                                                                                     │
│    ✅            - identify sparse cells                                                     │
│    ✅            - compute novelty + diversity needs                                         │
│    ✅            - check substrate-coverage at 4-tuple level per cell                        │
│    ❌            - check 4 progression-node coverage (doc 40 D27): early game / mid game /   │
│                    endgame start / endgame [85% target]                              [NEW]   │
│  Output:                                                                                     │
│    ⏳            - BC-target queue (cells to fill, ranked by priority + substrate-coverage   │
│                    feasibility + progression-node coverage)                                  │
└────────────────────────────────────┬─────────────────────────────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⏳  PHASE 2: GENERATION (BC-TARGET-DRIVEN + SUBSTRATE-BOUND + DOC-40 MULTI-T4 +              │
│           SPEC-DRIVEN GEAR) (rocket)                                                         │
│                                                                                              │
│  Input:                                                                                      │
│    ✅            - BC-target coordinate [5-tuple: range × tempo × amplitude × attribute ×    │
│                    proxy-density]                                                            │
│    ✅            - Genre filter (per product)                                                │
│    ❌            - Class chain count (doc 40 D83: T4 count = chain count - 1)        [NEW]   │
│    ❌            - Progression-node target (doc 40 D27)                              [NEW]   │
│                                                                                              │
│  ┌─────────────────── ⏳  2a. KIT COMPOSITION ────────────────────────────────────────────┐ │
│  │ 1. Compose skill kit matching cell                                                       │ │
│  │    ✅            - 10-15 node skill tree budget (skill-system § 1)                       │ │
│  │    ✅            - Element coupling per attribute (element_biases.py)                    │ │
│  │    ✅            - Mechanic-altering passives only (no filler)                           │ │
│  │    ⏳            - Tier-1 rotation + tier-2 β-pair + tier-3 build-defining               │ │
│  │    ❌            - Max 8 active skills (doc 40 D82; flat budget)               [NEW]    │ │
│  │    ❌            - Chains organized for class chain count (doc 40 D63-D64)     [NEW]    │ │
│  │                    • 3-chain class: 2 chains with T4 + 1 supporting T3 chain             │ │
│  │                    • 4-chain class: 3 chains with T4 + 1 supporting T3 chain             │ │
│  │                    • Supporting chains enable hybrid/multi-element builds (D83)          │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────── ⚠️  2b. T4 ALGORITHM (Algorithm § 8) ─────────────────────────────────┐ │
│  │ 2. Generate T4 nodes per class chain count (doc 40 D81 phased):                          │ │
│  │    ✅ 2026-05-25 - Algorithm § 8 scored-candidate strategy registry (commit 3430269)     │ │
│  │    ✅            - 6 v1 strategies: RESOURCE_CONVERSION / TRADE_OFF /                    │ │
│  │                    ELEMENT_CONVERSION / DEFENSIVE_CONVERSION / GEOMETRY_COLLAPSE /       │ │
│  │                    DEFENSIVE_TRADEOFF                                                    │ │
│  │    ⚠️            - BC-shift validation sweep FAILED Cycle 11; Tier 2 ratified            │ │
│  │                    (ships as intent metadata + spirit-guide narration + loadout display) │ │
│  │    ❌            - Layer 6 wire-up (alterations → combat arithmetic; Cycle 12 Wave 4)    │ │
│  │    All 4 phases of T4 algorithm wrap into Cycle 13 (doc 40 D81 + D85):                  │ │
│  │    ❌            • Phase 1: T4s into chains as capstones (single T4/chain)     [NEW]    │ │
│  │    ❌            • Phase 2: Multiple T4 options per chain with selection      [NEW]    │ │
│  │    ❌            • Phase 3: Character-wide vs chain-wide scope dimension       [NEW]    │ │
│  │    ❌            • Phase 4: Full sim cycling through all T4 configurations    [NEW]    │ │
│  │    ❌            - DUAL mechanical impact per T4 (doc 40 D76):                 [NEW]    │ │
│  │                    • Character-wide effect (kit-wide play feel shift)                    │ │
│  │                    • Within-chain (or parallel-chain) effect                             │ │
│  │    ✅ 2026-05-26 - INDEPENDENT of gear/legendaries (per doc 39 § 0.5 dependency chain)   │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────── ⏳  2c. SUBSTRATE BINDING ─────────────────────────────────────────────┐ │
│  │ 3. PULL specific substrate weapon from genre-filtered v1_scope:                          │ │
│  │    ✅ 2026-05-24 - Option α (Martial cell): 5-tuple mechanical-fingerprint match         │ │
│  │    ✅ 2026-05-24 - Option β (Caster cell): attribute-level match only                    │ │
│  │    ✅ 2026-05-24 - Option C (Hybrid cell): cross-attribute with ω-penalty                │ │
│  │    ⏳            - Substrate weapon PULL operational (Cycle 12 Layer 2 in-flight)        │ │
│  │ 4. PULL specific substrate secondary item per off-hand-items canonical doc:              │ │
│  │    ⏳            - Substrate secondary-item PULL (Cycle 12 Layer 2 in-flight)            │ │
│  │                    (shield / tome / banner / focus / horn / talisman /                   │ │
│  │                     weapon-integrated accessory / dual-wield secondary weapon)           │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────── ❌  2d. SPEC-DRIVEN GEAR GEN (doc 40 D7) — ALL NEW ────────────────────┐ │
│  │ 5. Derive gear specifications from kit + T4 selection:                                   │ │
│  │    ❌            - Per-slot specification (which modifier types; what magnitudes)        │ │
│  │    Stat-sheet partition design (doc 40 D13-D14 + § 3.6 7-item scope):                   │ │
│  │    ❌            - 1. Modifier surface enumeration                                       │ │
│  │    ❌            - 2. Per-slot partition design                                          │ │
│  │    ❌            - 3. Per-slot probability distribution (gap-filling per D80)            │ │
│  │    ❌            - 4. Node-count + chain-distribution interaction math                   │ │
│  │    ❌            - 5. Weapon damage spec completeness (main + off-hand)                  │ │
│  │    ❌            - 6. Non-weapon gear baseline stats for common variants                 │ │
│  │    ❌            - 7. Main_weapon routing cleanup (substrate curation pollution)         │ │
│  │ 6. Generate gear instances at all rarity tiers (doc 40 D8):                              │ │
│  │    ❌            - Common / Uncommon / Rare / Epic baseline (kit-attuned; chain-aware)   │ │
│  │    ❌            - Legendary instances at 4 tiers (doc 40 D50; tier 0/0.5/1/2):          │ │
│  │                    ┌─ ❌ Capability TOOLKIT at all tiers (doc 40 D9 + D54):              │ │
│  │                    │    multiplicative / mechanic-adjusting / spatial-adjusting /        │ │
│  │                    │    axis-adjusting / added-skill                                     │ │
│  │                    ├─ ❌ HIGH PROBABILITY triggered-passive on weapons (doc 40 D55):     │ │
│  │                    │    (e.g., "spawns tornadoes on wind hit"; "shrapnel on phys")       │ │
│  │                    │    - True actives EXTREMELY RARE + additive (weapons only)          │ │
│  │                    ├─ ❌ Modifier-surface expansion over scalar (doc 40 D56):            │ │
│  │                    │    legendaries unlock NEW stat types Epic cannot roll               │ │
│  │                    └─ ❌ T4-ATTUNEMENT annotation gate (doc 40 D33 + D51):               │ │
│  │                         ONLY tier 1+2 legendaries carry T4-attunement;                   │ │
│  │                         tier 0+0.5 carry capability toolkit but no T4-attunement;        │ │
│  │                         attunement = multiplicative + mechanic-alteration on             │ │
│  │                         matching T4 path                                                 │ │
│  │    ❌            - Unique instances at 4 tiers (doc 40 D49)                              │ │
│  │    ❌            - Set instances at 2 tiers (doc 40 D48; endgame-only; T4-attuned D35)   │ │
│  │ 7. Drop pool restriction by content-tier (doc 40 D50):                                   │ │
│  │    ❌            - Tier 0 content: tier 0 legendaries only                               │ │
│  │    ❌            - Tier 0.5 content: tier 0 + 0.5 legendaries                            │ │
│  │    ❌            - Tier 1+2 content (endgame): all 4 tiers of legendaries                │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────── ⏳  2e. COHERENCE + FACTION ───────────────────────────────────────────┐ │
│  │ 8.  ⏳            Compose trait constellation (Cycle 12 integration pending)             │ │
│  │ 9.  ✅            Apply ω-field + τ-field mechanical-coherence constraints               │ │
│  │ 10. ⏳            Generate faction-proxy spawn-template per algorithm § 8.6              │ │
│  │     ✅            (faction-anchor derived from substrate weapon's cultural-tradition +   │ │
│  │                    period — IMMEDIATELY AVAILABLE at Phase 2 per Architecture B)         │ │
│  └─────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                              │
│  Output: complete mechanical kit + multi-T4 capstones + skill tree structure +               │
│          bound substrate weapon + bound secondary item + gear specifications +               │
│          gear instances at all rarities (incl. T4-attuned tier 1+2 legendaries +             │
│          sets) + proxy-spawn-template + algorithm output bundle                              │
│                                                                                              │
│  Disciplines:                                                                                │
│    ✅            - NO pre-imposed role-shape constraints (per Pattern 6 retirement)          │
│    ✅            - Roles EMERGE from BC-coordinates implicitly                               │
│    ✅ 2026-05-26 - One-way dependency chain (per doc 39 § 0.5): T4 nodes INDEPENDENT of gear │
│    ✅ 2026-05-26 - Balance as PROPERTY not PROCESS (per doc 40 D1)                           │
│    ✅ 2026-05-26 - Spec-driven generation; sim validates at generation time (D7 + D1)        │
└────────────────────────────────────┬─────────────────────────────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⏳  PHASE 3: CONVERGENCE + MECHANICAL MEASUREMENT (gamora) + MULTI-T4 SIM METHODOLOGY        │
│           (per doc 40 D84) + PLAYABILITY GATE                                                │
│                                                                                              │
│  Input:                                                                                      │
│    ✅            - complete kit + multi-T4 capstones + bound substrate                       │
│    ⏳            - gear instances at all rarities (gates on Phase 2d completion)             │
│                                                                                              │
│  Action: run simulation with SPECIFIC bound weapon's mechanical signature                    │
│                                                                                              │
│    ✅ 2026-05-20 - 8 BC axes measurement (per qd-engine-bc-axes-lock-2026-05-20.md):         │
│                    ┌─ Axis 1 — Engagement profile (range × mobility)                         │
│                    ├─ Axis 2 — Damage geometry (single/AOE/chain/multi-spawn)                │
│                    ├─ Axis 2A — Proxy density                                                │
│                    ├─ Axis 2B — Control density                                              │
│                    ├─ Axis 3A — Damage tempo                                                 │
│                    ├─ Axis 3B — Damage amplitude variance                                    │
│                    ├─ Axis 4 — Defensive profile                                             │
│                    └─ Axis 5 — Resource economy                                              │
│    ✅            - Convergence per B14.5 V1 primary loop pattern                             │
│    🔒            - W1.13 H1-H5 baseline (DEFERRED v1.1/Cycle 13+ per Option γ confirmation)  │
│                                                                                              │
│  Multi-T4 sim methodology (doc 40 D84 — hybrid cohort + edge-case):                          │
│    ❌            - Cycle each tier-2 legendary/set weapon                          [NEW]    │
│    ❌            - Determine cohort archetypes that would equip it                 [NEW]    │
│                    (DPS-min-maxer / balanced / defensive / hybrid)                           │
│    ❌            - Map node configurations for cohort × weapon                     [NEW]    │
│                    • Sub-option A: per-weapon cohort coverage (primary)                      │
│                    • Sub-option B: per-legendary cohort selection (compute fallback)         │
│                    • Hybrid-within-hybrid: A for ambiguous; B for cohort-clear               │
│    ❌            - Sample PRE-EXISTING nodes (doc 39 § 0.5 — sim CONSUMES, doesn't gen)      │
│    ❌            - Validate each attuned-T4 configuration independently per node             │
│                                                                                              │
│  Multi-node calibration (doc 40 D27):                                                        │
│    ❌            - Validate against power-band appropriate for kit's progression node        │
│                    (early game / mid game / endgame start / endgame [85% target])            │
│                                                                                              │
│  Playability gate (doc 40 D61 — load-bearing validation criterion):                          │
│    ❌            - KPM in target band for progression node                          [NEW]   │
│    ❌            - Coherent skill rotation (not degenerate; not chaotic)            [NEW]   │
│    ❌            - Resource flow functional (mana/energy/cooldowns)                 [NEW]   │
│    ❌            - Defensive uptime adequate                                        [NEW]   │
│    ❌            - No degenerate states (stunlock / zero-damage / mandatory locks)  [NEW]   │
│    ❌            - Visual/cognitive load manageable                                 [NEW]   │
│    ❌            - PLAYABLE-AND-IN-BAND is the validation criterion                 [NEW]   │
│                                                                                              │
│  Compute discipline (doc 40 D62):                                                            │
│    ❌            - Stratified sampling / tiered validation / quick-estimate hybrid /         │
│                    caching per gamora methodology consultation (Discipline #18)              │
│                                                                                              │
│  Output: kit + multi-T4 capstones + bound substrate + 8-axis BC coordinate per               │
│          attuned-T4 configuration + per-tier WR + convergence data + playability             │
│          gate disposition per cohort                                                         │
└────────────────────────────────────┬─────────────────────────────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⏳  PHASE 4: MECHANICAL ARCHIVE INSERTION (gamora)                                           │
│  Input:                                                                                      │
│    ✅            - kit + bound substrate + 8-axis BC coordinate                              │
│  Action: math gates determine archive disposition                                            │
│    ✅            - Pareto dominance check (kit+substrate as unit)                            │
│    ✅            - Crowding distance / hypervolume contribution                              │
│    ✅            - Mahalanobis distance (duplicate detection)                                │
│    ✅            - Information gain (KL) for novelty score                                   │
│    ✅            - Eviction rules if cell at capacity                                        │
│    ✅            - Archive entries include bound substrate (per Architecture B)              │
│    ❌            - Multi-T4 archive entries (per attuned-T4 configuration)        [NEW]    │
│  Output:                                                                                     │
│    ⏳            - kit+substrate ACCEPTED (in archive) or REJECTED                           │
└────────────────────────────────────┬─────────────────────────────────────────────────────────┘
                                     │ (if ACCEPTED)
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ ❌  PHASE 5: COHESION COALESCENCE (gandalf cohesion + rocket LLM call) +                     │
│          SPIRIT-GUIDE DATA-ORACLE INTEGRATION (doc 40 D28-D32) +                            │
│          T4-ATTUNED GEAR COHESION (doc 40 D33-D39)        [CYCLE 14]                        │
│                                                                                              │
│  Input:                                                                                      │
│    ❌            - accepted kit + multi-T4 capstones + gear instances at all rarities        │
│                    + bound substrate + mechanical-BC coordinate                              │
│                                                                                              │
│  Action: LLM cohesion-judge confirms identity-narrative coherence + flavor + naming          │
│    ⏳            - confirm substrate-thematic fit (cultural-tradition coherence)             │
│    ⏳            - sub-element flavor mapping per element + bound substrate                  │
│    ✅ 2026-05-24 - bi-modal form-library assignment (Sketch F + universal-archetypal)        │
│    ⏳            - naming-space partitioning per engine-anchor                               │
│    ⏳            - nested mythology naming (Tier-2 invokes Tier-1; skill-system § 12.4)      │
│    ⏳            - archetypal form name + skill names per D7 AI-tell discipline              │
│    ⏳            - commit theme + flavor per loot-architecture tier                          │
│    ❌            - P5 cohesion-judge calibration spec (QUEUED post-Cycle-10 authoring)       │
│                                                                                              │
│  Spirit-guide data-oracle integration (doc 40 D28-D32):                                      │
│    ❌            - Generate spirit-guide projection templates for kit+gear:        [NEW]    │
│                    • Per-T4 projection: "T4-A projects KPM X at node Y"                      │
│                    • Per-content-tier projection: "tier-1 yields KPM, gear-pwr, set-prob"    │
│                    • Per-legendary projection: "legendary L advocates T4-Z; KPM X if attuned"│
│    ❌            - Voice: NEUTRAL OBSERVATION (data oracle, NOT counselor) (D28)   [NEW]    │
│    ❌            - Language: "projected to / typically / estimated" (D31 honesty)  [NEW]    │
│    ❌            - Throne-resident framing per existing spirit-guide canon (D30)   [NEW]    │
│    ❌            - Universal pattern across decision spaces (D29)                  [NEW]    │
│                                                                                              │
│  T4-attuned gear cohesion (doc 40 D33-D39):                                                  │
│    ❌            - Tier-1+2 legendary/set T4-attunement alignment confirmation     [NEW]    │
│    ❌            - Heroic Spirit narrative cohesion (T4 paths = aspects of Spirit) [NEW]    │
│    ❌            - Sets: set-level T4 attunement confirmation                      [NEW]    │
│    ❌            - Persuasion-to-experiment surface for spirit guide               [NEW]    │
│                                                                                              │
│  Acquisition curve calibration (doc 40 D21):                                                 │
│    ❌            - Option A calibrated drop rates per content tier                 [NEW]    │
│    ❌            - Drop rate = f(KPM × engagement distribution × 85th-percentile)  [NEW]    │
│    ❌            - Pure RNG with calibrated rate (no smart-loot pity per D21)      [NEW]    │
│    ❌            - Gap-filling discipline (D80) — drop calibration accounts for gaps[NEW]   │
│                                                                                              │
│  Output: kit + multi-T4 capstones + bound substrate + coalesced identity + archetypal        │
│          naming + spirit-guide projection templates + T4-attuned gear cohesion +             │
│          acquisition curve calibration + flavor + element-pair mapping                       │
└────────────────────────────────────┬─────────────────────────────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⏳  PHASE 6: VISUAL COALESCENCE (galadriel)        [CYCLE 15]                                │
│  Input:                                                                                      │
│    ❌            - fully-coalesced kit                                                       │
│  Action: CV-pipeline visual identity assignment                                              │
│    ✅            - image-pass-through-to-Meshy primary (asset-pipeline § 3.6 verdict)        │
│    ⏳            - ChatGPT-gen-to-Meshy fallback (substrate coverage gaps)                   │
│    🔒            - Polearm aspect-ratio gate (DEFERRED v1.1+ Recognition 5)                  │
│    🔒            - Meshy polygon-count delta diagnostic (DEFERRED v1.1+ Recognition 6)       │
│    ⏳            - Control Rig / Niagara / PCG asset generation                              │
│                    (per architecture-validation spike acceptance criteria 3.1/3.2/3.4/       │
│                     3.5/3.6 — queued)                                                        │
│  Output:                                                                                     │
│    ⏳            - kit + visual assets                                                       │
└────────────────────────────────────┬─────────────────────────────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🔄  PHASE 7: JOINT-GATE EVALUATION (gandalf + jack-ryan + Matt)   [CYCLE 16]                 │
│  Input:                                                                                      │
│    ⏳            - fully-coalesced + visualized kit                                          │
│  Action:                                                                                     │
│    🔄            - Discipline #18 mechanical AND cohesion AND visual pass                    │
│    🔄            - Per-cycle Gate-2 critique-pair throughput (operating)                     │
│  Output:                                                                                     │
│    🔄            - kit APPROVED for production or returned to specific phase                 │
└────────────────────────────────────┬─────────────────────────────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ ⏳  PHASE 8: PROFILE ASSEMBLY + EXPORT (rocket + star-lord)   [CYCLE 16]                     │
│  Input:                                                                                      │
│    ⏳            - approved kit                                                              │
│  Action:                                                                                     │
│    ⏳            - filter by profile config (Reincarnated v1 vs future commercial profile)   │
│    ✅ 2026-05-25 - Loadout app M3 (loadout display) shipped Cycle 11 Wave 3b                 │
│    ✅ 2026-05-25 - Loadout app M4 (T4 narration) shipped Cycle 11                            │
│    ✅ 2026-05-25 - Loadout app M6 (spirit-guide narration) shipped Cycle 11 Wave 3b          │
│    ❌            - Loadout app M1 (schema extension consumer; Cycle 12 Layer 2 gates)        │
│    ❌            - Loadout app M2 (schema extension consumer; Cycle 12 Layer 2 gates)        │
│    ❌            - Loadout app M5 (schema extension consumer; Cycle 12 Layer 2 gates)        │
│    ⏳            - Format + ship pipeline (per-product profile filtering operational)        │
│  Output:                                                                                     │
│    ⏳            - shipped content                                                           │
└──────────────────────────────────────────────────────────────────────────────────────────────┘

                                          ▼
                              ╔══════════════════════════╗
                              ║  ❌  ENGINE BUILD        ║
                              ║      COMPLETE            ║
                              ║                          ║
                              ║   →  REINCARNATED-GAME   ║
                              ║      UNLOCK milestone    ║
                              ╚══════════════════════════╝
```

**Cycle attribution:** [CYCLE 13] = Phases 1-3 + Phase 4. [CYCLE 14] = Phase 5. [CYCLE 15] = Phase 6. [CYCLE 16] = Phase 7+8 → engine build COMPLETE → REINCARNATED-GAME UNLOCK milestone.

---

## 4. Active workstream sequencing

What's in flight RIGHT NOW + what fires next.

### 4.1 Cycle 12 — v1 full new engine parallel-build (Option γ)

| Wave | Status | Detail |
|---|---|---|
| Wave 0/0.5 — prereq clearance | ✅ | jack-ryan Gate-1 + legolas MC-1/MC-2 + gandalf comp-policy + elrond pre-Layer-2 + SC-1/SC-2 |
| Wave 1 — rocket L2 + L3 | ✅ | Both jack-ryan Gate-2 PASS; CRITICAL VELOCITY ANOMALY (1 hour vs 4-6 weeks estimated) |
| Wave 2 — Gate-2 on L2 + MC-3 parallel | ⏳ | IN FLIGHT 2026-05-25 |
| Wave 3 — rocket Layer 4 (W1.13 multi-dim convergence) | ❌ | QUEUED |
| Wave 4 — rocket Layer 6 (§ 8 wire-up + L9 opportunity-scan refactor) | ❌ | QUEUED |
| Wave 5 — integration smoke + jack-ryan Gate-2 + KR auto-close | ❌ | QUEUED |

**Gate to T4 PM1:** Cycle 12 closes → engine generates ~30-40 v1 forms via new engine layers → forms upload into loadout app → T4 PM1 fires.

### 4.2 T4 PM1 — Post-Cycle-12 design call (Matt + gandalf)

| Item | Status | Detail |
|---|---|---|
| Prep doc | ✅ | `agentic_orchestration/gandalf/notes/2026-05-26-t4-post-mortem-session-1-prep.md` |
| Architectural foundation locked (doc 40) | ✅ | 2026-05-26 |
| Session execution | ❌ | Gates on Cycle 12 close + form-generation milestone |
| Output → Cycle 13 scope-doc inputs | ❌ | Post-T4-PM1 |

### 4.3 Cycle 13 — Mechanical Engine Build (Phases 1-3 of QD-engine workflow)

**Scope (per Matt 2026-05-26 clarification):** Cycle 13 addresses Phases 1, 2, 3 of the QD-engine workflow (per doc 39) culminating in gauntlet battle sim PASS + initial mechanical season generation. Phases 5-8 (cohesion + visual + gate + export) are SUBSEQUENT cycles. Phase 4 (mechanical archive insertion) completes automatically on sim PASS within Cycle 13.

**Out of scope for Cycle 13** (explicit; for subsequent cycles):
- Phase 5 cohesion coalescence (P5 cohesion-judge calibration + spirit-guide data-oracle integration + T4-attuned gear cohesion + acquisition curve calibration)
- Phase 6 visual coalescence
- Phase 7 joint-gate evaluation refinement
- Phase 8 profile assembly + export to game-ready format

| Item | Status | Detail |
|---|---|---|
| Architectural foundation (docs 38 + 39 + 40) | ✅ | Landed 2026-05-26 |
| Cycle 13 framing brief (gandalf) | ✅ | RATIFIED 2026-05-26 (Matt ratified Q1-Q11 in full); canonical authority basis for scope-doc + KR kicker; `agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-framing-brief.md` |
| T4 PM1 design session | ❌ | Gates on Cycle 12 close + form-generation milestone |
| Cycle 13 scope-doc authoring (gandalf 4-8 hrs per D85) | ❌ | Gates on T4 PM1 completion |
| Stat-sheet partition design cycle (multi-seam early Cycle 13 milestone) | ❌ | Gates on Cycle 13 launch + Discipline #18 methodology consultation |
| Gamora methodology consultation (D60 + D74 + D84) | ❌ | Gates partition cycle + gauntlet sim |
| Phase 1 T4 algorithm implementation (T4s into chains as capstones) | ❌ | Per doc 40 D81 Phase 1; gates on T4 PM1 + scope-doc |
| Phase 2 T4 algorithm implementation (multiple T4 options per chain) | ❌ | Per doc 40 D81 Phase 2; sequenced after Phase 1 |
| Phase 3 T4 algorithm implementation (character-wide vs chain-wide dimension) | ❌ | Per doc 40 D81 Phase 3; sequenced after Phase 2 |
| Phase 4 T4 algorithm implementation (full sim cycling) | ❌ | Per doc 40 D81 Phase 4; sequenced after Phase 3 |
| Spec-driven gear gen implementation (Phase 2d of workflow) | ❌ | Per doc 40 D7; gates on partition cycle |
| Gauntlet battle sim against full architecture | ❌ | **Cycle 13 culmination milestone**; sequenced after T4 4-phase implementation + spec-driven gear gen + partition |
| Initial mechanical season generation | ❌ | **Cycle 13 final demonstration**; produces sim-validated mechanical content for one season's worth of kits + gear |
| (DEFERRED) Drax integration | 🔒 | Deferred to post-Cycle-13 cycle that handles Phase 5+ (UX needs cohesion outputs to consume) |

---

## 5. Deferred commitments + empirical-evidence gates

Architectural commitments locked but execution DEFERRED. Each lists the empirical-evidence criterion that gates re-engagement.

| Commitment | Locked in | Empirical-evidence gate |
|---|---|---|
| Pattern B pre-gen library (doc 40 D2) | Doc 40 § 2.2 | Post-Cycle-13 engine maturity; sustained content library generation |
| Multi-node calibration WORK (doc 40 D27) | Doc 40 § 4.6 | Post-Cycle-13 engine extension; foundations laid in Cycle 13 |
| Peak-moment community layer Stage 1-6 (doc 40 D40-D43) | Doc 40 § 7 | Post-launch implementation work cycle; multi-season build-out |
| Layer 7 BDI test framework | Cycle 12 Option γ confirmation 2026-05-25 | v1.1 / Cycle 13+ if empirical observation surfaces concerns |
| W1.13 H1-H5 baseline | Same as above | Same |
| W1.20 BDI infrastructure | Same | Same |
| Polearm aspect-ratio gate (v1.1+ Recognition 5) | Cycle 10 visual-coverage assessment | v1.1+ visual benchmark trigger |
| Meshy polygon-count delta diagnostic (v1.1+ Recognition 6) | Same | v1.1+ |
| Pi infrastructure execution | Pi recognition record 2026-05-25 | Matt schedules "right moment" Pi build + Tailscale install |
| Smart-loot pity system (doc 40 D21 Option B fallback) | Doc 40 § 4.4 | IF Option A calibration proves insufficient across multiple seasons |
| Active-skill budget formula expansion | Doc 40 D82 simplified to flat 8 | Only if multi-chain class designs prove flat-8 insufficient empirically |
| Architecture B → A or C switch | Doc 39 § 4 empirical-trigger discipline | Faction clustering quality / algorithm cultural-fit / player-experience signal / substrate-enrichment cost / Phase 5 LLM cost |
| Faction architecture / three-tier branding / Track M1 mythological-named-weapons fire | Recognition record `fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` | Per § 9 empirical triggers in recognition record |
| MVP scope lock | (pending) | Post-Stage-1-cluster-checkpoint |

### Engineering-discipline candidates (jack-ryan ratification queue)

| Candidate | Source | Status |
|---|---|---|
| Playability discipline (D61) | Doc 40 § 8.10 | ❌ Pending jack-ryan ratification |
| Dual-effect capstone discipline (D76) | Doc 40 § 8.9 | ❌ Pending |
| Spirit-guide-pacing discipline (D78) | Doc 40 § 8.9 | ❌ Pending |
| Commitment-to-consequence discipline (D79) | Doc 40 § 8.9 | ❌ Pending |
| Sim methodology naming discipline (D84) | Doc 40 § 8.11 | ❌ Pending |
| Discipline #23 amendment — 3rd operational instance reference | Doc 40 § 1.4 | ❌ Pending jack-ryan amendment write-up |

---

## 6. Update protocol (for knight-rider)

### 6.1 Update cadence + format

**knight-rider updates this doc at every commit during cycle execution.** When a commit lands that changes a phase or sub-phase status, this doc gets updated in the same commit OR in an immediate follow-on commit.

**Find-and-replace pattern (ASCII visual format per § 3):**
- Locate the relevant line by phase header (e.g., "PHASE 2b") and item description
- Replace the leading icon (❌ / ⏳ / ⚠️ / etc.) with the new state icon
- When transitioning to ✅, **add the completion date** in YYYY-MM-DD format immediately after the icon: `✅ 2026-05-26`
- When aggregating sub-phase status changes a parent phase's status, update both lines + top-line § 2 entry
- Preserve ASCII box-drawing alignment (line endings, vertical bars)

### 6.2 Status transition rules

| Transition | Trigger |
|---|---|
| ❌ → ⏳ | Work-unit fires; specialist begins implementation |
| ⏳ → ✅ | jack-ryan Gate-2 PASS OR equivalent empirical-criterion satisfaction |
| ⏳ → ⚠️ | Blocker surfaces / partial outcome requires Tier-2 ratification / risk flagged |
| ⚠️ → ⏳ | Blocker resolved (e.g., Matt ratification lands; alternative path adopted) |
| ⚠️ → ✅ | Blocker resolved AND completion criterion satisfied |
| ✅ → 🔄 | Iteration / refinement landing without re-opening status |
| ⏳ → ❌ | Work-unit explicitly paused / re-deferred (rare; requires reason in commit message) |
| ❌ → 🔒 | Architectural commitment locked but execution explicitly deferred (post-cycle / empirical-gated) |
| ⛔ | Hard blocker requiring intervention; rare; flag in commit message + dispatch to Matt |

### 6.3 Commit message conventions

When updating this doc, commit messages should follow:

```
ops(knight-rider): roadmap update — <phase / sub-phase> <transition>

<one-line summary of what changed>
<reference to triggering commit or dispatch>
```

Example:
```
ops(knight-rider): roadmap update — Phase 2b T4 Algorithm ⏳→✅

Phase 1 of T4 algorithm (T4s into chains as capstones) jack-ryan Gate-2 PASS;
all Cycle 13 Phase 1 acceptance criteria satisfied per dispatch <DISP-ID>.
References commit <commit-hash>.
```

### 6.4 Structural-change protocol

If a commit introduces new architectural content (new canonical doc; new phase; new sub-phase; new decision point):

1. **knight-rider flags gandalf** for structural authoring of this roadmap
2. gandalf adds new row(s) with initial status (typically ❌ NOT YET STARTED)
3. gandalf updates § 2 top-line summary if phase-level structure changes
4. jack-ryan reviews to ensure status discipline compliance

### 6.5 When to update top-line summary (§ 2) vs detail (§ 3)

- **Detail (§ 3):** every sub-phase status change updates the relevant § 3 sub-section
- **Top-line (§ 2):** updated when overall phase status shifts (e.g., a phase moves from ⏳ to ✅ when all its sub-phases satisfy completion criteria)

### 6.6 Completion criterion — separating Cycle 13 close from engine build complete

**Cycle 13 completion criterion (per Matt 2026-05-26 clarification — mechanical layer only):**
- Phase 1 status = ✅ (incl. 4-progression-node coverage check landed)
- Phase 2 all sub-phases (2a kit composition + 2b T4 algorithm all 4 phases + 2c substrate binding + 2d spec-driven gear gen + 2e coherence + faction) status = ✅
- Phase 3 status = ✅ (incl. multi-T4 sim methodology + multi-node calibration + playability gate)
- Phase 4 status = ✅ (auto on sim PASS — math gates accept/reject kit+substrate)
- Gauntlet battle sim PASS against full new architecture
- Initial mechanical season generation produces sim-validated content for one season's worth of kits + gear
- jack-ryan Gate-2 PASS on Cycle 13 close

**Cycle 13 close does NOT mean engine build complete.** Cycle 13 produces mechanically-validated content but NOT game-ready content (no cohesion, no visuals, no export).

**Engine build COMPLETE criterion (post-Cycle-13; spans Cycle 14+ partitioning TBD):**
- All Phase 1-8 status = ✅ (or 🔒 for explicitly deferred items per § 5)
- All "NEW per doc 40" items have landed across all cycles
- All "NEW per Matt 2026-05-26 scope expansion" items have landed
- All post-Cycle-13 cycles (14+) successfully conclude
- jack-ryan Gate-2 PASS on full engine build verification

**Reincarnated-game unlock criterion:**
- Engine build COMPLETE (above)
- Full pipeline Phase 1-8 generates game-ready content end-to-end
- → **REINCARNATED-GAME UNLOCK** milestone fires → player-facing surface work / demo / loadout / playtest cycle opens

**Cycle 14+ partitioning LOCKED to Pattern A (3 cycles) per Matt 2026-05-26 amendment:**
- **Cycle 14** = Phase 5 cohesion coalescence (P5 cohesion-judge calibration + spirit-guide data-oracle integration + T4-attuned gear cohesion + acquisition curve calibration)
- **Cycle 15** = Phase 6 visual coalescence (CV pipeline + Meshy + Control Rig / Niagara / PCG)
- **Cycle 16** = Phase 7 joint-gate evaluation + Phase 8 profile assembly + export → engine build COMPLETE → **REINCARNATED-GAME UNLOCK**

---

## 7. Composition with other canonical docs

| Doc | Relationship |
|---|---|
| `canonical/00-ground-state.md` | Oracle for CURRENT/HISTORICAL/DEAD status across canon; references this doc in § 5 active workstreams |
| `canonical/38-downstream-delivery-strategy-2026-05-23.md` | D1-D10 delivery strategy keystone; this doc tracks execution against D-series strategies |
| `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` | Authoritative source for workflow architecture (the WHAT); this doc tracks execution (the HOW-FAR) |
| `canonical/40-gear-balance-guide-architecture-2026-05-26.md` | Cycle 13 architectural foundation; this doc tracks per-phase implementation of doc 40 commitments |
| `canonical/37-engine-and-game-two-products.md` | Variant C engine-vs-game lock; this doc's completion criterion = engine ready for reincarnated-game unlock |
| `canonical/historical/02-roadmap-workstream-tracker-2026-05-23.md` | Predecessor; workstream-tracking layer; HISTORICAL since 2026-05-26 |

---

## 8. Sign-off

**Author:** gandalf (story-and-design steward; structural author)
**Operator:** knight-rider (cycle orchestrator; status updater per § 6 protocol)
**Reviewer:** jack-ryan (status discipline compliance review per cycle)
**Authority:** Matt 2026-05-26 — directive to retire prior workstream-tracker roadmap and replace with this operational engine-build-progress tracker; knight-rider references and updates from hive-mind sessions through engine build completion AND reincarnated-game unlock

---

**Signed:** gandalf (story-and-design steward)
**For:** the operational engine-build progress tracker structured around the QD-engine workflow visual flow (per doc 39 § 1). Tracks per-phase + per-sub-phase execution status across the engine build through completion. Updated by knight-rider at every commit during cycle execution. Completion criterion = all phases ✅ → reincarnated-game unlock milestone fires.
