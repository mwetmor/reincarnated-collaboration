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
- `canonical/41-progression-framework-2026-05-27.md` — **NEW**: L50 hybrid progression framework + ~30-day seasonal duration; foundational architectural commitment
- `canonical/46-concentration-architecture-2026-05-27.md` — **NEW**: Concentration architecture 9-layer Cycle 14 sidecar foundation (stat-range bounds + affix migration + capability scope reduction + trigger vocabulary + concentration probability + cohesion layering + synergy scan refined + set keying to T4 strategy clusters + class-agnostic drops)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — **NEW**: Damage scaling architecture three-path routing (physical / magical / hybrid); prerequisite for Cycle 14 Wave 0.5 Track D content gap closure (per-skill mechanical content + substrate weapon binding + elements expansion); discipline candidate #38 queued
- `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — **NEW**: Bounded-viability-with-specialization design directive (Matt 2026-05-28 verbatim made explicit); LOAD-BEARING Cycle 14 v1 architectural commit; 5 operationalized design targets; gates Path α work-streams W-α1 + W-α2 + W-α3 + Wave 5 re-fire validation; Cycle 14 v1 tag revised `v1-cycle-14-bounded-viability-substrate-led`; Cycle 15 D2 Option 6 retroactively retracted; § 4.7 composition with doc 51 max-investment-profile cohort_median anchor added 2026-05-28 evening
- `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` — **NEW (2026-05-28 evening)**: Investment scaling 6-pattern architecture; integrated W-α7+ Phase 2 canonical lock; Patterns 1+2 detailed (active skill damage scaling decay=0.65; passive skill effect scaling decay=0.50; both linear-with-floor at max-investment cohort_median anchor); per-tier 1:1.5:2.17:4.0 preservation; profile semantic definitions (low/mid/max/mixed); W-α6 ENCOUNTER_COHORT_KPM_BAND structure absorbed as Phase 1 input; Patterns 3-6 canonical-locked stubs (threshold unlocks / QoL modifiers / synergy bonuses / resource economy modifiers) for Cycle 15+; Discipline #47 verification framework at § 7; Discipline #45 vocabulary audit PASS. Gates W-α7+ Phase 3 (rocket Patterns 1+2 + gamora BASE re-derivation + encounter HP rebalancing) + Phase 4 (multi-dim ~384-cell calibration) + Phase 5 (BVV harness multi-dim + Wave 5 RE-FIRE)
- `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` — **NEW**: Wave 1 partition design intent canonical; 9-cat × 11-slot affinity matrix + per-rarity grid + 6 principles + SC-4 closure
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone
- `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — **NEW**: Matt + gandalf Pattern-B session 2026-05-27 closeout (load-bearing handoff)
- `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` — **NEW**: Block C calibration scaffolding for gamora handoff per Discipline #18
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
│  │    ✅ 2026-05-27 - Chains organized for class chain count (doc 40 D63-D64, D83)          │ │
│  │                    DESIGN INTENT LANDED per closeout § 1.4 + variable 3-or-4 chains lock │ │
│  │                    • 3-chain class: 2 T4 chains × ~5 nodes (branching-eligible) +        │ │
│  │                      1 supporting chain × ~3 nodes                                       │ │
│  │                    • 4-chain class: 3 T4 chains × ~3-4 nodes (linear) +                  │ │
│  │                      1 supporting chain × ~3 nodes                                       │ │
│  │                    • Branching gated by chain depth ≥4 (§ 8.3.1 LOCKED 2026-05-27)       │ │
│  │                    • Supporting chains absorb class-intrinsic trait architecture         │ │
│  │                      (Option C per closeout § 2.1)                                       │ │
│  │    ❌            - Implementation of chain architecture (rocket Wave 2 work)             │ │
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
│  │    ❌            - 3-category T4 taxonomy (doc 40 § 8.4 LOCKED 2026-05-27):    [NEW]    │ │
│  │                    • Category A: class mechanical/energy alteration (char-wide)          │ │
│  │                    • Category B: chain multiplicative event (chain-specific)             │ │
│  │                    • Category C: chain element conversion/addition (chain-specific)      │ │
│  │                    • Exactly one of B or C per T4; A always present per D76 dual-effect  │ │
│  │    ❌            - DUAL_ELEMENT_ADDITION strategy (doc 40 § 8.4.1 NEW):        [NEW]    │ │
│  │                    Chain skills retain primary element AND add secondary element         │ │
│  │                    (PoE "X% physical as fire"; D4 "all skills deal X% as cold")          │ │
│  │    ❌            - Parallel-chain reach (doc 40 § 8.4.2):                      [NEW]    │ │
│  │                    Chain-specific effect can target OWN chain OR PARALLEL chain;         │ │
│  │                    algorithm-fixed at generation time (not player-chosen)                │ │
│  │    ❌            - Compositional synergy scan (doc 40 § 8.4.3):                [NEW]    │ │
│  │                    Two-pass scan: Pass 1 resolve + Pass 2 preserve;                      │ │
│  │                    Net synergy score = resolve − create; D7 AI-tell line preserved       │ │
│  │                    (pattern library + statistical priors + algorithmic composition;      │ │
│  │                    NOT LLM raw-reasoning)                                                │ │
│  │    ❌            - T4-failure-handling Option F (doc 40 § 8.2 LOCKED 2026-05-27):[NEW]   │ │
│  │                    (1) Regenerate 3 attempts → (2) ship partial T4 → (3) ≥1 T4 in-band   │ │
│  │                    minimum → (4) track regeneration rate as quality metric               │ │
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
│  │ 11. ❌ Class-intrinsic supporting chain absorbs trait architecture       [NEW 2026-05-27]│ │
│  │     (doc 40 § 6.6.1; Option C per closeout § 2.1):                                       │ │
│  │     • Supporting chain (T3-only; every class per D83) = class-intrinsic passives surface │ │
│  │     • NO separate trait modifier axis on character sheet (9-cat surface § 3.6)           │ │
│  │     • Player investment level in class-identity vs build-specialization = opportunity    │ │
│  │       cost; composes with depth-vs-breadth lever                                         │ │
│  │     • Minimum viable trait integration: 55-entry pool (5 per archetype × 11 archetypes)  │ │
│  │       lands in Wave 1; per-class 5-10 + L12/L25/L38 floors DEFERRED to Cycle 14+         │ │
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
│    ❌            - 8-pattern v1 degenerate-state catalog (doc 40 § 8.8.1 LOCKED     [NEW]   │
│                    2026-05-27 per closeout § 5.2 — D61 amendment):                           │
│                    1. Infinite stunlock (time-in-CC > 60%)                                   │
│                    2. Zero-damage void (damage < 1% expected)                                │
│                    3. Mandatory-skill-lock (only 1 viable rotation)                          │
│                    4. Permanent-CC (movement-blocked > 70%)                                  │
│                    5. Resource-starvation (resource < skill cost > 50%)                      │
│                    6. Degenerate-tank (defensive_uptime > 99%; pure DPS check)               │
│                    7. Bounce-CC (skill-cancellation > 50% attempted casts)                   │
│                    8. Resource-overflow (resource at max > 80%; paradoxical)                 │
│                    Substrate-led extension via Cycle 13 telemetry; methodology               │
│                    consultation #18+#18.2 fires post-baseline (gamora + legolas +            │
│                    star-lord)                                                                │
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
│    ⏳            - flavor element flavor mapping per element + bound substrate                  │
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
| T4 PM1 design session | ✅ 2026-05-27 | **PASS-1 COMPLETE** — Matt + gandalf Pattern-B sustained design session 2026-05-27 (~4 hours) covering Blocks A-E in full. All 6 REQUIRES-MATT-CREATIVE-RATIFICATION items ratified via live dialogue + additional architectural locks (L50 hybrid progression framework lock; T4 algorithm 3-category taxonomy + DUAL_ELEMENT_ADDITION + parallel-chain reach + compositional synergy scan; content-compositional attunement supersedes binary/graduated; 9-category char sheet surface; 11-slot taxonomy; per-slot affinity matrix; 8-pattern degenerate-state catalog; Block C calibration scaffolding for gamora handoff). 7 engineering-discipline candidates flagged to jack-ryan. Outputs durably captured at `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md`. Pass-2 (POST-CYCLE-13 with battle sim integrated) queued. |
| L50 hybrid progression framework lock (NEW canon — doc 41) | ✅ 2026-05-27 | Substantial latent canon made explicit; foundational architectural commitment for Reincarnated v1; `canonical/41-progression-framework-2026-05-27.md` |
| Block C calibration scaffolding for gamora handoff | ✅ 2026-05-27 | Design-spec-as-math handoff per Discipline #18; 5-dimensional P_node vector + C_archetype + W(cell, node, cohort) function + Steps 1-8 calibration loop; `agentic_orchestration/gandalf/notes/2026-05-27-block-c-calibration-scaffolding.md` |
| Doc 40 amendments (Wave 0) | ✅ 2026-05-27 | gandalf landed 11-item amendment pass per closeout § 9 #2: T4 algorithm 3-category taxonomy + DUAL_ELEMENT_ADDITION + parallel-chain reach + compositional synergy scan (§ 8.4 + sub-sections); content-compositional attunement (D33+D38+D51); 9-category char sheet surface (§ 3.6) + 11-slot taxonomy + per-slot affinity matrix + 6 principles; class-intrinsic supporting chain (§ 6.6.1 Option C); dual-effect separability + first-do-no-harm (§ 12.1 candidates #6 + #7); D61 8-pattern degenerate-state catalog; D66 one-T4-at-a-time sharpened; D69 chain-based + linear default + branching gated by depth ≥4; D71 graduated investment caps + 70-point endgame anchor; D73 two-option respec |
| Cycle 13 scope-doc authoring (gandalf 4-8 hrs per D85) | ⏳ | Skeleton landed 2026-05-26 (KR); § 12.3 filled 2026-05-26 via gandalf verdicts; remaining canonical doc authoring (3 docs per verdict file § 6.2) conditional on Matt async ratification |
| Stat-sheet partition design INTENT canonical (doc 42) | ✅ 2026-05-27 | gandalf authored `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` per closeout § 3 + Verdicts B.2/B.3/B.4 + framing brief § 3 Wave 1; 9-cat × 11-slot affinity matrix operationalized; per-rarity × per-slot grid; tier-restricted modifier surface enumeration; sample modifier enumerations per category per slot family; 6 principles; SC-4 5 methodology gates CLOSED; minimum-viable trait integration (55-entry pool per Option C); Wave 1 implementation guidance for rocket |
| Stat-sheet partition design cycle (Wave 1 implementation) | ❌ | rocket Wave 1 implementation against doc 42 intent; gates on jack-ryan Gate-1 critique on doc 42; sub-wave structure W1.0-W1.8 per doc 42 § 9.6 |
| Gamora methodology consultation (D60 + D74 + D84) | ⏳ | Delegate-to-gamora posture RATIFIED via Verdicts C.1-C.3; consultation fires post-Wave-4-baseline per Discipline #18.2 refinement |
| Phase 1 T4 algorithm implementation (T4s into chains as capstones) | ⏳ | Per doc 40 D81 Phase 1; design inputs landed via Verdicts A.1-A.6; A.2/A.3/A.4/A.6 RATIFIED standalone (Wave 2 design-intent unblocked); A.1/A.5 pending Matt async ratification |
| Phase 2 T4 algorithm implementation (multiple T4 options per chain) | ⏳ | Per doc 40 D81 Phase 2; design inputs landed via Verdicts A.1-A.6; sequenced after Phase 1 |
| Phase 3 T4 algorithm implementation (character-wide vs chain-wide dimension) | ⏳ | Per doc 40 D81 Phase 3; Verdict A.6 RATIFIED T4-failure-handling Option F standalone; sequenced after Phase 2 |
| Phase 4 T4 algorithm implementation (full sim cycling) | ⏳ | Per doc 40 D81 Phase 4; sequenced after Phase 3; gates on gamora methodology consultation post-baseline per #18.2 |
| Spec-driven gear gen implementation (Phase 2d of workflow) | ⏳ | Per doc 40 D7; design inputs landed via Verdicts B.1-B.4; gates on partition cycle close + Matt async ratification of B.1-B.3 |
| Gauntlet battle sim against full architecture | ❌ | **Cycle 13 culmination milestone**; sequenced after T4 4-phase implementation + spec-driven gear gen + partition |
| Initial mechanical season generation | ❌ | **Cycle 13 final demonstration**; produces sim-validated mechanical content for one season's worth of kits + gear |
| (DEFERRED) Drax integration | 🔒 | Deferred to post-Cycle-13 cycle that handles Phase 5+ (UX needs cohesion outputs to consume) |

### 4.4 Cycle 14 — Phase 5 Cohesion Coalescence + Track D content gap + Concentration Architecture

**Scope (per Cycle 14 framing brief RATIFIED 2026-05-27):** 7-wave structure addressing Phase 5 cohesion coalescence (Q9 Pattern A original scope) + doc 46 concentration architecture 9 layers + Track D content gap closure (Wave 0.5 LOAD-BEARING NEW). See full detail at `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` + live state at `agentic_orchestration/cycle-14-hive-mind-state.md`.

| Wave | Status | Detail |
|---|---|---|
| Wave 0 — scope-doc + sidecars | ✅ CLOSED 2026-05-27 | SC-1 jack-ryan disciplines #33-#39 RATIFIED (`d148808`); SC-2 gandalf doc 40 amendments (`f56ce8b`); SC-3/SC-4/SC-5 legolas research filed; SC-6 elrond substrate audit (NARROW) landed |
| Wave 0.5 — Track D content gap closure (LOAD-BEARING) | ✅ CLOSED 2026-05-27 | rocket (`b2e9a86`) + gamora (`cafd6e4`) + elrond SC-6b (`3c95883`); jack-ryan Gate-2 PASS-with-WARN (`f053281`); **synthetic_mode RETIRED ABSOLUTELY** (Discipline #39 empirical grep ZERO); Path A substrate architecture decisions-log entry; OMEGA_PENALTY Q-W05-G1 RESOLVED (`b3f4db5`) |
| Wave 0.5 follow-on — pipeline wiring + LUT alignment | ✅ COMPLETE 2026-05-27 (`685dafa`) | Pipeline wiring (per_skill_emitter + substrate_weapon_binding → season_generation_pipeline.py); 5-family LUT alignment to elrond Pass-2 |
| Wave 1 — concentration architecture Layers 1-4+7 | ✅ COMPLETE 2026-05-27 (`98b68aa`; tag `rocket/v1.5-wave-1-concentration-architecture-layers-1-4-7`) | **Cycle 13 capability-soup REMEDIATED EMPIRICALLY** — avg 4.2 triggered_passives/kit (Discipline #34 ≤6 TARGET MET; down from Cycle 13's ~22); 61 SC-4 conditions × 11 families; 5 CRITICAL AI-tell triggers; 5 dedup pattern_id clusters; 29 new tests + 232/232 PASS; jack-ryan Gate-2 pending |
| ⚠ **Wave 1.5 — Skill-Tree Architecture** (scaffold-drift Dispatch 2; NEW INSERTED) | 🔄 PIVOT (Option α; engine reverted 2026-05-27) | Stage 1 elrond audit ✅ (`06a3b7f`) + Stage 2 gandalf doc 48 ✅ (`6a28e39`) + Stage 3 rocket impl ✅ (`0a5a4f2`) → **REVERTED at engine `c9fcb1d` 2026-05-27** per Matt verbatim "option 1. Math before code" architectural pivot to Option α (substrate-clustered emergent classes; no pre-authored fixed class taxonomy). Doc 48 RETAINED as PRESERVED-FOR-COMPARISON A/B reference baseline. Re-implementation pending 5 math-notes ratification + jack-ryan Gate-1 + Matt ratification per math-before-code Discipline #1 LOAD-BEARING. Successor: `gandalf/notes/2026-05-27-option-alpha-pivot-and-math-note-inventory.md`. |
| ⚠ **Math-note authoring track (Option α; 5 notes)** | ⏳ AUTHORING QUEUED | 5 math notes pending per pivot record § 2: (1) substrate clustering for chain_count emergence (elrond + gandalf); (2) supporting-chain theme emergence (gandalf); (3) T4 capstone emergence from substrate sub-clusters (gandalf + elrond); (4) class-naming policy deterministic-vs-Phase-5-LLM (gandalf + star-lord); (5) cross-season identity-persistence semantics (gandalf). Ratification flow: author → jack-ryan Gate-1 → Matt ratification per Discipline #18 math-hotspot. |
| ⚠ **Substrate enrichment scope-creep (3 dispatches; INT-AoE + monk + hybrid)** | ⏳ AUTHORING QUEUED | Matt 2026-05-27 verbatim scope-creep directive "slight cycle 14 scope creep but not insurmountable". Three legolas Mode B + elrond curation dispatches firing in PARALLEL with math notes. ~1-2 weeks per. EXCLUDED: multi-spawn summoner (separate engine subsystem; deferred), DEX rebalancing (resolves naturally), Skirmisher shield-family (optional). |
| ⚠ **Substrate sidecar** (scaffold-drift Dispatch 1; NEW PARALLEL) | ⏳ Dispatched 2026-05-27 | `agentic_orchestration/dispatches/2026-05-27-substrate-weapon-family-balance-sidecar.md`. Fix A hygiene filter (rocket; ~1 hr) + Fix B STR family rebalancing math-note (rocket; impl Wave 2) + Fix C caster weapon_kind audit (elrond; non-gating). |
| ⚠ **Discipline #40 ratification** (scaffold-drift Dispatch 3; NEW PARALLEL) | ⏳ Dispatched 2026-05-27 | `agentic_orchestration/dispatches/2026-05-27-jack-ryan-discipline-40-scaffold-values-canonical.md`. Scaffold-values-require-canonical-decision discipline; jack-ryan canonical-write at engineering-disciplines.md; cross-references #11/#13/#18/#39. |
| Wave 2 — concentration architecture Layers 5+8+9 | ⏳ QUEUED (pushed back by Wave 1.5 insertion) | Gates: Wave 1 ✅ + SC-1 partial ratification ✅ + Wave 1.5 close |
| Wave 3 — Phase 5 cohesion-judge LLM architecture | ⏳ QUEUED | Gates: Wave 0.5 ✅ + SC-3 ✅ (CAN fire parallel with Wave 1.5; rocket secondary owner) |
| Wave 4 — T4-attuned gear cohesion + acquisition curve | ⏳ QUEUED | Gates: Wave 2 + Wave 3 |
| Wave 5 — production gauntlet sim + cohesion validation + FRESH cohort (no-class architectural recommitment) | ⏳ **GATED ON PATH α CLOSE 2026-05-28** (was: queued pending pre-fire checklist) | **AMENDED 2026-05-28 PER PATH α RATIFICATION:** Wave 5 RE-FIRE deferred until Path α work-streams (W-α1 damage formula refactor + W-α2 KPM ceiling raise/remove + W-α3 unified calibration pass + W-α4 design-target validation framework per doc 50) all land + validation harness passes 5 design targets simultaneously. Pre-fire checklist (per scaffold-drift § 5.3 + Path (1) expansion): Fix A ✅ / Fix B ✅ math-note / Wave 1.5 Stage 3 re-impl ⏳ / Season cardinality ✅ / Discipline #40 ✅ / Phase 4 math gates ⏳ / Phase 5 multimodal clustering + faction-coalescence ⏳ / Phase 7 2-layer joint-gate ⏳ / Discipline #46 ✅ / Pre-Phase-4 remediation ✅. **NEW gate Path α:** doc 50 5 design targets must PASS on Wave 5 re-fire output (18 kits × 6 encounter types = 108-cell matrix). Cycle 14 close criterion = gauntlet PASS with REAL content + doc 50 bounded-viability-with-specialization validation PASS + 2-layer joint-gate PASS (mechanical + cohesion) + jack-ryan Gate-2 PASS per Q8 (visual joint-gate Cycle 15+). |
| **Path (1) Phase 4 — Mechanical Archive Math Gates** (NEW Cycle 14 scope expansion 2026-05-27) | ✅ MATH NOTES COMPLETE; GATE-1 PENDING | 5 math notes authored (engine `bacc38d`/`24e1001`/`aa507c3`/`dfb1562`/`211c128`/`73d54f9`/`c3b9277` per gamora 2026-05-27): MG-1 Pareto (5-objective quality vector; incremental per-cell frontier) / MG-2 Crowding-Hypervolume (NSGA-II primary; HVC upgrade path) / MG-3 Mahalanobis (Welford incremental covariance; **LOAD-BEARING elrond Pattern-A consultation per Q-Bundle-2 gates impl**) / MG-4 KL Information Gain (KDE-based; JSD fallback at k<20) / MG-5 Eviction (two-trigger; Pareto Rank 0 protected). Per-cell bounding LOAD-BEARING throughout; shared DB fetch optimization documented (4 round-trips → 1 per insertion). gamora primary impl ~3-4 weeks post Matt-gate. |
| **Path (1) Phase 5 Multimodal Extension** (NEW Cycle 14 scope expansion 2026-05-27) | ✅ MATH NOTES COMPLETE + **Gate-1 PASS-with-REVISIONS** (`7d5d585`; 0 BLOCK / 1 WARN / 4 INFO; all 7 notes route to single Matt-gate); Matt-gate fires next | 2 math notes authored (engine `071de8d` + `90092d6` per gandalf 2026-05-27): PM-1 Multimodal Clustering Algorithm (gandalf lean Option β distinct algorithm class from Option α Note 1; per-season kit-population scope vs per-kit substrate scope) + PM-2 Faction-Label Assignment Policy (D-Hybrid + D-Separate; composes with SC-3 Pattern B PRIMARY + Option α Note 4 D3 hybrid; ~$0.15-$0.25 added cost; no-classes vocabulary clean verified). gandalf + star-lord LLM + rocket impl ~2-3 weeks parallel with Phase 4 post Matt-gate. |
| **Path (1) In-Advance Design Calls** (NEW 2026-05-27; 5 deeper design surfaces composed into bundled Matt-gate) | ✅ **MATT-RATIFIED 2026-05-27** with D + E amendments + A SUPERSEDED at PM-1 algorithm commit | A=A2 K=2-4 emergent ✅ → **SUPERSEDED 2026-05-27 by PM-1 K∈{3,4} BIC-selected** (k=2 NOT in selection space; faction-pair narrative composes via seasonal-brief curation per K∈{3,4} emergence; Cycle 15+ revisit if K=2 lockstep becomes design-essential) / B=B1 hybrid (per-season + persistent Court) ✅ / C=C2 30 kits/cell v1 ✅ / **D=D-Sharpened** ✅ (substrate-anchored named-personage hidden engine-layer; surfaced in drax loadout summary + star-lord telemetry as metadata; Phase 5 LLM names ALL kits uniformly player-facing regardless of substrate anchor; composes with PM-2 D-Hybrid + D-Separate) / **E=E-Dev-Phase-Aware** ✅ (retain rejected kits in reject pool during engine-dev phase; switch to E1 discard at Trigger B "engine production-stable" per jack-ryan Discipline #43 design-quality audit verdict). |
| **Matt-gate Path (1) Phase 4+5 + Option α math-note ratification** (2026-05-27) | ✅ **RATIFIED 2026-05-27** — Package A 7 Phase 4+5 (MG-1 PASS-AS-AUTHORED / MG-2 / MG-3 LOAD-BEARING / MG-4 / MG-5 / PM-1 / PM-2) + Package B 5 Option α (Notes 1-3+5 vocab + Note 4 Q2 D-Sharpened LOCKS + field rename + Risks+Watch Items). Cycle 14 implementation sequence fires next: Stage 3 RE-AUTHORING + Dispatch 3A + Dispatch 3B + THEMATIC_REGISTRY + OP amendments parallel. |
| **Matt 6 pre-ratifications + Wave 5 Position B amendment** (2026-05-27) | ✅ **RATIFIED + AMENDED 2026-05-27** | Pre-ratifications #1 Phase 7 thresholds STATIC v1 / #2 F-C tonal direction + TF-IDF <0.7 / #3 A/B 6 dimensions / #4 Wave 5 → **AMENDED to Position B** (single iterative generation + audit-gate; up to 3 retries; ~$0.65-$5.30 LLM cost) / #5 Discipline #45 canonical-write FIRE NOW / #6 OP amendments PARALLEL FIRING. Wave 5 dispatch amended; Position A 3-smoke retired; calibration discipline preserved via 12-discipline stack. |
| **Path (1) Elrond bundled methodology consultation (MG-1..MG-4 + PM-1)** (NEW 2026-05-27 `f8eb1a4`) | ✅ COMPLETE — 4 amendments → re-Gate-1 + 3 cross-cutting findings | **MG-1 PROCEED-AS-AUTHORED** / **MG-2 minor amendment** (MIN_POPULATION 6→10; NSGA-II crowding; HVC deferred indefinitely) / **MG-3 LOAD-BEARING substantive** (Gaussian Mahalanobis + Tikhonov λ=1e-3 NOT 1e-4; MIN_COV_POPULATION 7→15; empirically-calibrated DUPLICATE_THRESHOLD via Hotelling T² not chi-squared at small k; Pareto-strict replaces Q_scalar; HDBSCAN mutual-reachability fallback gated on Shapiro-Wilk smoke test G-MG3-1) / **MG-4 substantive REFRAMING** (JSD primary across full k; retire discrete-grid KL entirely — KDE curse-of-dimensionality at d=5; Silverman + 0.05 floor; remove NOVELTY_CLAMP; MIN_KL_POPULATION 5→10) / **PM-1 algorithm commit** (A4 GMM primary k∈{3,4} BIC-selected NOT 5; A1 k-means n<20 fallback; Option β CONFIRMED distinct from substrate-row HDBSCAN; aesthetic-heavy sqrt-weights + PCA-whitening 95%; PM-1↔MG-5 calibration feedback loop architecturally committed). **Cross-cutting findings (3):** (1) post-first-smoke covariance audit shared deliverable across all 4 Phase 4 gates; (2) shared `CellContext` materialization at Phase 4 pipeline entry (Σ_c + Q_mean_c + sorted_per_dim shared MG-1/2/3/4); (3) PM-1↔MG-5 calibration 5-season window architecturally committed now. KR folds all 3 into Dispatch 3A scope. |
| **Path (1) Failure-modes + Scope-creep + Design-drift Register** (NEW 2026-05-27; 16 patterns) | ⏳ FOLDED INTO PHASE 4+5+7+8 DISPATCH AUTHORING | 7 failure modes (F-1 math methodology drift / F-2 per-cell capacity blowup / F-3 faction cardinality drift / F-4 Phase 5 LLM volume drift / F-5 joint-gate threshold drift / F-6 class concept resurrection / F-7 Phase 6 implicit creep) + 4 scope creeps (S-1 Phase 8 multi-profile / S-2 Wave 4 cascade / S-3 monster-contrast / S-4 visual style register) + 5 design drifts (D-1 substrate-led erosion / D-2 faction pre-authored / D-3 archive as canonical library / D-4 Phase 5 LLM as oracle / D-5 joint-gate theological). KR includes "Risks + Watch Items" section per register § 5 in Phase 4+5+7+8 dispatch authoring; composes with Move 1 quality-criterion refutation conditions. |
| **THEMATIC_REGISTRY authoring** (gandalf cross-cutting; surfaced via PM-2 § 12 architectural finding) | ⏳ KR FOLLOW-ON QUEUED post Matt-gate | ~2-3 days cross-cutting design-call; ~1,500-2,500 registry entries per (element × cultural_lineage) cell; fires between Matt-gate ratification and Dispatch 3B implementation; gates Wave 3 (Phase 5 cohesion-judge LLM) dispatch authoring. |
| **Dispatch 3B scope items (star-lord Pattern-A PM-2 LLM cost consultation surfaced 2026-05-27 `708b575`)** | ⏳ KR FOLDS INTO DISPATCH 3B AUTHORING POST MATT-GATE | 5 items: (1) **LOAD-BEARING two-wave sequencing** Wave A cluster faction calls before Wave B per-kit identity calls — Phase 7 cohesion criterion structurally weaker without; (2) **Concurrency strategy** for ~2,100 Phase 5 calls (existing `_call_with_retry` synchronous; sequential = 70-140 min); (3) ExportFactionCluster schema + MIGRATION.md entry; (4) Local sentence-transformers for cross-faction diversity check (no Anthropic embedding API); (5) Phase 7 joint-gate accepts placeholder when canonical null (gamora/gandalf flag). Cost confirmed within SC-3 envelope: $0.015-$0.05/season expected; gandalf $0.15-$0.25 was conservative ceiling. |
| **Path (1) Phase 7 — 2-Layer Joint-Gate Evaluation** (NEW Cycle 14 scope expansion 2026-05-27) | ⏳ QUEUED | gandalf + jack-ryan; 2-layer (mechanical + cohesion); visual deferred Cycle 15+ alongside Phase 6 + Phase 8; ~1 week post Phase 4 + 5 close. |
| **Discipline #46 ratification** (NEW; LOAD-BEARING pre-Phase-4) | ⏳ DISPATCH AUTHORING QUEUED | jack-ryan canonical-write at engineering-disciplines.md § Discipline #46; 7 patterns (stream + push-to-SQL + index + bound + no-cartesian + WAL + per-cell-bounding); Gate-1/Gate-2 checklist amendments; ~1-2 days. |
| **Pre-Phase-4 Remediation Bundle** (NEW; landed 2026-05-27 same-day) | ✅ ALL 4 COMPLETE 2026-05-27 | 1A jack-ryan Discipline #46 canonical-write (LOAD-BEARING; 7 patterns; Gate-1+Gate-2 amendments; reciprocal cross-references) + 1B elrond v1_scope index (`70965dd`; COVERING INDEX on COUNT) + 1C star-lord telemetry fetchall (`6b758cd`; 3 REFACTOR + 2 INFO-CLOSE; 159/159 tests PASS) + 1D rocket substrate fetchall (RATIFY-AS-BOUNDED both sites; per-seed determinism preserved; comments added). Pre-Phase-4 protection LOCKED. |
| **No-classes architectural recommitment** (NEW 2026-05-27; Matt verbatim "There are no classes... This must be deleted, and immediately") | ✅ HALT-AND-REDACTION LANDED 2026-05-27 | Class concept architecturally RETIRED from generative architecture vocabulary; doc 48 STATUS VESTIGIAL; Option α math notes terminology redacted (substance preserved); Wave 1.5 Stage 3 RE-AUTHORING dispatch HALTED pending jack-ryan re-Gate-1 verification under no-class vocabulary; Matt-gate firing under no-class vocabulary post-verification. Composes with Path (1) expansion + 5-moves discipline-stack + Disciplines #40c/#41/#42/#43/#44 (#41 retroactively applied to class concept itself). Substrate enrichment + Path A revert + 5-moves package preserved untouched. |
| **Path α — Bounded-viability-with-specialization architectural commit** (NEW 2026-05-28; Matt Gate-6 RATIFICATION REVERSAL — Path α RATIFIED; both β paths REJECTED) | 🔥 **ACTIVE WORKSTREAM 2026-05-28** — W-α4-gandalf canonical lock LANDED (doc 50 LOAD-BEARING); W-α6 gamora per-encounter-type bands LANDED (case 10 timing-floor surfaced; absorbed into integrated W-α7+); integrated W-α7+ Phase 2 doc 51 LOAD-BEARING (Patterns 1+2 investment scaling formulas + max-investment cohort_median anchor + per-tier 1:1.5:2.17:4.0 preservation + W-α6 ENCOUNTER_COHORT_KPM_BAND absorbed as Phase 1 input + Patterns 3-6 Cycle 15+ stubs); **Phase 4 RE-RUN at engine `4706af1` SCENARIO B confirmed — CASE 19 EMPIRICALLY VALIDATED 2026-05-28 evening late** (compound_pass=False; T4 FAIL = 0 in-band kits at any calibration point under v1.1 per-variant magnitudes even at upper bounds); **Matt strategic deliberation resolution D1-D6 RATIFIED 2026-05-28 evening late — TWO-LAYER T4 ARCHITECTURE** (Primary T4 universal DIRECT_DAMAGE_AMPLIFICATION 1.75× preferred-encounter-type guarantees Target 4 universal satisfaction; Layer 2 strip-and-ship per doc 51 § 10.8.9; ELEMENT_CONVERSION variant magnitudes UPDATED to v1.2 LOCKED A=1.50/B=1.25/C=0.25+ailment per Matt D3; DEFENSIVE_TRADEOFF REMOVED; TRADE_OFF REVERSED PLACEHOLDER for Cycle 15 lock; Discipline #39 scaffold with Cycle 15 P0 architectural commit per Matt D5; tag retained `v1-cycle-14-bounded-viability-substrate-led` per D6); **gandalf v1.2 canonical amendments LANDED THIS SESSION** (doc 47 § 4.5 v1.2 + NEW § 4.6 + doc 51 § 10.7.8 NEW + § 10.8.9 NEW + doc 50 § 4.7 cross-reference); rocket implementation queued (per Matt D5 Cycle 14 + Cycle 15 retirement); Phase 4 RE-RUN-3 queued post rocket close; Phase 5+6 cascade post compound_pass=True | Authority: Matt 2026-05-28 verbatim design directive "some kits are better at AOE, others are better at bosses/elites/mini-bosses, others are better at speed running, others are better in team play; all are within a bounded space of minimum viability but also none have zero strengths and all weaknesses." Doc 50 canonical lock at `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md`; doc 51 integrated W-α7+ Phase 2 at `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md`; integrated W-α7+ master scoping at `agentic_orchestration/dispatches/2026-05-28-integrated-w-alpha-7-plus-master-scoping.md`; hive-mind state record at `agentic_orchestration/cycle-14-hive-mind-state.md` § "MATT STRATEGIC DELIBERATION RESOLUTION LOCKED 2026-05-28 EVENING LATE — TWO-LAYER T4 ARCHITECTURE". 5 operationalized design targets gate Path α close (base DPS variance ≤1.5× / zero_count=0 / saturation_count=0 / specialization peaks 1.5-2× / floor ≥30% cohort median across 18 kits × 6 encounter types) PLUS evaluated across investment profiles (low/mid/max/mixed); Target 4 satisfaction now via Primary T4 universal-guarantee + Layer 2 strip-and-ship composition per doc 47 § 4.6 + doc 51 § 10.7.8 + § 10.8.9. Cycle 14 v1 trajectory remains within ~4-6 week budget. Cycle 14 v1 tag RETAINED `v1-cycle-14-bounded-viability-substrate-led` per Matt D6. 6-week Matt re-evaluation hook preserves optionality. **Cycle 15 P0 architectural commit row added below for Discipline #39 retirement gate.** |
| **Cycle 15 P0 — DIRECT_DAMAGE_AMPLIFICATION natural-mechanics replacement (Discipline #39 retirement)** (NEW 2026-05-28 evening late per Matt D5 RATIFICATION) | ⏸️ **DEFERRED TO CYCLE 15** — natural-mechanics implementation post-Cycle-14-v1-close | Per Matt D5 ratified Cycle 15 P0 architectural commit scope: (1) per-element +% damage stats architecture (gear affixes + skill passives); (2) kit-specific resistance profiles OR per-encounter elemental advantage tables; (3) DIRECT_DAMAGE_AMPLIFICATION Primary T4 placeholder RETIRED at canonical-doc + engine-implementation level per Discipline #39 Mode B 3-element annotation (scaffold declaration: 1.75× preferred-encounter-type placeholder; named resolution party: Cycle 15+ rocket; named resolution gate: Cycle 15 P0 architectural commit). C14 strip-and-ship empirical outcomes from Phase 4 RE-RUN-3 + Wave 5 RE-FIRE inform Cycle 15 design dialog. TRADE_OFF REVERSED specific mechanic lock candidate at Cycle 15 entry pre-scoping per Matt strategic deliberation queue item 3. Owner: gandalf (canonical) + rocket (implementation). |
| **Patterns 3-6 (Cycle 15+)** (NEW 2026-05-28 evening per doc 51 § 8 canonical-locked stubs) | ⏸️ **DEFERRED TO CYCLE 15+** — canonical vocabulary reserved; implementation post-Cycle-14-v1-close | Pattern 3 threshold unlocks (discrete capability gates at investment thresholds) + Pattern 4 QoL modifiers (animation/cast/regen; non-damage-impacting; not under Discipline #47 scope) + Pattern 5 synergy bonuses (cross-node relational; composes with concentration architecture Layer 7 synergy scan) + Pattern 6 resource economy modifiers (cost/refund/efficiency; resource-economy BC axis). Patterns 7+ unnamed; future cycles may extend. |
| **Cycle 15 D2 Option 6 damage/HP% metric** (was Matt-RATIFIED at Gate-5 2026-05-28) | ❌ **RETROACTIVELY RETRACTED 2026-05-28** per Path α RATIFICATION REVERSAL | Path β-FULL Option 6 rejection rationale at doc 50 § 6.3. Metric replacement would preserve underlying damage formula divergence; future systems (gear, T4, progression, balance) would inherit divergence. Path α addresses root-cause damage formula refactor instead. Jack-ryan W-α5a handles canonical retraction per Discipline #40 case (c) — FOURTH ITERATION of canonical-lock retraction on Phase 7 doc. Cycle 15 scope post-Path-α undetermined; will be re-scoped at Path α close. |

**Scaffold-drift corrective package authority:** `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-recognition-and-corrective-package.md` (consolidated) + `agentic_orchestration/gandalf/notes/2026-05-27-scaffold-drift-kr-kicker.md` (KR routing).

**Externally-gated items per Cycle 14 scope-doc § 4.2:** class-roster sub-decision (Wave 1.5 Option A/B/C — ✅ Option C ratified 2026-05-27; **THEN PIVOTED to Option α 2026-05-27 per Matt "option 1. Math before code"** — substrate-clustered emergent classes; no pre-authored taxonomy; doc 48 retained as A/B baseline); any synthetic_mode retention proposal (Matt explicit re-engagement; KR NOT autonomous per Q4 emphatic lock); HYBRID caster-faith remediation Cycle 15 deferral commitment (✅ APPROVED 2026-05-27; Interpretation III LOCKED 2026-05-27 — ceremonial mace = faith, battle mace = martial); **Option α math-note ratification (5 notes; Discipline #18 math-hotspot; Matt-gate per pivot record § 3.3) gates Wave 1.5 Stage 3 re-implementation**.

**Cycle 15 deferred commitments locked 2026-05-27 (per HYBRID approval + Interpretation III):**
- elrond classifier rule amendment with ceremonial/battle mace discriminator
- legolas Mode B Sidecar B WIS-broad enrichment for ceremonial/battle discrimination boundary
- gandalf canonical doc amendment reconciling attribute-system § 1.3 / § 3 + doc 47 § 3.1 to lock Interpretation III canonically
- gamora BC measurement refresh on caster-faith subset
- star-lord telemetry refresh
- Gated on Wave 5 gauntlet output + Phase 5 cohesion-judge output (NOT Matt design call — Matt pre-resolved 2026-05-27)

### 4.5 WS1A hypothesis-flow workstream lane — hard-blocker Q-waves

**Scope:** WS1A workstream (parent canonical at `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 5.2 + § 8b) runs hypothesis-flow hard-blocker question waves IN PARALLEL with Cycle 14 (Phase 5) and forward cycles. Each Q-wave is a single hive-mind cycle (5 phases internally gated; PG-0 elrond / PG-1 gandalf triage / PG-2 gandalf stats-sufficiency / PG-3 Matt architectural-commitment / PG-4 jack-ryan wave-close). WS1A.Q18 pattern-sets the wave shape for Q16/Q17/Q19 per operational sequence § 10.2.

| Q-wave | Status | Detail |
|---|---|---|
| **WS1A.Q18 — Flavor-pool per-primary-element lock** | ✅ **CLOSED 2026-06-01** (canonical write COMPLETE; Phase 5d jack-ryan Gate-2 PG-4 wave-close critique next) | Matt 2026-06-01 PG-3 architectural-commitment ratification at `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/pg-3-ratification-2026-06-01.md`; canonical lock at `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` — **Architecture A LOCKED**, 118 entries across 8 primaries (109 rotating + 9 physical taxonomy registry); Q18.a-e structural commitments locked; physical opts out of WS1A.4 LLM judgment (mechanical-schema templates); pool.json schema amendments deferred to sub-phase 5f POST-WAVE migration (3 new fields: substrate_validation_lineage + vocabulary_commonness + slot_unambiguous); 3 discipline-recognition candidates surfaced awaiting jack-ryan wave-close ratification |
| **WS1A.Q16 — Per-skill flavor judgment LLM prompt design** | ⏳ **UNBLOCKED** (pending PG-4 PASS on Q18; wave-open dispatch authoring queued) | Composes against the locked Q18 pool; Q16's research scope shifts to LLM-prompt-design canon (FF / SMT spell-naming conventions; PoE skill-name patterns; D&D 5e formal taxonomies). Pattern-sets per WS1A.Q18 5-phase wave structure. |
| **WS1A.Q17 — Hybrid kit element pair selection** | ⏳ **UNBLOCKED** (pending PG-4 PASS on Q18; wave-open dispatch authoring queued) | Composes against the locked Q18 pool + Q16 judgment design. Hybrid kit pairs primaries; per-pair sub-element selection consumes Q18 allow-lists per primary. Pattern-sets per WS1A.Q18 5-phase wave structure. |
| **WS1A.Q19 — Emergent kit concept naming consistency** | ⏳ **UNBLOCKED** (pending PG-4 PASS on Q18; wave-open dispatch authoring queued) | Composes against Q16 LLM judgment + Q18 pool. Naming consistency validates per-kit naming against (primary + sub-element + form + ailment) coherence per Q18 vocabulary. Pattern-sets per WS1A.Q18 5-phase wave structure. |
| **Sub-phase 5f — pool.json migration dispatch (POST-WAVE for Q18)** | ❌ **QUEUED** (POST-WAVE; not within Q18 wave scope) | KR authors operational dispatch extending `data/seasonal_elements/pool.json` per the Q18 lock; elrond + star-lord surface touches (pool migration; 3 schema-field additions; 118 entries migrated with lineage tags per Q18 canonical doc § 7; 9 physical entries to separate taxonomy-registry surface; downstream consumer updates). Cross-seam contract change per ADR-004. |

**WS1A workstream lane composition:** runs in parallel with engine-build cycles; does NOT block the engine-build progress tracker phases 1-8. Wave-close (PG-4 PASS) on Q18 unblocks the Q16/Q17/Q19 sequence. Each Q-wave is bounded by its own 5-phase internal sequence; multiple Q-waves may fire in parallel post-Q18-close per orchestrator scheduling.

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
| **Per-level scaling formulas** (player stat scaling; monster stat scaling; XP curve; encounter difficulty multipliers per level) | Doc 41 § 4 #1 (deferred 2026-05-27) | Cycle 13 mechanical season gen telemetry OR scaling-implementation cycle scheduled (Cycle 14+ candidate) |
| **First-pass class roster** (specific class lineup; chain count + composition per class) | Block A2b deferred 2026-05-27 | Wave 1 BC-target review + substrate evidence on chain composition viability |
| **Full respec cost calibration** | Block A4b deferred 2026-05-27 | Gear/currency infrastructure landed (Cycle 14+) |
| **Multi-node calibration WORK across all 4 progression nodes** (Block C Scaffolds 1+3 per-node numerical calibration) | Doc 41 § 4 #2 deferred 2026-05-27 | Per-level scaling formulas land (post #1 above) |
| **Acquisition curve calibration sharpening** (D21 Option A specifics under L50 hybrid engagement window) | Doc 41 § 4 #3 deferred 2026-05-27 | Per-level scaling formulas + telemetry-based per-cohort engagement data |
| **Position-as-resource (9th resource model)** | Block A.5b deferred v1.1+ 2026-05-27 | P2/P3 substrate clustering surfaces artillery/cannoneer/siege cluster (~50+ rows) whose mechanical natural fit is none-of-current-8-models |
| **Faith/Souls/Karma + Crafted-resource (10th+ resource models)** | Block A.5b deferred v1.1+ 2026-05-27 | Substrate vote OR design call for archetypal kits requiring them |
| **Chain-level respec** (between T4-only and full respec) | Block A4a deferred v1.1+ 2026-05-27 | Substrate-evidence shows binary T4-only / full respec is too rigid |
| **Graduated attunement** (alternative to content-compositional) | Block B1a deferred v1.1+ 2026-05-27 | Substrate-evidence shows content-compositional too rigid |
| **Per-node bracket numerical calibration** (Block C Scaffold 3 W(cell, node, cohort) per-bracket numerics) | Block C scaffolding § 3 deferred 2026-05-27 | Per-level scaling formulas land (gates on first row of this table) |
| **Proxy-light / proxy-heavy 7-cell endgame encounter content** (Cycle 14+ work-unit) — 7 BC cells deferred from Cycle 13 SC-6 WU-R2 scope due to proxy-density sim constraint (Axis 2A proxy-light/heavy deferred-evaluation pool per qd-engine-bc-axes-lock-2026-05-20.md § 5). Cells: `(melee, low, spiky, STR, light)` Ancestor-Warrior / `(ranged, high, flat, DEX, light)` Falconer-Pet-Archer / `(mid, low, spiky, DEX, heavy)` Trap-Assassin-Mine-Mercenary / `(mid, low, spiky, INT, heavy)` Necromancer-Summoner / `(mid, medium, variable, INT, heavy)` Totem-Hierophant-INT / `(mid, low, variable, WIS, heavy)` Druid-Beastmaster / `(mid, medium, variable, WIS, heavy)` Witch-Doctor-Petmaster. 18 non-deferred cells authored in Cycle 13 SC-6. | Cycle 13 SC-6 WU-R4 — rocket 2026-05-27 | Sim capability extension lands for proxy-density encounters (player-side entity spawning + ally AI + target-selection + ally HP tracking per BC-axes-lock § 5 sim extension list); empirical trigger = gamora SC-7 methodology consultation confirms proxy-sim architecture ready |

### Engineering-discipline candidates (jack-ryan ratification queue)

| Candidate | Source | Status |
|---|---|---|
| Playability discipline (D61) → **#26** | Doc 40 § 8.10 | ✅ 2026-05-26 — jack-ryan SC-2 canonical landed (engine commit `9705469`) |
| Dual-effect capstone discipline (D76) → **#27** | Doc 40 § 8.9 | ✅ 2026-05-26 — jack-ryan SC-2 canonical landed |
| Spirit-guide-pacing discipline (D78) → **#28** | Doc 40 § 8.9 | ✅ 2026-05-26 — jack-ryan SC-2 canonical landed |
| Commitment-to-consequence discipline (D79) → **#29** | Doc 40 § 8.9 | ✅ 2026-05-26 — jack-ryan SC-2 canonical landed |
| Sim methodology naming discipline (D84) → **#30** | Doc 40 § 8.11 | ✅ 2026-05-26 — jack-ryan SC-2 canonical landed |
| Discipline #23 amendment — 3rd operational instance reference | Doc 40 § 1.4 | ✅ 2026-05-26 — jack-ryan SC-3 amendment landed (1st + 2nd instances also made explicit inline) |
| **Dual-effect separability discipline (D76 amendment) → #31** | Block A.5 2026-05-27 session — corrected Blood Magic example; doc 40 § 8.4 + § 12.1 #6 | ❌ — jack-ryan SC-2 expansion ratification queued; founding instance captured in closeout doc § 7 + doc 40 § 8.4 |
| **First-do-no-harm discipline for algorithmically-generated T4 keystones → #32** | Block A.5 2026-05-27 session button-up; doc 40 § 8.4.3 + § 12.1 #7 | ❌ — jack-ryan SC-2 expansion ratification queued; two-pass synergy scan (resolve + preserve); founding instance captured in closeout doc § 7 + doc 40 § 8.4.3 |

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
