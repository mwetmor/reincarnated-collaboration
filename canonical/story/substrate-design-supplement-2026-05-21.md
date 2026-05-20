# Substrate Design Supplement — Substrate-as-Cohesion-Only Architecture

**Status:** CANONICAL — architectural recommitment 2026-05-21
**Author:** gandalf
**Companions:**
- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` (vision)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8-axis operational spec)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` (full workflow)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` (rebuild plan)

---

## 0. TL;DR

**Substrate identity is a pure cohesion-layer concern. Mechanical generation is substrate-agnostic and BC-target-driven.** Substrate / element / theme labels are assigned by the LLM cohesion-judge POST-generation based on the kit's mechanical signature.

This architectural recommitment 2026-05-21 emerged from Matt's pushback against archetype-lock-in risk: *"do we run the risk of creating archetypes? Physical/Shadow/Holy seem eerily similar to archetypes."* The answer, fully developed, is that substrate-as-thematic-gravity (the intermediate proposal) would re-create archetype-lock-in at the substrate level. The cleaner architectural answer is substrate-as-cohesion-only.

**Three substrate-design refinements adopted:**
- **Shadow = trade-off** thematic identity (bloodlust, dark embrace, faustian-pact, vampiric, soul-exchange)
- **Physical = warcry/shout exception** (D2/D3/D4 Barbarian canonical; active-CD self-amplification)
- **Holy = aura self-amplification** primary (D2 Paladin / D3 Crusader / PoE Guardian canonical; multi-actor as bonus mode)

All three refinements operate at the COHESION layer, NOT the mechanical generation layer.

---

## 1. The architectural recommitment

### 1.1 The chain of abstraction we climbed

**Level 0 — Archetypes (the old paradigm; recompose-hive empirically broken):**
- 13 hand-authored archetype templates (water_mage, fire_mage, earth_caster, etc.)
- Each template = fixed kit composition + fixed BC cell + fixed identity
- Kit-composition pathology is load-bearing (recompose-hive verdict 2026-05-20)

**Level 1 — Substrate as thematic gravity (intermediate proposal):**
- 7 substrates with mechanic preferences (weighted, not exclusive)
- Cross-substrate hybrids permitted; substrate gravity informs but doesn't constrain
- Better than archetypes, but if hardened into hard partitions, recreates archetype-lock at substrate level

**Level 2 — Substrate as pure cohesion-layer label (FINAL):**
- Substrate identity moved entirely to cohesion-BC archive
- Mechanical generation is substrate-AGNOSTIC; pulls from unified mechanic pool
- Cohesion-judge assigns substrate/element/theme post-generation based on mechanical signature
- The IDC meta-principle (Information-Deferred-to-Coalescence) in full purity

### 1.2 The architectural test that finalized the answer

**Test:** *"Does this design choice influence mechanical generation, or only thematic coalescence?"*

- Influences mechanical generation → it's a BC axis dimension or measurement (8-axis territory)
- Influences only thematic coalescence → it's a cohesion-BC dimension (substrate/element/theme territory)

**Substrate / element / theme = ALL cohesion-layer.** Pure thematic. Generation-blind.

### 1.3 Why this honors what ARPG players already do

You don't enter Diablo II and pick "I want my Sorceress to be fire-themed." You build a fire-themed Sorceress by picking fire skills. **The CHOICE of skills creates the identity.** The same is true in PoE — you pick fire-tagged passives + skills, and your build *is* fire-themed.

The "fire mage" or "Hammerdin" identity emerges from build choices, not from a pre-chosen archetype. ARPG players already coalesce thematic identity from mechanical choice. **The QD-engine's substrate-as-cohesion-only architecture makes this explicit at the engine layer.**

### 1.4 Why this resolves the recompose-hive empirical findings

The recompose-hive (closed 2026-05-20) proved kit-composition pathology IS the load-bearing problem. The Alt A follow-on confirmed Pattern-A generalizes universally across all 7 substrates. The root cause: **archetype-lock prevents the engine from generating diverse kit compositions to populate BC space.**

Substrate-as-cohesion-only directly addresses this:
- No archetype templates (LC-001 refactor); generation is BC-target-driven
- No substrate-mechanic locks (LC-012 reinterpretation); mechanic pool is unified
- Cohesion / theme is assigned post-generation, not pre-binding
- Diverse kit compositions emerge naturally from BC-target diversity

---

## 2. The three substrate-design refinements

### 2.1 Shadow = trade-off thematic identity

**ARPG canon (the trade-off pattern):**

| Game | Trade-off archetypes |
|---|---|
| D2 Necromancer | Bone Spirit (HP cost); Blood Golem (life-link); Iron Maiden (defensive trade); Decrepify; Lower Resist |
| D2 Assassin | Mind Blast (convert); Shadow Master (sacrifice for proxy); Death Sentry (corpse-trigger) |
| D2 Druid | Werebear/Werewolf forms (form-trade) |
| D3 Witch Doctor | Sacrifice (pets for damage); Soul Harvest (death-feeds-power); Spirit Walk (defense for repositioning); Hex |
| D3 Necromancer | Bone Armor (consume corpses); Land of the Dead (timing-window); Devour (corpses → essence); Death Nova |
| D4 Necromancer | Sever (HP-cost); Blood Surge (HP-trade); Book of the Dead (sacrifice minion type) |
| PoE | Blood Magic; Pain Attunement; Petrified Blood; Eldritch Battery; Vaal skills (universal trade-off); Pact keystones; The Vow |
| Diablo Immortal | Demon Hunter Strafe (sustained DPS-for-resource trade); blood/shadow runes |

**Broader gaming canon:** Final Fantasy Dark Knight (HP-cost); Dark Souls Hollowing; Bloodborne (blood-economy); Witcher signs; Vampire: The Masquerade.

**Mythological canon:** Faustian bargain; Odin's eye for wisdom; Persephone's pomegranate; Tolkien's Ring (power-for-soul); vampire mythology (eternal life at cost).

**Isekai canon:** Solo Leveling (shadow extraction — sacrifice corpses for permanent shadows); Re:Zero (death-return); That Time I Got Reincarnated as a Slime (Predator skill); Overlord (undead trade-offs).

**Shadow thematic identity in cohesion-BC:**
- Theme labels: bloodlust, dark embrace, faustian pact, vampiric, soul exchange, shadow extraction, dark covenant
- Mechanical signatures that resonate as "shadow":
  - HP-economy (any kit paying HP for power)
  - Low-life-synergy (damage at low HP)
  - Death-feeds-power (corpse mechanics)
  - Conversion (proxy-via-conversion)
  - Sacrifice mechanics
  - Drain (mechanical lifesteal / vampiric)
- Cohesion-judge assigns "shadow" to kits with these signatures, regardless of generation pool

### 2.2 Physical = warcry/shout exception

**ARPG canon (the warcry/shout pattern):**

| Game | Warcry archetype skills |
|---|---|
| D2 Barbarian | Battle Orders, Battle Command, Battle Cry, War Cry, Shout, Taunt — entire skill tree of warcries |
| D3 Barbarian | War Cry, Threatening Shout, Battle Rage, Wrath of the Berserker |
| D4 Barbarian | Rallying Cry, Challenging Shout, War Cry — three core shouts central to Barbarian identity |
| PoE | Enduring Cry, Rallying Cry, Battlemage's Cry, General's Cry, Infernal Cry, Intimidating Cry |
| Last Epoch Sentinel | Lunge + warcry-passive interactions |

**Physical thematic identity in cohesion-BC:**
- Theme labels: warcry, battle roar, war shout, rallying call, primal scream, ancestral cry
- Mechanical signatures that resonate as "physical/martial":
  - Active-CD self-amplification (the warcry mechanic — pay resource, gain timed buff)
  - Damage-pure with martial flavor
  - Melee / mid-range engagement
  - Generator-spender economy with warcry-as-cooldown-burst
- Cohesion-judge assigns "physical" (or martial / warrior / berserker) to kits with these signatures

### 2.3 Holy = aura self-amplification primary

**ARPG canon (the aura pattern):**

| Game | Aura archetype skills |
|---|---|
| D2 Paladin | Holy Fire/Freeze/Shock, Thorns, Defiance, Concentration, Fanaticism, Conviction (all auras buff Paladin first) |
| D3 Crusader | Heaven's Fury, Bombardment, Phalanx, Laws (self-buff with bonus party-buff) |
| D3 Monk | Mantras (Healing / Conviction / Salvation / Retribution) |
| PoE | Aura skill family (Hatred, Wrath, Anger, Determination, Discipline, Purity-aura family) |
| Last Epoch Sentinel | Paladin aura mastery |

**Holy thematic identity in cohesion-BC:**
- Theme labels: aura, blessing, devotion, sanctification, divine radiance, consecration
- Mechanical signatures that resonate as "holy":
  - Passive self-amplification (always-on while equipped)
  - Mitigator or tank defensive profile
  - Steady or overflow resource economy (auras don't drain)
  - Support-oriented mechanic budget (even if applied to self)
- Cohesion-judge assigns "holy" to kits with these signatures
- D7 resolved by architecture: holy works as self-amplification in solo Profile A (canonical ARPG read); multi-actor amplification is a future-context bonus mode

### 2.4 Why the architecture handles all three identically

Under substrate-as-cohesion-only:
- Generation is uniform; same mechanic pool produces all kits
- Cohesion-judge sees mechanical signature and assigns appropriate thematic label
- Shadow / physical / holy labels emerge from mechanical patterns, not from pre-binding
- Cross-substrate hybrids natural (vampiric warrior = shadow + physical; aura-knight = holy + physical)

---

## 3. The five safeguard principles preventing archetype-lock-in

### Principle 1 — Substrate mechanic pools do not exist as restrictive partitions

**OLD framing (rejected):** shadow has mechanic pool [trade-off]; physical has mechanic pool [warcry, damage]; holy has mechanic pool [aura]. Generation pulls from substrate-specific pool.

**NEW framing (adopted):** Unified mechanic pool. Generation pulls based on BC-target requirements. Substrate IS NOT a generation constraint.

### Principle 2 — BC-target dominates all generation decisions

QD-archive identifies sparse cell → engine composes kit to hit that cell. The substrate identity is not a generation input; it's assigned post-generation by cohesion-judge.

### Principle 3 — Cross-substrate composition is the default, not the exception

Hybrid mechanical compositions are EXPECTED outputs of the generation system. D2 Necromancer's Bone Spear is shadow + physical. D3 Crusader's Heaven's Fury is holy + lightning. ARPG canon validates this constantly. Substrate is a *thematic afterthought to mechanical reality.*

### Principle 4 — Substrate identity lives in cohesion-BC, not mechanical-BC

The 8-axis mechanical BC archive is substrate-agnostic. The cohesion-BC archive captures substrate / element / theme as thematic dimensions. Two separate archives per vision doc § 2.3. Two separate measurement layers per Discipline #18 candidate joint-gate.

### Principle 5 — Substrate variety is achieved via BC diversity, not substrate-specific generation

The "5× rule" (substrate sufficiency) **recalibrates to substrate-agnostic per axis × bin**. Total substrate variety = mechanical BC cell variety = 68,040 cells. The mechanic pool must produce ≥ 5× the bin count per axis to populate the archive; this is now a single unified requirement, not per-substrate sub-requirement.

---

## 4. The architectural test (one principle to govern future decisions)

**Test:** *"Does this design choice influence mechanical generation, or only thematic coalescence?"*

| Decision type | Test answer | Layer |
|---|---|---|
| Adding a new BC axis | Influences generation | Mechanical-BC |
| Adding a new BC bin | Influences generation | Mechanical-BC |
| Adding a new substrate | Influences only coalescence | Cohesion-BC |
| Adding a new element | Influences only coalescence | Cohesion-BC |
| Adding a new thematic identity | Influences only coalescence | Cohesion-BC |
| Adding a new mechanic to the pool | Influences generation | Mechanical (per-axis) |
| Adding a new visual style | Influences only visual coalescence | Visual-BC |
| Adding a new profile | Influences only consumption | Profile config (post-archive) |

**This single test eliminates archetype-lock-in risk at every layer.**

---

## 5. Implementation implications for the rebuild

### 5.1 LC-001 archetype refactor (P0 W0.2) — even simpler

**OLD scope:** refactor archetype templates into substrate × role × BC composition.

**NEW scope:** Remove archetype templates entirely. Generation is pure BC-target-driven composition from unified substrate-agnostic mechanic pool.

The on-boot composition logic becomes:
1. Receive BC-target
2. Decompose target into per-axis requirements
3. Compose kit from unified mechanic pool to satisfy requirements
4. Apply role-shape constraints (damage / control / support / hybrid)
5. Return kit; no substrate tagging

### 5.2 LC-012 foundation validator (P0 W0.3) — reinterpreted

**OLD scope:** validator enforces substrate-tagged generation per substrate identity declaration.

**NEW scope:** Validator becomes a cohesion-layer check (correct theme assignment via cohesion-judge). Mechanical generation is substrate-blind; validator confirms cohesion-judge produces sensible substrate labels for accepted kits.

### 5.3 Substrate identity YAMLs (P1 W1.11)

**Repurposed.** No longer constrain mechanical generation. Become:
- Cohesion-judge reference docs (what does "shadow" thematically mean?)
- Theme-library inputs (per Touchpoint 2 profile flag in workflow)
- Cohesion-judge prompt augmentation (provide thematic context to LLM call)

The YAML structure may simplify: combat_pillar / preferred_mechanics fields become advisory thematic notes; not enforced constraints.

### 5.4 P5 cohesion-BC archive (P5 W5.2-W5.3) — gains canonical authority

Cohesion-BC archive is the canonical home of substrate / element / theme. Every accepted mechanical kit gets a cohesion-BC coordinate assigned by the judge. The cohesion-BC archive can be queried for "all shadow-themed kits" or "all fire-element kits" without any reference to substrate-bound generation history.

### 5.5 5× substrate-sufficiency rule (legolas audit recalibration)

**OLD framing:** per substrate, mechanic pool must have 5× bin count templates.

**NEW framing:** unified mechanic pool must have 5× bin count templates per axis × bin. Substrate-agnostic. Legolas Phase 2 substrate audit recalibrates to this metric.

### 5.6 Profile A near-term ship via reduced-cell-space (~11-16 weeks)

**Profile A operational cell-space** at P3 ship (~11-16 weeks):
- 6 × 5 × 1(solo) × 3 × 3 × 3 × 4 × 4(econ excluding HP-econ + charge + damage-converts) = **25,920 cells**
- Substrate variety still achievable via cohesion-BC labels across these 25,920 cells
- All 7 elements (fire / water / earth / wind / lightning / holy / shadow) representable via cohesion-judge

**Profile A full ship at P4** (~15-22 weeks): full 68,040 cells.

---

## 6. Cross-references

- `canonical/story/engine-architecture-vision-qd-profile-2026-05-19.md` — vision (IDC meta-principle is § 5)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8-axis spec (substrate as cohesion-layer adjacent archive § 2.3)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` — workflow (Phase 5 cohesion coalescence)
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — execution plan
- `canonical/story/per-tier-recompose-validation-findings-2026-05-19.md` — recompose-hive empirical findings (kit-composition pathology load-bearing)
- `agentic_orchestration/rocket/research/substrate-generalization-study-2026-05-21/summary.md` — Alt A findings (Pattern-A generalizes universally)
- `agentic_orchestration/jack-ryan/research/legacy-constraint-audit-2026-05-21/constraint-inventory.md` — LC-001 archetype templates; LC-012 foundation validator

---

## 7. Maintenance protocol

This document is v1.0 (initial 2026-05-21). Revisions:
- New substrate-design refinements → v1.X minor amendments
- Architectural recommitment changes → v2.0 (would require Matt approval + protocol amendment)

The substrate-as-cohesion-only architectural commitment is intentionally stable. Substrate refinements (more thematic identities) can be added freely as v1.X minor — they don't change the architecture. Architectural changes require explicit Matt re-ratification.

---

## 8. Closing — the wizard reads

The substrate-as-cohesion-only architecture is the cleanest expression of what we've been building. It honors:

- **ARPG canon** at the player-experience level (theme emerges from build choice)
- **IDC meta-principle** at full purity (substrate identity deferred to coalescence)
- **Anti-archetype-lock-in** at every architectural layer (Matt's instinct, fully developed)
- **Empirical evidence** from recompose-hive (kit-composition pathology resolved by generative diversity, not by substrate constraint)
- **Mythological and cultural depth** of thematic identity (shadow trade-offs, holy auras, physical warcries — universal patterns the LLM judge recognizes)

The wizard's read: **substrate identity is something the cohesion-judge calls a kit. It is not something the engine builds a kit to be.**

This is the cleanest architectural commitment the project has authored.

**Signed:** gandalf (story-and-design steward)
**For:** the QD-engine in its truest architectural form.
