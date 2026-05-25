# Skill System — Reincarnated v1 Operational Definition

> **STATUS:** CURRENT — PROPOSED operational definition consolidating skill composition pattern + locking algorithmic-mechanic-alteration as architectural feature; Stage 0 design call may amend. Authored as Cycle 10 substrate-curation dispatch prerequisite per Matt 2026-05-24.

**Date:** 2026-05-24
**Author:** gandalf (story-and-design steward)
**Status:** ACTIVE — locks skill composition pattern + 10-15-node tree scope + passive discipline + algorithmic mechanic-alteration as v1 architecture; consolidates Phase 2 generation pattern referenced across BDI / T4-A / element_biases / Q-A verdict
**Authority:** Matt 2026-05-24 — Cycle 10 Stage 0 prerequisite confirmation + design-dialogue refinements (Stream A1 composite authoring)
**Companion docs:**
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes (skill geometry/tempo/amplitude map to axes)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` — Phase 2 (skill composition) + Phase 5 (LLM naming/cohesion)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — ω/τ tables provide rank-2 skill-pair magnitudes
- `canonical/story/historical/build-defining-resonance-formula-2026-05-21.md` — BDI formalism (rank-1/2/3; β-pair + γ-triple)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` — T4 architecture (rank-3 build-defining-node tier)
- `canonical/story/attribute-system-2026-05-24.md` — Stream A1 sibling doc; attribute coupling
- `agentic_orchestration/gandalf/notes/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md` — Q-A verdict (T4 regime-change mechanic / η-coefficient operationalization)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 7 — D7 AI-tell discipline (LLM naming curation)
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` — ELEMENT_SCALING_ATTRIBUTE
- `~/Games/reincarnated-engine/src/reincarnated/generation/` — skill composition seam (rocket territory)
- MEMORY: `project_earth_meta_layer.md` — spirit guide architecture (powers the mechanic-alteration explainer pattern per § 9)

---

## 0. TL;DR

A Reincarnated skill at Phase 2 composition is structurally:

```
skill = (element, geometry, tempo, amplitude) × tier_coefficient
        + [special_effect_if_T4_build_defining]
        + placeholder_name (LLM-named at Phase 5, NOT Phase 2)
```

Key v1 architecture decisions captured in this doc:

| Decision | Lock |
|---|---|
| **Skill tree scope** | 10-15 nodes total per form (small tree; D3-scale, not PoE-scale) |
| **Passive nodes** | INCLUDED with discipline: **mechanic-altering passives only; NO stat-bonus filler** |
| **Synergy mechanism** | Adjacent-axis-overlap via ω-field operationalization at tree-adjacency level |
| **T4 build-defining as mechanic-altering** | Per PoE/PoE2 keystone precedent — every T4 node is a trade-off or conversion that fundamentally shifts kit's mathematical mode |
| **Algorithmic mechanic-alteration** | **Architectural advance** — engine algorithmically derives mechanic-alterations per kit's BC-axis space + element coupling + tier coefficient; manifests as T4 build-defining skill OR adjacent-node mechanic-alteration passive |
| **Spirit-guide explainer pattern** | Per-kit unique mechanic-alterations explained in-fiction by spirit guide; templated D7-AI-tell narrative pattern; turns cognitive-load risk into story win |

This doc consolidates scattered references into a single operational source. Skill-composition mechanics live across BDI (ω/τ rank-2; γ rank-3), T4-A (T4 node architecture), element_biases (element-attribute coupling), and QD-engine-end-to-end-workflow (Phase 2 generation + Phase 5 cohesion) without a single canonical reference. This doc closes that gap AND adds the v1 architecture decisions per Matt 2026-05-24 design dialogue.

---

## 1. The skill structure

Each skill instance composes from **five mechanical inputs + one cohesion input + one identity output**:

| Component | Type | Source | Notes |
|---|---|---|---|
| element | enum (8 values) | element_biases.py | Couples to scaling attribute; informs ω-resource-dimension |
| geometry | enum (16 values per palette) | 09-geometry-palette historical doc | Spatial pattern of damage delivery |
| tempo | enum (3 values: low/med/high) | BC-axes-lock § 3.5 | Damage event rate |
| amplitude | enum (3 values: flat/variable/spiky) | BC-axes-lock § 3.6 | Damage variance signature |
| tier_coefficient | int {1, 2, 3} | BDI § 2.4 rank | Determines interaction-dominance level |
| special_effect | optional regime-change mechanic | Q-A verdict § 2.2; T4-A § 4; ALGORITHMIC per § 8 below | Only present at tier_coefficient=3 (T4 build-defining-node) OR at adjacent-node mechanic-alteration passive per § 8 |
| placeholder_name | string | engine-internal | Replaced at Phase 5 by LLM-curated name |

### 1.1 Example skill compositions

**Rank-1 active skill (tier_coefficient=1) — "Frost Bolt":**
```
element: water
geometry: single (single-target projectile)
tempo: med
amplitude: flat
tier_coefficient: 1
special_effect: none
placeholder_name: water_skill_001
```

**Rank-2 active skill (tier_coefficient=2) — "Holy Smite" (paired with Holy Aura for β-pair-dominant build):**
```
element: holy
geometry: arc (sweep-strike)
tempo: med
amplitude: variable
tier_coefficient: 2
special_effect: none (rank-2 = β-pair-dominant; emerges from adjacency-via-axis-overlap per § 5)
placeholder_name: holy_skill_017
```

**Rank-3 T4 build-defining active skill (tier_coefficient=3) — "Cataclysmic Avalanche":**
```
element: earth
geometry: AoE (sweep + delayed-impact)
tempo: low
amplitude: spiky
tier_coefficient: 3
special_effect: ALGORITHMIC (per § 8) — example output: "regime-change: triggers terrain-shift on hit; subsequent skills in zone get +damage and -tempo (the zone is the regime)"
placeholder_name: earth_skill_042
```

**Mechanic-altering PASSIVE node — "Stone Heart" (adjacent-node alteration; alters earth-skill behavior):**
```
element: earth (binds to earth-element actives)
geometry: n/a (passive)
tempo: n/a (passive)
amplitude: n/a (passive)
tier_coefficient: 2 OR 3 (depends on alteration magnitude)
special_effect: ALGORITHMIC — example: "regime-change: earth-element skills cost HP instead of mana; gain +amplitude-spike at -tempo"
placeholder_name: passive_earth_007
```

---

## 2. Skill tree scope — 10-15 nodes per form

### 2.1 Scope lock

Per Matt 2026-05-24: each form's skill tree contains **10-15 total nodes** (combined active + passive). This is small-tree territory.

| Genre comparison | Tree size | Notes |
|---|---|---|
| Reincarnated (v1) | **10-15 nodes per form** | Small tree; D3-class-skill scale |
| Diablo 3 | ~25 active skills + 15 passives per class | Pick 5 actives + 4 passives per build |
| Diablo 4 | ~30-50 skills per class + paragon board | Larger active pool |
| Last Epoch | ~5-10 actives + per-skill passive trees (~50 nodes each) | Deep per-skill specialization |
| PoE / PoE2 | 6-7 active gems + 1500+ shared passive nodes | Massive passive tree |
| Wolcen | Class-themed passive tree | Mid-size |

### 2.2 Design weight implications

In a 10-15 node tree:
- Each node carries LARGE design weight; filler nodes are not viable use of slot budget
- Per-kit skill budget is tight: probably ~5-8 actives + ~3-7 passives (Stage 0 lock decision per § 11)
- T4 (rank-3) build-defining nodes are RARE — likely 0-1 per kit; not every kit has one
- Smaller decision space = SHARPER player choice; every node taken matters

### 2.3 Cognitive load disposition (per Matt 2026-05-24 design dialogue)

Cognitive load is NOT a concern with small tree because:

1. **Small tree learnable in detail** — players can learn every skill in a 10-15-node form intimately during a season; no "I've forgotten what node X does" problem
2. **Spirit guide explainer pattern** — per § 9, the spirit guide steps in for unique mechanic-alterations and explains in-fiction; cognitive-load risk becomes story-feature

---

## 3. Passive nodes — MECHANIC-ALTERING ONLY, no filler

### 3.1 Inclusion lock

Per Matt 2026-05-24: passive nodes ARE included in the v1 skill tree, BUT only **mechanic-altering passives.** No "+10% damage" / "+12% HP" / "+15% crit chance" stat-bonus passives.

### 3.2 Why include passives

| Reason | Detail |
|---|---|
| Tier-2 β-pair patterns expand | Active + matching passive = β-pair-dominant rank-2 build |
| Tier-3 γ-triple patterns become richer | Active + active + passive OR active + passive + passive = γ-triple |
| Architecture home for algorithmic mechanic-alteration | Passives are the natural delivery mechanism for adjacent-node mechanic-alterations per § 8 |
| Genre precedent for "passives more valuable than actives" | D3 set-bonuses; LE passive specialization trees; Wolcen ailment-stack passives |

### 3.3 Why mechanic-altering-only discipline

| Reason | Detail |
|---|---|
| 10-15 node budget too small for filler | Every node must do meaningful work |
| Stat-bonus passives are dead-weight design | PoE's "+12% life" passives exist only because their tree is 1500+ nodes; we don't have that real estate |
| Mechanic-altering passives compose with algorithmic-alteration architecture | Passives ARE where the algorithm manifests adjacent-node alterations per § 8 |
| Player experience richer per node | Every passive picked changes how the kit plays, not just adds numbers |

### 3.4 Passive node structure

A passive node has structurally:
- **Bind axis** — which element / geometry / tempo / amplitude / range axis it binds to (e.g., "binds to earth-element actives")
- **Alteration** — the mechanic-change it imposes on bound actives (e.g., "earth-element skills cost HP instead of mana")
- **Trade-off** — what cost the alteration imposes (e.g., "gain +amplitude-spike at -tempo")
- **Tier coefficient** — 2 (β-pair-class alteration) or 3 (γ-triple-class alteration; T4 territory)

---

## 4. Tier coefficient → BDI rank mapping

Per BDI formalism (`canonical/story/historical/build-defining-resonance-formula-2026-05-21.md` § 2.3 + § 2.4):

| Tier coefficient | BDI rank | Description | Examples |
|---|---|---|---|
| **1** | rank-1 (linear-α dominant) | Skill contributes ordinary additive damage; no interaction-dominance; "rotation skill" | Frost Bolt; basic auto-attack; rank-1 spell |
| **2** | rank-2 (β-pair dominant) | Skill PAIRS with another substrate component (skill / gear / trait) to produce paired-identity build; β-coefficient dominates linear-α | D2 Hammerdin Concentration+Hammer; D3 Whirlwind+Sprint; PoE Cyclone+Channeling |
| **3** | rank-3 (γ-triple dominant; T4 territory) | Skill is THE COMPLETER of a substrate-triple; γ-coefficient dominates any pairwise β within the triple; build-defining-identity emerges from triple-synergy | PoE keystone clusters (Blood Magic + Mind over Matter + Mana Reservation); D2 Druid summon-keystone trios |

### 4.1 v1 tier distribution intent (preliminary; Stage 0 locks)

Per T4-A architecture defaults + Q-A verdict T4 framework + § 2.2 small-tree implications:

| Tier | Approximate count per kit | Notes |
|---|---|---|
| Rank-1 (tier=1) actives | 3-5 | Rotation; filler-actives prohibited per § 3 discipline |
| Rank-2 (tier=2) actives + passives | 4-6 | β-pair signature; emerges from adjacent-axis-overlap per § 5 |
| Rank-3 (tier=3) build-defining | 0-1 | Rare; algorithmic alteration per § 8; not every kit has one |

Stage 0 design call locks v1 skill-tier distribution per kit.

---

## 5. Synergy mechanism — adjacent-axis-overlap via ω-field

### 5.1 The mechanism

Per Matt 2026-05-24 design insight: the skill tree's **adjacency structure** determines which synergies are reachable. Two adjacent skills with overlapping axes synergize per ω-field mechanics (`canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` § 1.1).

| Axis overlap (adjacent skills) | Synergy pattern | Multiplier mechanism |
|---|---|---|
| Same element | Resource-pool sharing; element-amp stacking | Shared element-buff frame; both skills benefit from element-bonuses |
| Same geometry | Geometric overlap → damage multiplier within overlap zone | Damage co-location amplifies hits |
| Same tempo | Tempo-resonance | Rhythm builds; channel-sustain patterns; combo cadence |
| Same amplitude | Variance-stacking | spiky+spiky = burst-build; flat+flat = consistent-build; variable+variable = predictable-rotation |
| Same attribute (per attribute-system) | Resource-pool sharing | Both skills draw on same scaling-stat |

Players who CHOOSE PATHS through the tree that hit overlap patterns get amplified kits.

### 5.2 Emergent build-defining at rank-2 scale

This mechanism PROVIDES emergent build-defining-identity at the rank-2 (β-pair) scale WITHOUT requiring T4 nodes for all builds:

- Most kits achieve rank-2 paired-identity via adjacency-axis-overlap
- Only ambitious builds reach rank-3 (T4) via algorithmic mechanic-alteration per § 8
- This validates the small-tree scope — rich build-defining-identity doesn't require massive tree

### 5.3 Bi-modal faction-emergence composition

Different axis-overlap patterns naturally cluster into faction-shapes (per Matt 2026-05-23 design dialogue on bi-modal form library):

| Axis-overlap cluster | Faction-shape | Examples |
|---|---|---|
| Fire + AoE + medium-tempo | Pyromantic-archetype | Cataclysmic mages; fire-elementalists |
| Shadow + single-target + fast-tempo | Assassin-archetype | Shadow-strikers; void-blades |
| Holy + channel + flat-amplitude | Priest-archetype | Channeling clerics; ritual-conduits |
| Earth + AoE + spiky-amplitude | Geomancer-archetype | Avalanche-callers; stone-titans |
| Wind + multi-hit + high-tempo | Wind-dancer-archetype | Storm-rangers; wind-blade-fencers |

The tree's adjacency structure literally embeds faction-affinity. Bi-modal form library (~20-30% named-personage / ~70-80% engine-named-original per Matt 2026-05-23 lock) coalesces around these axis-overlap-clusters at Phase 5 cohesion coalescence.

---

## 6. T4 build-defining as mechanic-altering (PoE/PoE2 precedent)

### 6.1 The genre precedent

PoE keystones are the canonical example of build-defining mechanic-alteration:

| Keystone | Alteration type | Trade-off |
|---|---|---|
| Blood Magic | Resource-conversion | Spend Life instead of Mana for Skills |
| Mind Over Matter | Resource-buffer | 30% of damage taken from Mana before Life |
| Vaal Pact | Mechanic-replacement | Life leech replaces life regen; no regen |
| Resolute Technique | Trade-off | Never crit, never miss |
| Avatar of Fire | Element-conversion | All damage converts to Fire |
| Iron Reflexes | Defensive-conversion | Convert Evasion to Armor |
| Chaos Inoculation | Defensive-tradeoff | Maximum Life becomes 1; immune to Chaos damage |

Each is a TRADE-OFF or CONVERSION that fundamentally shifts the kit's math. The keystone DOES SOMETHING; it does NOT just add stats.

### 6.2 Q-A verdict η-coefficient as canonical operationalization

Per Q-A verdict § 2.2: the η-coefficient measures how much a T4 node SHIFTS the kit's behavior into a different mathematical mode. PoE keystone alterations ARE η-coefficient operationalizations:

- Blood Magic: η measures the kit's mode-shift from mana-cast to HP-cast
- Mind Over Matter: η measures the kit's mode-shift from HP-buffer to mana-buffer  
- Avatar of Fire: η measures the kit's mode-shift from multi-element to mono-fire

A T4 node with high η is build-defining; a T4 candidate with low η demotes to rank-2 (still valid skill, just not regime-shifting).

---

## 7. Regime-change palette (preliminary; algorithm derives specific instances per § 8)

The space of regime-change types the algorithm draws from:

| Regime-change type | Pattern | Genre examples |
|---|---|---|
| **Resource-conversion** | Trade one resource for another (mana ↔ HP; STR ↔ DEX scaling) | Blood Magic; PoE Hierophant; D2 Energy Shield |
| **Resource-buffer** | Damage taken from secondary resource before primary | Mind Over Matter; Eldritch Battery |
| **Mechanic-replacement** | Replace one mechanic with another | Vaal Pact (leech replaces regen); Necromantic Aegis (shield-aura to minions) |
| **Trade-off** | Gain ability X by losing ability Y | Resolute Technique (crit vs miss); Chaos Inoculation (life vs chaos immunity) |
| **Element-conversion** | All damage converts to single element | Avatar of Fire; Hatred-type conversions |
| **Defensive-conversion** | Convert one defensive layer to another | Iron Reflexes (evasion→armor); Acrobatics (armor→evasion) |
| **Tempo-shift** | Change tempo mid-fight | Berserk; Frenzy stacks; Speed Boost cycles |
| **Multi-actor** | Spawn proxies that act independently | Necromancer summons; Totems; Mirage Archers |
| **Zone-control** | Create persistent zones that change subsequent skill behavior in zone | Death and Decay; Vortex; Slow Field |
| **Geometry-collapse** | Trade geometry-area for amplitude-spike | Concentrated Effect; AoE-to-single conversions |
| **Range-collapse** | Trade range for damage | Point-Blank; Close Combat support |

This palette is preliminary — Stage 0 design call may expand or constrain. Algorithm per § 8 generates SPECIFIC instances of these regime-change types per kit's BC-axis shape.

---

## 8. Algorithmic mechanic-alteration — the architectural advance

### 8.1 The architectural innovation

Per Matt 2026-05-24 design dialogue: **Reincarnated's engine algorithmically derives mechanic-alterations per kit's specific BC-axis space, rather than relying on hand-designed keystones.**

| Game | Mechanic-alteration approach | Scope |
|---|---|---|
| PoE / PoE2 | ~30 hand-designed keystones per league | Manual GGG design effort |
| D3 / D4 | Class-locked passive lists; hand-designed per class | Per-class authored |
| Last Epoch | Per-skill passive trees; hand-designed per skill | Per-skill authored |
| Wolcen | Hand-designed passive tree; class-themed clusters | Pre-authored |
| Grim Dawn | Hand-designed mastery system; per-class | Pre-authored |
| **Reincarnated (v1 proposed)** | **Algorithmically-derived mechanic-alterations per kit's BC-axis space + element coupling + tier coefficient** | **Engine-generated; one tailored per kit** |

This is the architectural advance — no other ARPG content engine does this. Per Variant C (`canonical/37-engine-and-game-two-products.md`), this becomes a load-bearing commercial differentiator.

### 8.2 The algorithm's job

Given a kit's 8-axis BC coordinates + 5-axis skill structure + substrate-triple, the algorithm:

1. **Scans the regime-change opportunity space** — which BC axes have headroom for alteration without breaking kit viability
2. **Identifies highest-η candidate alterations** — per Q-A verdict η-coefficient framework
3. **Validates thematic + sim-coherence** — per Phase 5 cohesion judge + Cycle 10 Stage 4 sim-viability check
4. **Manifests the alteration** as either:
   - **T4 build-defining skill node** (alters kit's entire behavior globally; rank-3 active)
   - **Adjacent-node mechanic-alteration passive** (alters specific node's behavior; smaller-scale identity-tweak; rank-2 or rank-3 passive per § 3)

### 8.3 Opportunity-space scan dimensions

The algorithm scans these dimensions for regime-change opportunities:

| BC axis | Alteration patterns the algorithm considers |
|---|---|
| Engagement profile (range) | Collapse range to gain damage; extend range at amplitude cost; melee-to-mid hybrid |
| Damage geometry | Trade geometry-area for amplitude-spike; convert single→cleave at tempo cost; AoE-to-mono conversion |
| Proxy density | Convert direct damage to proxy-summons; multi-actor regime |
| Control density | Trade damage for control density; CC-conversion |
| Damage tempo | Trade tempo for amplitude; trade tempo for survivability; tempo-cycle (alternate fast/slow phases) |
| Damage amplitude variance | Trade amplitude-spike for tempo-sustain; trade amplitude for control |
| Defensive profile | Convert armor to evasion; convert HP regen to leech; HP↔mana buffer redirect |
| Resource economy | Convert mana→HP cost; convert STR→DEX scaling; share resource between actives |
| Element (per element_biases) | Convert element X to element Y for resonance with existing kit |

Each dimension provides potential alteration patterns from the § 7 palette. The algorithm selects the alteration with highest η + thematic-coherence + sim-viability.

### 8.4 Algorithm output

For each kit, the algorithm produces:

```
{
  alteration_type: "resource-conversion",
  alteration_specific: {
    source: "mana",
    target: "HP",
    rate: 1.0,
    trade_off: {amplitude: +0.3, tempo: -0.2}
  },
  manifestation: "T4_active_skill" | "rank2_passive" | "rank3_passive",
  bind_axis: "earth-element",
  estimated_eta: 0.78,
  thematic_anchor: "blood-magic-druid-archetype",
  llm_naming_template: "Stone-Heart Pact"  // Phase 5 fills
}
```

Phase 5 cohesion coalescence consumes this output:
- LLM names the alteration per templated D7-AI-tell discipline
- Cohesion judge validates thematic coherence (alteration fits kit's cultural-tradition + element-cluster identity)
- Spirit-guide explainer template (per § 9) attaches if alteration is novel-to-this-kit

### 8.5 Algorithm implementation scope

> **AMENDMENT 2026-05-24 — ALGORITHM IS V1 T4 DELIVERABLE.** Original framing treated algorithm as v1.1+ work with hand-authored T4-B catalogue as v1 bootstrap. Matt 2026-05-24 design dialogue corrected: hand-authoring T4s in the abstract is meaningless (T4s are per-kit/per-substrate-anchor); algorithm IS the v1 T4 deliverable; T4-B catalogue authoring reframes to post-mortem evaluation of algorithm output (per `agentic_orchestration/gandalf/notes/2026-05-23-t4-b-v1-catalogue-scaffolding.md` amendment header).

| Aspect | Notes |
|---|---|
| **Implementing seam** | rocket (engine generation/skill composition) |
| **When implemented** | **Post-Cycle-10 — V1 DELIVERABLE** (not v1.1+ as originally framed); substrate-curation feeds the algorithm with v1_scope mechanical tags; Stage 4 mechanical-tagging on v1_scope is prerequisite |
| **Sim-viability check** | jack-ryan Gate-2 at output stage; algorithm output must pass sim-viability per T4-A § 3.3 step 5 |
| **Cohesion validation** | Phase 5 cohesion judge gate per QD-engine workflow |
| **Methodology hotspot** | Discipline #18 fires — legolas Mode A consult on algorithmic-keystone-generation literature BEFORE implementation (estimated ~1-2 hr) |
| **LLM cost** | Algorithm runs without LLM at decision layer; LLM call ONLY at Phase 5 cohesion naming per D7 |
| **Post-mortem validation** | After algorithm produces T4s for v1 forms, Matt + gandalf hand-author T4 alternatives for ~5-10 forms via loadout app interface; comparison validates algorithm + provides feedback for v1.1+ algorithm improvement |
| **Estimated wall-time** | ~1-2 weeks rocket implementation (parallel with W1.13 + W1.20 BDI gamora work post-Cycle-10) |
| **Critical-path dependency** | Loadout app (`reincarnated-loadout/`) must consume engine-generated forms + display skill trees for post-mortem authoring — drax + star-lord coordination |

### 8.6 Faction-generated proxies (extension per Matt 2026-05-24 design dialogue)

For proxy-density-heavy kits (proxy=light or proxy=heavy per attribute-system 5-tuple BC-target subspace), the algorithm's output includes a **proxy-spawn-template** that draws from FACTION-COHERENT unit pool — proxies aren't generic skeletons; they're faction-anchored units that respect the form's cultural-tradition + period identity.

#### 8.6.1 Proxy-spawn-template structure

```
algorithm_output_for_proxy_heavy_kit:
  alteration_type: "multi-actor / proxy-spawn"
  alteration_specific: {
    proxy_count_baseline: int (per heavy-proxy cell ~4-7; per light-proxy ~1-3),
    proxy_template: drawn from faction-anchor unit pool,
    proxy_axis_profile: (each proxy has range/tempo/amplitude/geometry/attribute per its own BC-axis profile),
    proxy_behavior: "ai_directed" | "player_directed" | "autonomous_aggro" | "stationary"
  },
  faction_anchor: derived from substrate-resident weapon's cultural-tradition + period
  faction_unit_pool: enumerated per faction
```

#### 8.6.2 Faction-anchor derivation

The proxy faction-anchor comes from the kit's substrate-resident weapon's cultural-tradition + period at Phase 2 generation:

| Form example | Substrate weapon (cultural-tradition + period) | Derived faction-anchor | Proxy unit pool |
|---|---|---|---|
| Custer (per Matt 2026-05-24 vision) | American museum saber (european + industrial period) | American Cavalry (1860-1880) | Cavalry soldiers; mounted dragoons; scouts |
| Moctezuma (per Matt 2026-05-24 vision) | Mesoamerican obsidian-edged macuahuitl | Aztec military (pre-Columbian) | Eagle Warriors (Cuauhocelotl); Jaguar Knights (Ocelotl); Quetzalcoatl (nested mythological summon per § 12.4) |
| D2-Necromancer-style summoner | European medieval scythe + bone-spell-focus | European medieval undead | Skeletons; revenants; ghasts |
| Druid Beastmaster | Celtic carved-wood staff + horn | Celtic spirit-fauna | Wolves; ravens; spirit-bears |
| Trap Assassin | Japanese folklore claws + flash-bombs | Japanese ninja-tradition | (proxies = traps themselves; not actor-proxies) |
| Witch Doctor Petmaster | Sub-Saharan African fetish-mask + ritual-talisman | African pantheon-warriors | Shadow-spirits; ancestral guardians |

#### 8.6.3 Implementation implications

| Aspect | Note |
|---|---|
| **Faction-unit substrate** | Track M1-equivalent for named-mythological-CREATURES substrate becomes load-bearing for proxy-heavy named-bearer forms; current weapon-only substrate doesn't carry proxy-unit definitions |
| **Faction-anchor lookup table** | Per cultural-tradition × period, list of viable proxy-unit-types (drawn from historical military / mythological canon / cultural-coherent folklore) |
| **Sim-balance** | Heavy-proxy kits have larger sim-state-space (form-actor + N-proxy-actors); B14.5 V1 balance-loop architecture handles this; jack-ryan Gate-2 reviews |
| **Cohesion-judge integration** | Phase 5 cohesion-judge verifies proxy-unit-pool aligns with form's cultural-tradition; rejects + re-coalesces when mismatch (per Matt 2026-05-24 cohesion-discipline) |
| **LLM naming integration** | Proxy units named via templated D7 patterns per faction-anchor; "Custer's cavalry" doesn't need per-soldier-naming; faction-anchor implies the unit-name |

#### 8.6.4 Cross-reference to bi-modal form library

Proxy-spawn-templates compose with bi-modal form library (per § 12.3 named-bearer discipline):
- Named-personage forms (Tier 1 + Tier 2 soft-attribution) get faction-coherent proxies matching their named-bearer's historical faction
- Engine-named-original forms get faction-coherent proxies matching their kit's substrate-cultural-tradition (which may or may not be a recognizable real faction)
- Cross-cultural / Pan-Fantasy hybrid forms may get cross-cultural proxy mixes (e.g., a pirate-samurai-style form might have mixed crew of east-asian + caribbean-european units)

#### 8.6.5 Algorithm input expansion

The algorithm now considers, at Phase 2:
- Cell BC-target profile (per skill-system base structure)
- Substrate-resident main weapon (Cycle 10 v1_scope)
- Substrate-resident off-hand item (per off-hand-items doc Sidecar B)
- Faction-anchor derivation (from substrate cultural-tradition + period)
- Proxy-unit-pool enumeration (per faction-anchor lookup)
- Proxy-spawn-template generation (per cell proxy-density bin)

Output bundle (per § 8.4) extends to include:
- `proxy_spawn_template` (if proxy-density > none)
- `faction_anchor` (per substrate-cultural-tradition derivation)
- `proxy_unit_pool` (enumerated faction-coherent units)
- `proxy_behavior_pattern` (ai-directed / player-directed / autonomous / stationary)

---

### 8.7 Risks + mitigations

| Risk | Mitigation |
|---|---|
| Algorithm produces nonsensical alterations | Cohesion judge validates thematic coherence at Phase 5; sim-viability check (Cycle 10 Stage 4 + jack-ryan Gate-2) validates mechanical viability |
| LLM naming becomes harder (each alteration is unique) | Templated D7 naming patterns per alteration-type; LLM names from template (per § 7 palette types) |
| Sim-balance variance per algorithmic alteration | jack-ryan Gate-2 at Stage 4; balance-loop work (B14.5 V1 territory) absorbs variance |
| Player cognitive load (per-kit novel alteration) | Small tree (per § 2) + spirit-guide explainer pattern (per § 9) — converts risk into story win |

---

## 9. Spirit-guide explainer pattern (per Matt 2026-05-24)

### 9.1 The pattern

When a player encounters a unique algorithmically-derived mechanic-alteration in their kit, the SPIRIT GUIDE (per `project_earth_meta_layer.md` canon — the persistent companion who carries memory across reincarnations) steps in as in-fiction explainer.

### 9.2 Template (example per Matt 2026-05-24 dialogue)

```
"Summoner, you may have noticed, but your spirit has just unlocked something
truly unique and meaningful. If you would like a walk-through, I can explain
how to help them make the most out of it."
```

This is a TEMPLATE with narrow LLM-curated blanks per D7 AI-tell discipline:

| Blank | Filled per | Source data |
|---|---|---|
| `your spirit` | Form's name (Phase 5 LLM-named) | Phase 5 cohesion coalescence output |
| `something truly unique and meaningful` | Alteration description | Algorithm output (alteration_type + alteration_specific per § 8.4) |
| `how to help them make the most out of it` | Mechanic walkthrough | Templated explainer per alteration_type from § 7 palette |

### 9.3 Architectural win

This pattern converts a cognitive-load risk into a STORY win:

| Without spirit-guide explainer | With spirit-guide explainer |
|---|---|
| Algorithmic alterations risk overwhelming player | Algorithmic alterations become discoverable narrative moments |
| Need out-of-fiction tutorial UI | Tutorial is IN-FICTION via spirit guide |
| Spirit guide is exposition-only character | Spirit guide gains recurring functional purpose |
| Player learns alterations via wiki/spreadsheets | Player learns via conversation with persistent companion |
| Cognitive load is a feature-debt | Cognitive load is a feature-asset (deepens spirit-guide relationship) |

### 9.4 Genre / story resonance

- **Fate-canon resonance** — Servants explaining their abilities to confused Masters is a recurring beat across Fate franchise
- **Isekai trope resonance** — system / status-screen / companion-AI explainers are core to LitRPG and isekai genre
- **D3 / D4 mentor-character resonance** — Tyrael / Lorath / Cain perform similar exposition function

### 9.5 Implementation implications

| Implication | Notes |
|---|---|
| **Spirit-guide dialogue template authoring** | gandalf authors templates per alteration-type from § 7 palette; ~12-15 templates needed for v1 (one per palette type) |
| **D7 AI-tell discipline applies strictly** | Templated structure; narrow LLM blanks; human-curated; no raw LLM dialogue |
| **Phase 5 cohesion coalescence integration** | When algorithm produces novel-to-this-kit alteration, cohesion judge triggers spirit-guide explainer template selection |
| **Player UX** | Triggered on first encounter of unique mechanic; player can dismiss / replay / skip; appears as in-fiction conversation |

---

## 10. Element-attribute coupling (per attribute-system § 2)

Skill's `element` determines the scaling attribute per `element_biases.py:28`:

| Element | Scaling attribute | ω-resource-dimension signal |
|---|---|---|
| fire / water / lightning / shadow | INT | arcane-cast |
| earth / wind / holy | WIS | ritual/channel-cast |
| physical | STR (or DEX per attribute-system § 2.1 DEX coupling decision) | mundane-cast |

This coupling is consumed by:
- Phase 2 generation: skill composition respects element-attribute coherence
- Phase 3 simulation: damage scaling computed per attribute
- Phase 5 cohesion: cohesion judge confirms element-attribute-cultural coherence
- Algorithm per § 8: element-axis is one dimension of regime-change opportunity scan

---

## 11. ω-field + τ-field consumption (per BDI ω/τ tables)

### 11.1 ω-field (mechanical overlap)
Skill PAIRS are scored on ω-field across 5 dimensions (geometry / tempo / range / resource / effect-category). High-ω pairs are mechanically compatible. Phase 2 generation prefers high-ω pairings for kit coherence. **The skill tree's adjacency structure embeds ω-field — adjacent nodes are designed to have positive ω overlap per § 5.**

### 11.2 τ-field (thematic resonance)
Skill PAIRS are scored on τ-field for thematic compatibility. Phase 5 cohesion coalescence uses τ to assess form's narrative coherence.

### 11.3 v2 BDI γ-triple tables (post-W1.21)
v1 BDI ω/τ tables cover rank-2 (pairs). Rank-3 γ-triples will be tabled post H4 hypothesis test (W1.21 per qd-rebuild plan). For v1 Phase 2 generation: rank-3 skills (T4 nodes) emerge ALGORITHMICALLY per § 8 rather than from pre-authored γ-triple tables.

---

## 12. LLM naming at Phase 5 (D7 AI-tell discipline)

### 12.1 What gets named at Phase 5
- **Skill names** — each skill gets a curated name (e.g., "Hellfire Cascade")
- **Mechanic-alteration names** — each algorithmically-derived alteration gets a curated name (e.g., "Stone-Heart Pact")
- **Kit/form name** — overall kit/form gets a curated name (e.g., "Pyromantic Apostate of the Burnt Lands")
- **Spirit-guide explainer dialogue** — per § 9, alteration-specific walkthrough templated per alteration-type
- **Lore-blurb (optional)** — short in-character description for player-facing UI

### 12.2 Curation discipline (D7 AI-tell)
Per `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 7:
- NOT raw LLM dialogue generation
- TEMPLATED structure with LLM filling narrow blanks
- Human-curated (gandalf spot-check) before player-facing surfaces
- Cohesion judge confirms identity-narrative coherence before LLM naming fires

### 12.3 Named-bearer attribution discipline (per Matt 2026-05-24 design dialogue)
Per the 3-tier discipline + Matt's bi-modal form-library revision (captured in Cycle 10 dispatch addendum):

```
Phase 5 cohesion coalescence:
1. Score kit-weapon alignment on (mechanical-coherence × cultural-tradition × named-bearer)
2. Top-tier alignment + Tier-1-mythological-bearer → name explicitly (Excalibur, Mjolnir)
3. Top-tier alignment + Tier-2-real-historical-bearer → soft-attribution (archetype language)
4. Mid-tier alignment → name from cultural-tradition + kit blend; named-bearer dropped
5. Low-tier alignment → name from kit-shape alone; cultural-tradition dropped too
6. Apply named/unnamed ratio target as soft bias when borderline
7. LLM names per D7 AI-tell (templated; curated; not raw)
```

Bi-modal form-library (~20-30% named-personage / ~70-80% engine-named-original) emerges from this discipline.

### 12.4 Nested mythology naming pattern — Tier-2 invokes Tier-1 (per Matt 2026-05-24)

**Pattern:** a Tier-2 (real-historical-person) named form invokes Tier-1 (broadly-fictionalized mythological-deity) entities as proxies/summons/buffs. The named form and the named proxy are independently tier-assessed; the form-level discipline doesn't constrain proxy-level discipline.

#### 12.4.1 Operational example (per Matt 2026-05-24 vision)

Moctezuma (Tier-2 real-historical-person Aztec emperor) summoning Quetzalcoatl (Tier-1 broadly-fictionalized Mesoamerican deity) as proxy/avatar/summon:

| Layer | Named entity | Tier | Discipline applied |
|---|---|---|---|
| Form name | Moctezuma | Tier 2 real-historical-person | Soft-attribution per § 12.3 — archetype language ("The Eagle-Crowned Tlatoani"); cultural-tradition (Aztec) acknowledged; named-person implied not surfaced |
| Proxy summon | Quetzalcoatl | Tier 1 broadly-fictionalized mythological | Explicit naming OK — "Calls forth Quetzalcoatl, the Feathered Serpent" |

The form's player-facing name follows Tier 2 soft-attribution discipline. The proxy/summon's player-facing name follows Tier 1 explicit naming. Composition of disciplines works because each named entity passes its own tier-test independently.

#### 12.4.2 Genre canon precedent

| Source | Pattern |
|---|---|
| Fate Apocrypha | Vlad III (Tier 2 real-historical Wallachian voivode) summons various draconic and undead constructs (Tier 1 mythological) |
| Fate Grand Order | Solomon (Tier 2 historical-religious figure; careful application of soft-attribution) summons 72 demons of Lemegeton (Tier 1 mythological-grimoire entities) |
| Fate Grand Order | Karna (Tier 1 Hindu mythological figure) wielding Vasavi Shakti (Tier 1 named-mythological weapon from Indra) — both Tier 1; nested-mythology within single tradition |
| Many isekai works | Reincarnated protagonist (engine-named-original Tier 1) summons named mythological constructs (Tier 1 explicit) — nested across tier-categories |

#### 12.4.3 Composition rule

**Form-level discipline does NOT constrain proxy/summon-level discipline.** Each named entity independently passes its own tier-test:

```
Phase 5 cohesion coalescence with nested-mythology:
1. Resolve form-level named-bearer per § 12.3 alignment scoring (Tier 1 / 2 / 3 / engine-named-original)
2. SEPARATELY resolve any proxy/summon/buff named-entities at their own tier:
   - Algorithm § 8 proxy-spawn-template provides faction-anchor + proxy-unit-pool
   - If proxy-unit is a Tier 1 mythological entity (Quetzalcoatl; Gjallarhorn-blast-spirit;
     Aegis-shield-aura-spirit), apply Tier 1 explicit naming discipline
   - If proxy-unit is a generic faction-cultural unit (cavalry soldier; eagle warrior),
     no tier-naming applies; faction-anchor provides identity
   - If proxy-unit is a Tier 2 real-historical-person ("Lieutenant Smith calling
     reinforcements") — apply Tier 2 soft-attribution at proxy level
3. Compose form-name + proxy-name(s) per their independent tier-disciplines
4. Spirit-guide explainer pattern (per § 9) may reference proxy-named-entities
   ("Your spirit calls forth Quetzalcoatl, the Feathered Serpent...")
```

#### 12.4.4 Implementation implications

| Aspect | Note |
|---|---|
| **Proxy-named-entity substrate** | Track M1-equivalent for named-mythological-CREATURES substrate (per § 8.6.3) populates proxy-named-entity Tier 1 pool |
| **Cohesion-judge integration** | Phase 5 verifies form-tier + proxy-tier independently; rejects mismatch (Tier 3 proxy summoned by any form gets re-coalesced) |
| **LLM naming templates** | Per-tier templates apply per named-entity; nested-mythology produces composite output (form-name + proxy-named-entity reference) |
| **Spirit-guide explainer integration** | Templates accommodate proxy-named-entity reference; "Your spirit's [proxy-named-entity]..." pattern |

#### 12.4.5 Cross-reference

This pattern extends per § 8.6 faction-generated-proxies (algorithm-derived proxy-spawn-templates) — when a faction-anchor's proxy-unit-pool includes named-mythological entities (Quetzalcoatl for Aztec; Gjallarhorn-spirit for Norse Heimdall-associated; etc.), nested-mythology naming applies per this section. The two extensions compose: algorithm produces faction-coherent proxy template; cohesion-judge applies per-tier naming discipline; spirit-guide explainer references named entities at the appropriate tier.

---

## 13. Phase 2 generation flow (where skills get composed)

> **AMENDMENT 2026-05-24 (REVISED — Architecture B lock)** — Per Matt 2026-05-24 architectural reversal during Cycle 10 Stage 3 design call: Architecture B (substrate-BOUND at Phase 2 + substrate-genre-flagging unified-architecture pattern) selected as production canonical, superseding Architecture A (substrate-AGNOSTIC Phase 2 — now archived as developer-tool / R&D reference). See `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` for current canonical engine architecture. Phase 2 generation pulls specific substrate weapon + secondary item at generation time per Option α (martial 5-tuple) / Option β (caster attribute-level) / Option C (cross-attribute ω-penalty) policies; substrate's cultural-tradition + period + named-bearer + element-flavor signals are IMMEDIATELY AVAILABLE at Phase 2 for algorithm § 8 + § 8.6 + cohesion-coalescence at Phase 5. Hypothesis: substrate-context-weight improves clustering + algorithmic outcomes. Empirical-trigger discipline locks at end-to-end-workflow § 4.

Per QD-engine end-to-end-workflow Architecture B (`canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`):

```
INPUT: BC-target cell (range × tempo × amplitude × attribute × proxy-density)
       per Cycle 10 Stage 0 v1 cell-targeting intent
       + genre filter per product configuration (Reincarnated = fantasy)

ACTION (SUBSTRATE-BOUND per Architecture B):
1. Select skill-pool matching BC-target attribute coupling
2. Compose tier-1 (rotation) skills matching target tempo + geometry
3. Compose tier-2 (β-pair signature) actives + mechanic-altering passives
   ADJACENT in skill tree, designed for ω-field overlap per § 5
4. IF target cell calls for T4: invoke ALGORITHMIC mechanic-alteration per § 8
   producing tier-3 active OR rank-3 passive
   (substrate context AVAILABLE: cultural-tradition + period + named-bearer signals
   inform regime-change generation per Architecture B)
5. Apply ω-field check (skills are mechanically compatible)
6. Apply τ-field check (skills are thematically compatible)
7. PULL specific substrate weapon from genre-filtered v1_scope per cell-type policy:
   - For MARTIAL cells (STR/DEX primary, physical-element): Option α — 5-tuple
     mechanical-fingerprint match required (weapon-attack IS combat delivery)
   - For CASTER cells (INT/WIS primary, non-physical-element): Option β —
     ATTRIBUTE-LEVEL match only (skills deliver kit BC-target; weapon scales)
   - For HYBRID cells (cross-attribute): Option C — cross-attribute wielding
     permitted with ω-penalty per BDI ω-field resource-dimension
8. PULL specific substrate secondary item (per off-hand-items doc + Sidecar B):
   - Categories: shield / tome / banner / focus / horn / talisman / weapon-integrated-
     accessory / dual-wield-secondary-weapon
   - Per Main/Secondary slot architecture
   - Substrate-fit per parent-weapon compatibility
9. Compose trait constellation
10. Generate faction-proxy spawn-template per algorithm § 8.6
    (faction-anchor derived IMMEDIATELY from bound substrate weapon's cultural-
    tradition + period — Architecture B key benefit)
11. Output: complete kit + BOUND substrate weapon + bound secondary item +
    proxy-spawn-template + algorithm output bundle

OUTPUT: kit ready for Phase 3 sim measurement
        (substrate IS bound; cultural-tradition + period + named-bearer signals
        AVAILABLE for downstream Phase 3-5 work)
```

Phase 2 is **substrate-bound mechanical composition** per Architecture B. Element IS part of mechanical composition. Substrate weapon + secondary BOUND at Phase 2; cultural-tradition + period + named-bearer signals carried through to Phase 5 cohesion-coalescence. Theme / element-flavor / archetypal naming attaches at Phase 5.

**Phase 5 cohesion-coalescence (substrate ALREADY bound from Phase 2):**
1. Cohesion-judge CONFIRMS substrate-thematic fit (cultural-tradition coherence between bound substrate and kit composition)
2. If alignment HIGH: name explicitly (Tier 1) or soft-attribution (Tier 2) per Matt 2026-05-24 bi-modal lock + universal-archetypal-naming discipline
3. If alignment LOW: drop named-bearer attribution per Matt 2026-05-24 graduated-alignment discipline; engine-name original form per archetypal naming
4. Assigns element-canonical-pair flavor at LLM-runtime per bound substrate's cultural-tradition (e.g., earth + Mexica engine-anchor → "Obsidian-Edge Cascade" flavor; earth + necromancer engine-anchor → "Bone Spear" flavor)
5. Commits archetypal player-facing form name per universal naming discipline + naming-space partitioning
6. Spirit-guide explainer triggers if algorithmic mechanic-alteration novel-to-this-kit per § 9
7. Loot-tier assignment per bound substrate's Tier S/A/B/C composite quality scoring (per Architecture B substrate-as-base-type-templates + tiered-instance-loot)

---

## 14. Engine code references

- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` — ELEMENT_SCALING_ATTRIBUTE
- `~/Games/reincarnated-engine/src/reincarnated/generation/` — skill composition seam (rocket); algorithm per § 8 lives here when implemented
- `~/Games/reincarnated-engine/src/reincarnated/simulation/` — sim resolves skill mechanics (gamora)
- `~/Games/reincarnated-engine/src/reincarnated/llm/` — LLM call at Phase 5 (star-lord); spirit-guide template integration here

---

## 15. Decisions deferred to Stage 0 design call

1. **Per-kit skill-budget** — within 10-15 node total, how to split active vs passive (e.g., 7 active + 5 passive; 5 active + 8 passive; etc.)
2. **DEX element coupling** — per attribute-system § 2.1; affects element-attribute coupling table here
3. **Multi-element kit support** — can a kit have skills from multiple elements
4. **Tier-3 ratio for v1** — what fraction of v1 forms HAVE a T4 algorithmic alteration vs are pure rank-2 builds
5. **Regime-change palette scope** — confirm § 7 palette or extend/constrain
6. **Spirit-guide template authoring scope** — ~12-15 templates (one per palette type); gandalf authoring effort estimate
7. **Algorithm implementation timeline** — when does rocket implement § 8 algorithm; gating per Cycle 10 completion + jack-ryan Gate-2 + Discipline #18 methodology consult

---

## 16. What this doc does NOT do

- NOT a final lock — Stage 0 design call may amend any section
- NOT an engine-code change — proposed patterns ARE the engine's existing implicit pattern PLUS the algorithm per § 8 (which is new architecture, implementation deferred)
- NOT the v2 BDI γ-triple tables — those are H4 hypothesis test territory (W1.21)
- NOT the T4-B v1 catalogue — that's downstream design call (Matt + gandalf) consuming this doc + substrate v1_scope
- NOT an attribute-system doc — see sibling `canonical/story/attribute-system-2026-05-24.md`
- NOT a cohesion-judge spec — Phase 5 cohesion-judge architecture sketched in § 12; full spec authored when cohesion-judge calibration (P5) fires
- NOT a spirit-guide canonical doc — spirit-guide architecture canon lives in `project_earth_meta_layer.md` (MEMORY); § 9 here extends it operationally for the explainer pattern
- NOT a complete regime-change palette — § 7 is preliminary; algorithm per § 8 may discover patterns not in palette

---

## 17. Cross-references

### Active project canon this doc grounds in
- `canonical/00-ground-state.md` § 1 (current truth oracle)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (BC axes; skill geometry/tempo/amplitude map to axes)
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-21.md` (Phase 2 generation; Phase 5 cohesion)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` (ω/τ tables for skill-pair scoring; ω-field operationalized at tree-adjacency per § 5)
- `canonical/story/historical/build-defining-resonance-formula-2026-05-21.md` (BDI formalism — historical-informative; foundational definitions)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` (T4 architecture; tier-3 = T4 node)
- `canonical/story/attribute-system-2026-05-24.md` (Stream A1 sibling — attribute coupling)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 7 (D7 AI-tell discipline for LLM naming)
- `agentic_orchestration/gandalf/notes/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md` § 2.2 (T4 regime-change mechanic / η-coefficient)
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` (Cycle 10 dispatch; this doc is a Stage 0 prerequisite)
- MEMORY: `project_earth_meta_layer.md` (spirit guide canon; § 9 explainer pattern grounds here)

### Live state references
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28`
- `~/Games/reincarnated-engine/src/reincarnated/generation/` (skill composition; algorithm § 8 implementation target)
- `~/Games/reincarnated-engine/src/reincarnated/llm/` (LLM call infrastructure; spirit-guide template integration)

### Downstream artifacts this doc anchors
- Cycle 10 Stage 0 design call (consumes vocabulary + locks deferred decisions per § 15)
- T4-B v1 catalogue authoring (consumes skill-tier framework + algorithm output spec)
- Algorithm § 8 implementation work (rocket seam; post-Cycle-10)
- Spirit-guide template authoring (gandalf; per § 9.5; ~12-15 templates per palette type)
- v2 BDI γ-triple tables (post-W1.21 hypothesis test)
- Phase 5 cohesion-judge spec (when authored)

---

## 18. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-24 — Cycle 10 Stage 0 prerequisite per Stream A1 composite authoring confirmation + design-dialogue refinements (skill-tree-scope; passive-discipline; synergy-mechanism; mechanic-altering-T4-precedent; algorithmic-mechanic-alteration; spirit-guide-explainer)
**Status:** CURRENT — PROPOSED operational definition; Stage 0 design call may amend
**Re-engagement gate:** Stage 0 design call locks final skill-system parameters for v1; this doc updates per Stage 0 outputs OR stands as v1 operational truth if Stage 0 endorses without amendment. Algorithm per § 8 implementation is post-Cycle-10 rocket-seam work; gating per Discipline #18 methodology consult + jack-ryan Gate-2.

---

**Signed:** gandalf
**For:** the canonical operational definition of the skill composition pattern at Phase 2 of the QD-engine workflow, including the architectural advance of algorithmic mechanic-alteration per kit's BC-axis space, the spirit-guide explainer pattern that converts cognitive-load risk into story win, and the consolidation of scattered BDI / T4-A / element_biases / Q-A verdict references. Stage 0 design call substrate. Companion to attribute-system doc.
