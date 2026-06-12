# Architecture Design Session Plan — Reincarnated Engine Expansion

**STATUS:** CURRENT — Matt-authorized 2026-06-12 (Pattern B session); 5-session cascading architecture plan covering T4, proxy, core combat, kit identity, and validation
**Author:** gandalf
**Date:** 2026-06-12
**Companion docs:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — primary spec translation source
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — BC axis definitions
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — current T4 architecture
- `agentic_orchestration/gandalf/notes/2026-06-12-session-1-t4-architecture-spec.md` — Session 1 detailed spec

---

## Design authority

Matt (senior architect) + gandalf (spec translation + design steward). Each session produces locked specs that gamora/rocket implement against. No implementation fires before spec is locked and Matt-ratified per session.

---

## 5-Session Cascade — Overview

### Session 1 — T4 Architecture *(immediate next session — gates everything)*

**Scope:**
- Name and spec all 21 T4 strategies (6 current + 15 new; see companion spec doc)
- Retire DIRECT_DAMAGE_AMPLIFICATION scaffold (Discipline #39 commitment)
- Multiple T4 node selection architecture: chain count → T4 node count; selection rules
- Chains-within-trees implementation contract (gamora + rocket seams)
- Companion convergence item: design + T4 compatibility matrix
- Proxy-family T4 strategies (6 of the 15 new)
- Companion Contract + Monster Pact T4 strategies
- Support-eligible T4 subset for companion/monster seasons
- 5-property scoring (P1-P5) as generation directive (BUILD_DEFINING assignment rules)

**Produces:**
- Full 21-strategy T4 catalog with eligibility gates + capstone mechanics + pass/fail criteria
- Multi-node selection architecture doc
- Companion convergence item design
- Engine-readable specs gamora/rocket can implement against directly

**Blocks:** Sessions 2, 3 (partially); all proxy T4 strategies; companion system design

---

### Session 2 — Proxy + Companion Architecture *(after Session 1; gates companion system)*

**Scope:**
- Proxy Tier 1 entity modeling: full scope — all 14 confirmed distinct mechanical proxy types
  - Minimal tier: HP + death event + damage contribution
  - Mid tier: HP + position + enemy AI targeting
  - Full tier: HP + position + independent skill rotation + cooldown tracking
  - ProxyCombatant interface design (gamora kernel handoff)
- Proxy Tier 2 NPC/Companion: generation criteria + faction gating rules + BC axis prior weights
- Proxy Tier 3 Monster: generation criteria + binding category eligibility + CC/debuff skew
- Companion modifier vector: modifier types per BC archetype, cap values, interaction rules
- Faction structure: definition + mapping to cultural lineage × historical period × register
- Monster binding categories: 5-6 categories + player kit eligibility per energy_type/element/T4
- Support/CC skew parameters for companion/monster season generation

**Produces:**
- ProxyCombatant full interface spec (→ gamora kernel handoff, see below)
- Companion modifier vector spec
- Faction taxonomy (maps to existing BUILD SPEC generation categories)
- Monster binding category taxonomy

**Blocks:** Gamora kernel extension; all proxy hypothesis tests; companion balance validation

**GAMORA KERNEL HANDOFF fires immediately after Session 2 locks:**
Session 2 produces a `gamora-proxy-kernel-handoff` document containing:
1. ProxyCombatant interface spec (HP, position, skill rotation, death events, threshold triggers)
2. `simulate_fight` signature extension proposal
3. Companion modifier vector application spec (pre-fight modifier; no kernel change)
4. Charge-stack energy type `_ENERGY_CONFIGS` entry (kernel-change-protocol item)
5. Terrain-reactive geometry assessment request (gamora inspects fight_engine boundary)
Gamora begins proxy entity model implementation in parallel with Session 3/4.

---

### Session 3 — Core Combat Mechanics *(partial independence from Session 1; can overlap)*

**Scope:**
- Layer 2 mechanism-structural dimensions: formalize as generation directives (magnitude_pattern × stackability × trigger × scaling_pattern per skill)
- Resource economy Axis 5: charge-stack passive mechanic design (fills missing bin)
- Damage geometry types: terrain_reactive + beam implementation spec (not yet built)
- Control density (Axis 2B): CC ratio measurement methodology
- Damage tempo mechanics: burst / DoT / sustained — formalize mechanic definitions
- Cognitive load metric: execution complexity measurement design (enables hypothesis test)

**Produces:**
- Layer 2 generation directive spec (rocket seam implementation contract)
- Charge-stack mechanic spec (→ gamora kernel-change-protocol item)
- terrain_reactive + beam geometry implementation contract
- Control density measurement methodology
- Cognitive load metric definition

**Blocks:** Resource economy Axis 5 validation; terrain-reactive hypothesis tests

---

### Session 4 — Kit Identity + Generation *(mostly independent; rocket-primary)*

**Scope:**
- Kit architecture (single vs hybrid 2-element): generation logic + skill composition rules
- Vestigial-class identity / archetype label: label system + assignment rules per kit type
- Coupling-architecture / Layer 1.5: max coupling depth rules per kit type
- Cultural lineage + historical period + register: as generation directives + faction alignment
- Investment profile: gear scaling rules
- Faction-kit assignment: map generated kits to faction per lineage/period/register

**Produces:**
- Kit architecture generation spec (rocket seam)
- Vestigial-class label taxonomy + assignment rules
- Coupling-architecture rules
- Cultural lineage / period / register generation directive integration

**Blocks:** Kit identity uniqueness guarantee; faction assignment completeness

---

### Session 5 — Validation Architecture *(after Sessions 1-4 implementation; closes hypothesis loops)*

**Scope:**
- Multi-difficulty gauntlet: L1 / L13 / L26 / L39 enemy scaling design (power-plane validity)
- Content-type scenarios: Speedfarm vs Push mode design (variant-axis hypothesis)
- Per-fight mechanic contribution attribution: measurement design (5-property empirical validation)
- Companion modifier balance validation: 400-kit × companion archetype pairing runs
- Hypothesis test execution: power-plane, variant-axis, experiential axes, 5-property empirical

**Produces:**
- Multi-difficulty gauntlet spec (gamora seam)
- Content-type scenario definitions
- Per-fight attribution measurement methodology
- Balance validation protocol for companion system

---

## Dependency graph

```
Session 1 (T4)
    ├── Session 2 (Proxy + Companion)  ──► Gamora Kernel Handoff (immediate)
    │       └── Session 5 (Validation)
    ├── Session 3 (Core Combat)        ──► (partially parallel with Session 1)
    │       └── Session 5 (Validation)
    └── Session 4 (Kit Identity)       ──► (independent; can start any time)
            └── Session 5 (Validation)
```

---

## Classification summary

**Pure SPEC (10 categories):** Companion convergence item, vestigial-class identity, coupling-architecture, primary element + sub-element, faction system, monster binding categories, investment profile, weapon type family, cultural lineage + period + register, attribute

**Pure HYPOTHESIS — 4 categories (all require engine gaps to test):**

| Category | Engine gap |
|---|---|
| Cognitive load + execution | Complexity metric (Session 3) |
| Power-plane validity | Multi-difficulty gauntlet (Session 5) |
| Variant-axis (Speedfarm↔Push) | Content-type scenarios (Session 5) |
| Experiential axes | Same as variant-axis |

**BOTH (14 categories):** T4 strategy, Proxy Tier 1/2/3, kit architecture, resource economy (Axis 5), multiple T4 node selection, damage geometry (Axis 2), engagement profile (Axis 1), defensive profile (Axis 4), damage tempo + amplitude variance (Axes 3A/3B), control density (Axis 2B), layer 2 mechanism-structural dimensions, 5-property scoring (P1-P5)

---

## Kernel change surface (bounded)

| Change | Session | Status |
|---|---|---|
| ProxyCombatant full entity model | Session 2 → Kernel Handoff | **BLOCKING** for proxy hypothesis tests |
| Charge-stack `_ENERGY_CONFIGS` entry | Session 3 | **BLOCKING** for Axis 5 validation |
| Terrain-reactive geometry (pending gamora assessment) | Session 3 → gamora | Possibly caller-side |
| Multi-T4 combatant properties (pending gamora assessment) | Session 1 → gamora | Likely additive flags only |

Architecture decision: **BROWNFIELD** — all 4 changes are additive extensions; golden-master oracle is preserved as regression anchor for all kernel changes.

---

**Author:** gandalf, 2026-06-12. Matt-authorized architecture session plan. Session 1 spec at companion doc.
