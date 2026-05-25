# Methodology Recommendation — Algorithm § 8 Mechanic-Alteration Architecture

**Mode:** A (analytical)
**Commissioner:** knight-rider (orchestrator) / for Matt scope-lock
**Date:** 2026-05-25
**Dispatch:** `agentic_orchestration/dispatches/2026-05-25-legolas-algorithm-section-8-methodology-consult.md`
**Sources consulted:** See § 10 (source list)

---

## Summary (3-5 sentences)

The ARPG genre offers two architectural precedents for build-defining mechanic-alteration: hand-designed keystones (PoE/PoE2/D3/GD) and per-skill passive trees (Last Epoch) — in every extant case the mechanic-altering nodes are hand-authored, not algorithmically derived. No published commercial ARPG engine derives keystones programmatically from a BC-coordinate space; this is the architectural advance § 8 introduces. The closest prior art is QD/MAP-Elites research using behavior characteristics, but none couples BC-coordinate scanning to mechanic-alteration generation in a production game context. The implementation pattern most appropriate to Reincarnated's constraints is a **scored-candidate strategy registry**: a regime-change palette (§ 7 of skill-system doc) is enumerated at generation time; each candidate is scored against the kit's BC-axis shape via an η-coefficient proxy function; the highest-scoring viable candidate that passes sim-viability and thematic-coherence gates is committed as the § 8 output. Runtime complexity is O(P × A) per kit where P = palette size (~11 regime-change types) and A = BC-axis scan dimensions (~9 per regime-change type), making per-kit cost negligible relative to Phase 3 convergence. The cheapest refuting test is a small-N offline scan: generate 10-15 kits across diverse BC cells and verify that the committed alterations actually shift the kit's measured BC profile in the predicted direction at a magnitude ≥ η_threshold.

---

## 1. Required-reading synthesis — what § 8 is architecting against

### 1.1 The innovation gap vs genre prior art

`canonical/story/skill-system-2026-05-24.md` § 8.1 explicitly states: "no other ARPG content engine does this." The literature scan confirms this. The table below captures the genre state:

| Game | Mechanic-alteration approach | Authoring | Per-kit tailoring |
|---|---|---|---|
| PoE 1 | ~30 hand-designed keystones on shared passive tree | GGG design team, manual | None — same keystones for all builds |
| PoE 2 | ~18 keystones (as of patch 0.2.0) on shared passive tree | GGG design team, manual | None — same keystones for all builds |
| Diablo 3 | Class-locked passive lists (~20 per class), hand-designed per class | Blizzard design team, manual | Per-class, not per-kit |
| Diablo 4 | Paragon board Legendary nodes (1 per board), hand-designed | Blizzard design team, manual | Per-class, not per-kit |
| Last Epoch | Per-skill passive trees (~20-50 nodes per skill), hand-designed | EHG design team, manual | Per-skill, not per-kit |
| Grim Dawn | Mastery passive trees + Devotion celestial powers, hand-designed | Crate Entertainment, manual | Per-mastery combo, not per-kit |
| **Reincarnated § 8 target** | **Algorithmically-derived mechanic-alteration per kit's BC-axis space** | **Engine-generated** | **Per-kit, per-substrate-anchor** |

The gap is real. There is no published prior art for the § 8 approach in a shipped game.

### 1.2 What "mechanic-altering" means in practice — genre evidence

Across the ARPG literature, mechanic-altering nodes share a common structural signature distinct from additive numerical modifiers:

**Defining structural property:** a mechanic-altering node changes the *type of operation* rather than the *magnitude of an existing operation*. The change is categorical, not scalar.

**Genre examples by alteration type (sourced from PoE 1 + PoE 2 + D3 + LE literature scan):**

| Alteration type | PoE 1 example | PoE 2 example | Effect class |
|---|---|---|---|
| Resource-conversion | Blood Magic (mana → HP cost) | Blood Magic (same) | Replaces resource type consumed by skill costs |
| Resource-buffer | Mind Over Matter (30% damage from mana before life) | Mind Over Matter (50% less mana recovery) | Redirects damage intake through secondary pool |
| Mechanic-replacement | Vaal Pact (leech replaces regen) | Vaal Pact / V-Pack (instant leech, no flasks) | Replaces one recovery mechanic with another |
| Trade-off | Resolute Technique (no crits, never miss) | Resolute Technique (same) | Disables one stat axis to gain immunity to a penalty |
| Element-conversion | Avatar of Fire (all damage → fire) | Avatar of Fire (75% all damage → fire) | Converts outgoing damage element |
| Defensive-conversion | Iron Reflexes (evasion → armor) | Iron Reflexes (same) | Converts one defensive layer to another |
| Defensive-tradeoff | Chaos Inoculation (max life → 1, immune to chaos) | Chaos Inoculation (same) | Eliminates one defense axis entirely in exchange for immunity |
| Geometry-restriction | Ancestral Bond (no direct damage, unlimited totems) | Ancestral Bond variant | Constrains a damage axis to unlock a proxy-density axis |
| Equipment-mechanic | Necromantic Aegis (shield mods → minions) | Necromantic Talisman (amulet mods → minions) | Redirects gear-stat axis to a different target |
| Avoidance-tradeoff | Acrobatics (+dodge, -armor -ES -block) | Acrobatics (evade projectiles/strikes/AoE, -50% evasion) | Converts one avoidance layer for another |
| Multi-hit-tradeoff | Unwavering Stance (no stun, cannot evade) | Unwavering Stance (double stun threshold, no dodge) | Trades avoidance for stun immunity |
| Conditional-modifier | Pain Attunement (PoE 2: +30% crit damage on low life) | Pain Attunement | Ties a stat bonus to a runtime condition |
| Stun/block-tradeoff | Glancing Blows (double block, 50% damage on block) | Glancing Blows | Amplifies a defensive mechanic at reduced quality |

**Runtime vs build-time classification:**

All genre keystones operate at **build-time** (loadout-resolution layer) — they are passive nodes that restructure the character's stat model and combat arithmetic as a fixed modifier applied before any fight begins. None operate dynamically per-attack (runtime keystone selection is not an ARPG pattern in any shipped game examined). The exception is *conditional-modifier* keystones (Pain Attunement, Heart Stopper), where the *activation condition* is runtime but the alteration rule itself is still a static loadout property. This distinction matters for § 8 implementation scoping.

---

## 2. Per-pattern comparative analysis vs § 8 architecture

The § 8 architecture must: (a) scan the kit's BC-axis space for regime-change opportunity; (b) select the highest-η candidate; (c) manifest the alteration as either a T4 active or mechanic-altering passive. The following analysis maps genre patterns to this architecture.

### 2.1 Resource-conversion (Blood Magic class)

**Genre mechanism:** replaces Axis-5 (resource economy) resource type entirely. Operationally: `cost_resource = "HP"` replaces `cost_resource = "mana"` across all skill costs.

**§ 8 opportunity scan trigger:** Axis 5 bin = `HP-economy` in BC-target OR BC-target shows strong INT/WIS caster profile with high mana demand AND sufficient HP regeneration headroom. Algorithm scan: `if bc_target.resource_economy == "HP-economy" OR (bc_target.attribute IN ["INT","WIS"] AND bc_target.defensive_profile != "glass")`.

**η-coefficient interpretation:** high when the kit has: (a) large HP pool relative to mana pool in the element_biases context; (b) low skill count that makes HP-drain manageable; (c) substrate cultural-tradition with blood/sacrifice resonance (Architecture B substrate-context benefit).

**Implementation surface:** loadout-resolution layer. Set `cost_resource_override = "HP"` on all skills in the kit. No per-attack runtime logic.

**Build-time or runtime:** build-time only. Combat arithmetic changes at character-setup.

---

### 2.2 Resource-buffer (Mind Over Matter class)

**Genre mechanism:** damage routing rule change. Operationally: `damage_router = lambda d, stats: min(d * 0.3, stats.mana) + max(0, d - min(d * 0.3, stats.mana))` — absorbs 30% of incoming damage from mana before it reaches HP.

**§ 8 opportunity scan trigger:** Axis 4 bin = `mitigator` OR BC-target has high Axis-5 `overflow` resource economy (surplus mana makes the buffer meaningful). Algorithm scan: `if bc_target.defensive_profile in ["mitigator","tank"] AND bc_target.resource_economy in ["overflow","steady"]`.

**η-coefficient interpretation:** high when the kit generates mana surplus naturally (overflow economy class) making the buffer robust, or when the element generates high mana regeneration (holy/wind WIS-scaling).

**Implementation surface:** damage-resolution layer in simulation. Requires a `pre_damage_routing` hook in the fight engine that intercepts `incoming_damage` before HP reduction. This is the most structurally novel implementation surface of any regime-change type — it requires simulation support, not just loadout-resolution.

**Build-time or runtime:** runtime modification (per-hit), but the *rule* is build-time. Sim must support `damage_routing_hook` as a kit property.

---

### 2.3 Mechanic-replacement / leech-replaces-regen (Vaal Pact class)

**Genre mechanism:** disables passive recovery mechanic; activates instant-leech or active recovery only. Operationally: `regen_rate_override = 0`, `leech_mode = "instant"`.

**§ 8 opportunity scan trigger:** Axis 4 bin = `mitigator` with high leech-fraction in the BC-target profile, AND substrate has warrior/assassin cultural-tradition (offensive survivability pattern).

**η-coefficient interpretation:** high when the kit has reliable leech sources (physical/shadow element couplings with STR/DEX), making passive regen a net-negative deferral.

**Implementation surface:** loadout-resolution layer. Toggle `regen_disabled = True`, `leech_instant = True` on kit. Sim must support instant-leech resolution.

**Build-time or runtime:** build-time rule, runtime application at leech events.

---

### 2.4 Trade-off (Resolute Technique class)

**Genre mechanism:** trades one stat dimension for immunity to its failure mode. Operationally: `hit_chance = 1.0` (never miss), `crit_chance = 0.0` (never crit).

**§ 8 opportunity scan trigger:** Axis 3B bin = `flat` amplitude variance AND BC-target has mid-tempo sustained damage profile (no reliance on crit spikes). Algorithm scan: `if bc_target.damage_amplitude == "flat" AND bc_target.damage_tempo in ["medium","high"]`.

**η-coefficient interpretation:** high when the kit's BC-target explicitly favors flat amplitude (consistent damage) over spiky (crit-burst), making the crit-loss negligible and the miss-immunity high-value.

**Implementation surface:** loadout-resolution layer only. Set `hit_modifier = 1.0`, `crit_rate = 0.0` at loadout. Zero sim extension needed.

**Build-time or runtime:** build-time only.

---

### 2.5 Element-conversion (Avatar of Fire class)

**Genre mechanism:** converts outgoing damage element. Operationally: `element_override = "fire"` for all non-fire outgoing damage.

**§ 8 opportunity scan trigger:** kit's BC-target element is non-fire BUT substrate cultural-tradition has strong fire resonance (e.g., Aztec obsidian-fire, Zoroastrian fire-cult, Norse forge/Surtr anchor). Algorithm scan: `if bc_target.element != "fire" AND substrate.cultural_tradition.fire_resonance_score > threshold`.

**η-coefficient interpretation:** high when element-conversion unlocks substrate thematic coherence that the base element misses — a direct Architecture B benefit. Low when the kit's BC-target is already mono-element.

**Implementation surface:** generation time. Modify `skill.element` at Phase 2 generation, not at loadout or runtime.

**Build-time or runtime:** generation-time rule. All downstream phases (Phase 3 sim, Phase 5 LLM naming) operate on the converted element.

---

### 2.6 Defensive-conversion (Iron Reflexes class)

**Genre mechanism:** converts one defensive stat layer to another. Operationally: `evasion_rating_converted_to_armor = True` — evasion stat contributes to armor pool instead of evasion chance.

**§ 8 opportunity scan trigger:** Axis 4 bin = `dodger` in BC-target BUT substrate cultural-tradition is heavy-armor-associated (e.g., Medieval European plate, Japanese do-maru). Architecture B benefit: cultural-tradition of bound weapon signals armored vs unarmored combat style.

**η-coefficient interpretation:** high when the cultural-mismatch between the kit's defensive BC-target (dodger) and the substrate's armored identity is resolved by conversion.

**Implementation surface:** loadout-resolution layer. Convert stat at character-build time. No sim extension needed beyond armor/evasion calculation.

**Build-time or runtime:** build-time only.

---

### 2.7 Multi-actor / proxy-spawn (§ 8.6 extension)

**Genre mechanism:** adds persistent player-allied actor generation. This is the genre's summoner pattern (D2 Necromancer, PoE summoner builds, D3 Witch Doctor).

**§ 8 opportunity scan trigger:** BC-target Axis 2A bin = `proxy-light` or `proxy-heavy`, AND substrate cultural-tradition has military/spiritual unit pool (Architecture B: faction-anchor lookup per § 8.6).

**η-coefficient interpretation:** high when BC-target explicitly targets proxy-density — this is the primary alteration for proxy-heavy kits. Low for solo-target kits.

**Implementation surface:** generation time (proxy-spawn-template structure per § 8.4 + § 8.6 schema). Sim must support proxy entity spawning (deferred per BC-axes-lock § 5 sim deferral matrix for proxy-light/heavy).

**Build-time or runtime:** build-time template; runtime execution per fight (proxy spawns are fight-time events).

**Implementation constraint:** proxy bins (proxy-light/proxy-heavy) are currently DEFERRED per BC-axes-lock doc § 5 sim deferral matrix — current sim supports solo only. This means the § 8 proxy-spawn extension is a v1.1+ implementation target, not v1.

---

### 2.8 Zone-control (Death and Decay class)

**Genre mechanism:** creates persistent zones that modify subsequent skill behavior within the zone. Operationally: `zone_modifier = {skills_in_zone: bonus_damage_multiplier, enemies_in_zone: debuff}`.

**§ 8 opportunity scan trigger:** Axis 1 (engagement profile) bin = `mid-slow` or `ranged-slow` AND Axis 2 (damage geometry) bin = `large-AOE` — stationary or slow-moving ranged kits benefit most from zone-control because they hold position long enough to leverage zone persistence.

**η-coefficient interpretation:** high when tempo is low (low-tempo zone → full zone duration utilized), amplitude is spiky (zone amplifies burst window), and substrate has ritual/control cultural-tradition (druidic, necromantic, earth/holy WIS coupling).

**Implementation surface:** fight engine skill-execution layer. Requires `zone_effect` type in skill schema + zone-tracking state in simulation. Non-trivial sim extension.

**Build-time or runtime:** runtime — zones are created and expire per fight. The rule that skills create zones is build-time; zone execution is runtime.

---

### 2.9 Geometry-collapse / Concentrated Effect (range-for-amplitude trade)

**Genre mechanism:** trades geometry breadth for amplitude spike. Operationally: `aoe_radius *= collapse_factor`, `damage_multiplier *= amplitude_factor`.

**§ 8 opportunity scan trigger:** Axis 3B = `spiky` amplitude AND Axis 2 = `large-AOE` in BC-target — the archetype that wants burst but is built around AOE. Concentrated Effect narrows AOE in exchange for spike amplification.

**η-coefficient interpretation:** high when BC-target wants spiky amplitude but the kit's primary skills are AOE-by-base (earth/wind WIS-scaling, AoE geometry). The collapse trades unused AOE area for the requested spike.

**Implementation surface:** loadout-resolution layer. Apply `aoe_radius *= 0.5` and `damage_multiplier *= 1.5` (canonical PoE Concentrated Effect proportions) as kit modifiers. Simple stat application.

**Build-time or runtime:** build-time only.

---

### 2.10 Conditional-modifier (Pain Attunement / Heart Stopper class)

**Genre mechanism:** ties a stat bonus to a runtime condition. Operationally: `damage_bonus = f(current_hp_fraction)` — bonus fires when a condition holds during the fight.

**§ 8 opportunity scan trigger:** Any BC-target with Axis 4 = `glass` (low eHP builds that regularly enter low-HP threshold) OR high-variance amplitude builds that spike damage when near-death creates a strategic tension.

**η-coefficient interpretation:** high for glass-cannon kits where the low-HP condition is a design feature, not a failure state. Creates a skill-expression pattern (stay low, deal maximum damage) unique to this kit.

**Implementation surface:** fight engine combat arithmetic. Requires a per-tick `condition_check` hook that evaluates `current_hp < threshold` and applies bonus. Moderate sim extension.

**Build-time or runtime:** runtime condition evaluation per tick; the rule is build-time.

---

## 3. Implementation pattern proposal

### 3.1 Architecture recommendation: Scored-Candidate Strategy Registry

**Recommended pattern: scored-candidate strategy registry.**

The § 8 algorithm should be implemented as a scored-candidate strategy registry with the following components:

```python
# Strategy registry (authored once; populated from § 7 regime-change palette)
REGIME_CHANGE_STRATEGIES = [
    ResourceConversionStrategy(),      # Blood Magic class
    ResourceBufferStrategy(),          # Mind Over Matter class
    MechanicReplacementStrategy(),     # Vaal Pact class
    TradeOffStrategy(),                # Resolute Technique class
    ElementConversionStrategy(),       # Avatar of Fire class
    DefensiveConversionStrategy(),     # Iron Reflexes class
    GeometryCollapseStrategy(),        # Concentrated Effect class
    ZoneControlStrategy(),             # Death and Decay class
    ConditionalModifierStrategy(),     # Pain Attunement class
    ProxySpawnStrategy(),              # Summoner class (v1.1+ pending sim extension)
]

# Per-strategy interface
class RegimeChangeStrategy(ABC):
    @abstractmethod
    def opportunity_scan(self, bc_target: BCTarget, substrate: SubstrateWeapon) -> float:
        """Return η-score in [0.0, 1.0]; 0.0 = not applicable to this kit."""
        ...
    
    @abstractmethod
    def generate_alteration(self, bc_target, substrate, tier_coefficient) -> AlterationOutput:
        """Produce the § 8.4 output bundle for this alteration type."""
        ...
    
    @property
    @abstractmethod
    def manifestation_preference(self) -> Literal["T4_active", "rank2_passive", "rank3_passive"]:
        """Which tree manifestation this strategy prefers."""
        ...
    
    @property
    @abstractmethod
    def sim_prerequisite(self) -> Optional[str]:
        """Sim extension required (None = no extension needed; str = extension name)."""
        ...
```

**Selection algorithm per kit:**

```python
def select_mechanic_alteration(bc_target, substrate, tier_coefficient, kit_composition):
    candidates = []
    
    for strategy in REGIME_CHANGE_STRATEGIES:
        # Skip strategies with unmet sim prerequisites
        if strategy.sim_prerequisite and not sim_supports(strategy.sim_prerequisite):
            continue
        
        eta = strategy.opportunity_scan(bc_target, substrate)
        if eta > ETA_FLOOR_THRESHOLD:  # proposed: 0.35
            candidates.append((eta, strategy))
    
    if not candidates:
        return None  # Kit produces no mechanic-alteration (rank-2 only build)
    
    # Select highest-η candidate
    best_eta, best_strategy = max(candidates, key=lambda x: x[0])
    alteration = best_strategy.generate_alteration(bc_target, substrate, tier_coefficient)
    alteration.estimated_eta = best_eta
    
    return alteration
```

### 3.2 Why this pattern (vs alternatives)

**Alternative A: Function composition chain.** Each regime-change type is expressed as a pure function that transforms a `KitState` object: `transformed_kit = f3(f2(f1(base_kit)))`. This is elegant in functional languages. The problem for Reincarnated: multiple regime-change types are not composable — resource-conversion + element-conversion compose fine, but resource-conversion + defensive-conversion may conflict (HP-cost kit with armor-stacking is a valid design space; HP-cost kit with instant-leech disabling regen is a conflicting state). The strategy registry pattern handles conflicts explicitly through the opportunity_scan scoring, which can return 0.0 for conflict cases. Function composition requires a separate conflict-resolution layer, adding complexity without structural benefit.

**Alternative B: Decorator chain.** Each regime-change type is a decorator applied to the skill object at generation time. This is the correct pattern for additive modifiers (stat boosts), but creates deep object hierarchies for categorical alterations — a `VaalPactDecorator(BloodMagicDecorator(BaseKit))` is harder to inspect, diff, and debug than a flat `AlterationOutput` struct. The strategy registry produces an explicit `AlterationOutput` bundle per § 8.4 that Phase 5 cohesion coalescence can inspect without traversing a decorator chain.

**Alternative C: LLM-judge for candidate selection.** Use the Phase 5 LLM to select the alteration rather than a heuristic η-score. This adds per-kit LLM cost at Phase 2, which § 8.5 explicitly prohibits: "Algorithm runs without LLM at decision layer; LLM call ONLY at Phase 5 cohesion naming." The strategy registry keeps LLM out of the selection path.

**Alternative D: Hand-authored per-kit T4 catalogue (original v1.1 approach, superseded).** Per § 8.5 AMENDMENT 2026-05-24: hand-authoring T4s in the abstract is "meaningless (T4s are per-kit/per-substrate-anchor); algorithm IS the v1 T4 deliverable." The strategy registry implements this.

### 3.3 Per-layer architectural fit

| Phase | § 8 role | Strategy registry touchpoint |
|---|---|---|
| Phase 2 generation (rocket) | Algorithm fires; strategy selected; alteration output bundle produced | `select_mechanic_alteration()` called here; output bundle stored on kit |
| Phase 3 convergence (gamora) | Sim resolves alteration rules in combat arithmetic | Each strategy's `sim_prerequisite` determines whether kit routes to deferred-evaluation pool |
| Phase 4 archive insertion (gamora) | No § 8 involvement; kit + alteration inserted as unit | Alteration output bundle stored on archive entry |
| Phase 5 cohesion coalescence (rocket/star-lord) | LLM names the alteration; spirit-guide explainer triggered | AlterationOutput.alteration_type → template selection → LLM blank-filling per D7 |
| Phase 7 joint gate (gandalf + jack-ryan + Matt) | Gate-2 reviews alteration viability | AlterationOutput inspectable; η score reviewable |

### 3.4 Fight engine layer vs loadout-resolution layer — which strategies need which

| Strategy | Loadout-resolution layer | Sim/fight-engine layer | Phase 5 LLM layer |
|---|---|---|---|
| Resource-conversion | Yes (cost_resource_override) | No | Yes (naming) |
| Resource-buffer | Yes (rule set at build-time) | Yes (per-hit damage routing hook) | Yes |
| Mechanic-replacement | Yes (regen/leech flags) | Yes (leech resolution) | Yes |
| Trade-off | Yes (hit_override, crit_override) | No | Yes |
| Element-conversion | Generation-time (skill.element) | No | Yes |
| Defensive-conversion | Yes (stat conversion) | No | Yes |
| Geometry-collapse | Yes (radius + damage modifiers) | No | Yes |
| Zone-control | Yes (skill schema: zone_effect tag) | Yes (zone state tracking) | Yes |
| Conditional-modifier | Yes (condition rule on kit) | Yes (per-tick condition evaluation) | Yes |
| Proxy-spawn | Generation-time (template) | Yes — DEFERRED (proxy AI, spawn, HP) | Yes |

**Sim extension summary:** 4 of 10 strategies require sim extension (resource-buffer damage routing, leech-replacement resolution, zone state tracking, conditional-modifier per-tick evaluation). Proxy-spawn requires the most extensive extension and is already deferred per BC-axes-lock sim deferral matrix. The 6 loadout-resolution-only strategies (resource-conversion, trade-off, element-conversion, defensive-conversion, geometry-collapse + trade-off variants) are implementable with zero sim extension — these form the natural v1 implementation subset.

---

## 4. Complexity analysis

### 4.1 Per-kit runtime compute envelope

**Strategy registry scan (per kit):**
- N_strategies = 10 (regime-change palette)
- Per-strategy opportunity_scan: O(A) where A = BC-axis dimensions scanned = ~9 axes
- Total: O(N × A) = O(10 × 9) = 90 operations per kit

This is negligible. Phase 3 convergence (run_spatial_gauntlet across 50 iterations) dominates by multiple orders of magnitude. The strategy registry adds zero meaningful compute cost to Phase 2.

**Strategy alteration generation (per kit, once candidate selected):**
- O(1) for loadout-resolution strategies (static parameter assignment)
- O(1) for generation-time strategies (element assignment)
- O(1) for rule-attachment strategies (zone_effect tag, condition rule)

Phase 2 total § 8 cost: effectively O(1) per kit.

### 4.2 Complexity scaling per keystone count

The question of "per-keystone-count complexity scaling" translates in the strategy registry model to scaling with palette size P:

| Palette size (P) | Scan cost per kit | Generation cost | Memory |
|---|---|---|---|
| 10 (current § 7 estimate) | 90 ops | O(1) | ~1 KB per kit (AlterationOutput struct) |
| 20 (expanded palette) | 180 ops | O(1) | ~1 KB |
| 50 (full genre coverage) | 450 ops | O(1) | ~1 KB |

**Verdict:** linear in palette size; practically free at any foreseeable palette scale. The constraint is not compute but design completeness — each strategy in the registry requires a well-specified opportunity_scan and generate_alteration implementation. Adding a new regime-change type is O(1) compute but O(N) design effort.

### 4.3 Comparison to PoE/PoE2 hand-designed alternative

| Property | PoE/PoE2 hand-designed | Reincarnated § 8 strategy registry |
|---|---|---|
| Per-keystone authoring cost | ~20-40 hrs per keystone (design + playtest + balance) | Per-strategy implementation ~8-16 hrs once; zero marginal cost per additional kit |
| Per-player-character keystone variety | Same ~18-30 keystones for all characters | Per-kit unique alteration (theoretically unlimited variety) |
| Thematic fit to kit's cultural identity | None — keystones are substrate-agnostic | Architecture B: strategy selection informed by substrate cultural-tradition and element coupling |
| Balance scalability | Each new keystone requires full playtest budget | Balance validated per-kit via jack-ryan Gate-2 + Phase 3 sim convergence |
| Player-legibility of unique mechanics | Universal — same mechanic for all players who invest in it | Per-kit unique — requires spirit-guide explainer pattern per § 9 |
| Design space covered | GGG-curated ~18-30 concepts | Engine-discoverable: limited only by palette breadth |

**Cost/benefit verdict:** the strategy registry is strictly superior to hand-designed keystones at the per-kit scale Reincarnated targets (~37 v1 forms across ~22 cells). At PoE's scale (millions of players; ~30 shared keystones for the entire player base), hand-design amortizes per-keystone cost across a massive player base. At Reincarnated's per-kit generation scale, hand-design would require ~37 bespoke keystone designs before a single form is finalized — an authoring cost GGG would allocate a full design team sprint to, but which the strategy registry executes at zero marginal cost per additional kit.

---

## 5. Cheapest-refuting-test (per Discipline #19.1)

### 5.1 The claim to refute

The § 8 algorithm's core claim: **the committed mechanic-alteration actually shifts the kit's measured BC profile in the predicted direction.** Specifically: a resource-conversion alteration should measurably shift Axis 5 bin toward `HP-economy`; a geometry-collapse alteration should measurably shift Axis 3B toward `spiky`; a trade-off alteration should shift crit_rate to 0 while raising hit_chance to 1.0.

If the alteration does not produce the predicted BC shift, the η-coefficient scoring is mis-calibrated and the algorithm is producing alterations that don't meaningfully differentiate kits.

### 5.2 Test design

**Test name:** BC-shift validation sweep

**Scale:** 10-15 kits, spanning diverse BC-target cells (minimum: cover at least 5 of the 6 loadout-resolution-only strategy types)

**Procedure:**
1. Generate kits using Phase 2 algorithm with § 8 active; record `AlterationOutput` per kit
2. Run Phase 3 convergence WITHOUT the alteration active (baseline BC measurement)
3. Run Phase 3 convergence WITH the alteration active (altered BC measurement)
4. For each kit: compute `bc_shift = altered_bc - baseline_bc` on the axis most predicted to shift
5. Verify: for the alteration type committed, the predicted shift direction matches observed shift direction

**Pass threshold:**
- Direction correct: bc_shift on predicted axis has the correct sign for ≥ 80% of kits (8/10 minimum)
- Magnitude meaningful: |bc_shift| on predicted axis ≥ 0.1 BC-units for ≥ 60% of kits (6/10)

**Fail conditions (refuting signals):**
- Direction wrong (< 50% correct sign): strategy's opportunity_scan is selecting wrong BC-target scenarios; re-examine the axis-trigger conditions
- Direction correct but magnitude near-zero (< 0.05 on predicted axis for ≥ 80% of kits): the alteration is not strong enough to produce meaningful BC differentiation; re-examine the alteration parameter magnitudes (e.g., geometry-collapse radius factor too mild)
- Direction correct, magnitude meaningful, but unexpected secondary shifts appear: alteration is producing unintended BC perturbations; refine generate_alteration to control secondary effects

**Compute cost:** 10-15 kits × 2 runs (baseline + altered) × Phase 3 convergence cost (~10 min/kit per multi-dim convergence algorithm). Total: ~200-300 min. One day of compute if run overnight.

**Why this is the cheapest refuting test:** the alternative (run full v1 archive generation with § 8 active, then do post-hoc cluster analysis) would require completing Phase 2 implementation, generating all 37+ v1 forms, running Phase 5 cohesion, and doing cluster analysis — estimated weeks of pipeline work. The BC-shift sweep short-circuits to the load-bearing claim with a ~200-300 min compute budget.

### 5.3 Alternative cheapest-refuting-test (if compute budget is tighter)

**Static η-calibration check:** before running any generation, write 5-10 hand-crafted test BC-target inputs with known expected strategy selections (e.g., `bc_target = {resource_economy: "HP-economy", defensive_profile: "glass"}` → expected strategy = `ResourceConversionStrategy`). Run `select_mechanic_alteration()` and verify the expected strategy wins at η ≥ ETA_FLOOR_THRESHOLD. This tests the scoring logic without Phase 3 convergence. Cost: ~5 minutes. This is the absolute cheapest refuting test for the selection logic, though it does not validate the BC-shift magnitude claim.

---

## 6. Resource-bounds projection

### 6.1 Per-kit Phase 2 cost (§ 8 contribution only)

| Component | Operations | Time (estimated) | Memory |
|---|---|---|---|
| Strategy registry scan (10 strategies × 9 axes) | 90 comparisons | < 1 ms | < 1 KB |
| Alteration generation (single strategy, O(1)) | ~20 attribute assignments | < 1 ms | ~500 bytes AlterationOutput |
| Phase 5 LLM call (naming, not selection) | 1 LLM API call | ~2-5 s (network-bound) | ~2 KB prompt |

§ 8's contribution to per-kit Phase 2 cost is negligible relative to Phase 3 convergence (est. 10+ min per kit for full multi-dim convergence). The § 8 algorithm does not add compute meaningful to the pipeline.

### 6.2 v1 full-run projection (37 forms)

| Stage | Per-kit cost | 37-form total |
|---|---|---|
| Phase 2 § 8 scan + generation | < 2 ms | < 74 ms |
| Phase 3 convergence (§ 8 alters sim arithmetic for 4 strategies) | ~10 min/kit (varies) | ~370 min total |
| Phase 5 LLM naming of alteration | ~3 s/kit | ~111 s total |

**No memory concern at any stage.** The AlterationOutput struct per kit is ~500 bytes; 37 kits × 500 bytes = ~18 KB. This is irrelevant at any foreseeable host configuration.

### 6.3 Sim extension cost (for strategies requiring sim extension)

The 4 sim-extension strategies (resource-buffer damage routing, leech-replacement, zone-control, conditional-modifier) add per-hit or per-tick evaluation hooks to the fight engine. The computational impact depends on fight length and hit rate:

| Extension type | Per-fight overhead | Notes |
|---|---|---|
| Damage routing hook (resource-buffer) | O(hits_per_fight) × O(1) per hit | Minimal: adds one comparison and one arithmetic op per hit |
| Leech-replacement resolution | O(leech_events) × O(1) | Minimal: modifies leech-resolution path |
| Zone state tracking | O(tick_rate) × O(active_zones) | Moderate: requires per-tick zone expiry check; linear in zone count |
| Conditional-modifier evaluation | O(tick_rate) × O(conditions) | Moderate: per-tick condition check; linear in condition count |

At 60-tick fights with typical hit rates (2-6 events/s per Axis 3A = 120-360 events per 60s fight), damage routing and leech-replacement add < 1% fight-engine overhead. Zone tracking and conditional-modifier add < 5% overhead at ≤ 3 simultaneous zones/conditions. None constitute a resource risk.

---

## 7. Spirit-guide explainer pattern — implementation surface per § 9

The spirit-guide explainer pattern (§ 9 of skill-system doc) converts the cognitive-load risk of per-kit novel alterations into a story win. The implementation surface is straightforward given the strategy registry output:

### 7.1 Template set required

One template per regime-change type in the palette = 10 templates for v1 palette (9 non-proxy strategies + 1 proxy template for v1.1). The templates are slot-based per D7 AI-tell discipline:

```
"Summoner, [your spirit's name] has awakened [alteration_description].
If you would like a walkthrough, [spirit_guide_name] can explain how to make the most of it."

→ Inner walkthrough template per alteration_type:
  resource_conversion: "Your spirit's skills now draw from their lifeforce rather than arcane reserves. 
    This makes every cast a wager — but it means [cost_resource_name] is no longer a constraint 
    on how aggressively you push the fight."
  
  trade_off: "Your spirit has abandoned the pursuit of critical precision entirely. 
    Every strike will land — but none will surge past ordinary limits. 
    Consistency is the weapon now."
  
  element_conversion: "All of your spirit's elemental expressions have converged on [element_name]. 
    The diversity is gone, but the unity unlocks [element_name] resonances 
    that cross-element kits cannot access."
  
  [etc., one template per alteration_type]
```

### 7.2 Trigger condition

The spirit-guide explainer triggers when `alteration.estimated_eta > ETA_FLOOR_THRESHOLD` — i.e., whenever the algorithm committed a meaningful alteration. The `AlterationOutput` struct carries `alteration_type` which maps directly to template selection at Phase 5.

### 7.3 Cognitive load surface

The genre literature confirms the cognitive load risk. PoE's design philosophy for keystones is explicit: each keystone "always offers significant power, but also always offers a significant weakness — giving players a different style of gameplay to build around and altering the value of other stats." This implies player education is needed. In PoE, that education comes from community wikis, streamers, and build guides. Reincarnated cannot rely on those at v1 scale (solo gameplay; new player cohort). The spirit-guide explainer replaces the external education surface with an in-fiction system.

**Implementation note:** the explainer must appear BEFORE the player's first fight with the altered kit, not after — the player needs to understand the alteration before it surprises them in combat. First-form-encounter trigger is the correct UX timing.

---

## 8. Open questions for rocket to resolve at implementation time

These were named as open questions in the dispatch § 5. Legolas findings per question:

**Q1: Per-keystone implementation pattern (function composition vs decorator chain vs strategy registry vs other)?**
Recommendation: **strategy registry** (per § 3 analysis). Function composition is elegant but requires explicit conflict-resolution logic. Decorator chain produces deep hierarchies difficult to inspect. Strategy registry is flat, inspectable, and produces the `AlterationOutput` struct that Phase 5 requires.

**Q2: Whether keystones operate at fight engine layer vs loadout-resolution layer vs both?**
Finding: depends on the strategy type (per § 3.4 table). 6 of 10 strategies operate at loadout-resolution layer only (zero sim extension). 4 require sim extension for runtime hooks. Proxy-spawn requires the most extensive sim extension and should be deferred to v1.1 per the existing BC-axes-lock sim deferral matrix.

**Q3: LLM-judge vs heuristic-judge for keystone-altering-conditions?**
Recommendation: **heuristic-judge (strategy registry opportunity_scan)** for the selection decision. LLM-judge for naming and explainer text only (Phase 5). The § 8.5 constraint prohibits LLM at the decision layer. The heuristic η-score is a deterministic, reproducible function of BC-target + substrate — auditable, debuggable, no latency or API-cost implications. LLM-judge for condition evaluation would add per-kit API cost, introduce non-determinism, and break the separation between mechanical generation (Phase 2) and narrative generation (Phase 5).

---

## 9. Knowledge gaps not resolved

1. **η-coefficient threshold calibration.** The `ETA_FLOOR_THRESHOLD = 0.35` proposed in § 3.1 is a prior estimate. The cheapest-refuting-test in § 5 will generate empirical signal for calibrating this threshold. The BC-shift magnitude pass condition (|bc_shift| ≥ 0.1) implicitly calibrates what η value produces "meaningful" shifts.

2. **Strategy opportunity_scan implementation specifics for each regime-change type.** This document provides the scan trigger conditions and axis logic at the conceptual level. Rocket must implement the specific arithmetic per strategy (e.g., exactly what constitutes `substrate.cultural_tradition.fire_resonance_score > threshold` requires a threshold value from Elrond's substrate data).

3. **Phase 3 simulation impact of damage-routing hook (resource-buffer strategy).** The claim that the damage-routing hook adds < 1% overhead is an estimate. The cheapest-refuting-test in § 5 will also generate per-fight timing data that can be inspected for sim overhead.

4. **Conflict resolution between strategies.** If two strategies both score above ETA_FLOOR_THRESHOLD for the same kit (e.g., resource-conversion η=0.61 + element-conversion η=0.58), the current proposal selects the highest-η winner. Whether two alterations can coexist on a single kit (e.g., HP-cost skills that also convert to fire) is an open design question for the Stage 0 design call. The strategy registry accommodates either: single-winner selection (current proposal) or multi-winner composition (requires conflict-resolution logic addendum).

5. **T4 active vs passive manifestation decision rule.** The `manifestation_preference` property on each strategy is proposed but not fully specified. The general rule from § 8.2: T4 active if the alteration affects the entire kit globally; rank-2 or rank-3 passive if the alteration affects a specific node's behavior (adjacent-node alteration). The strategy registry's `manifestation_preference` encodes this per strategy type, but the exact condition for "global" vs "node-specific" requires a Stage 0 design call lock.

---

## 10. Source list

**Primary sources (project canonical docs):**
- `canonical/story/skill-system-2026-05-24.md` — § 8 architectural definition, regime-change palette, spirit-guide explainer pattern
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes operational specification; sim deferral matrix
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md` — Architecture B 8-phase pipeline
- `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` — BC convergence algorithm; Tier 4 keystone discrete selection; trigger/conditional interaction layer
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #18 (methodology-before-execution), #19.1 (cheapest-refuting-test), #1 (math-before-code)

**Secondary sources (web research, 2026-05-25):**
- PoE 2 keystone mechanics survey: https://www.aoeah.com/news/3679--poe-2-passive-skill-tree-keystones-locations--effects--path-of-exile-2-keystone-tier-list
- PoE 2 keystone list and categories: https://www.mmojugg.com/news/every-poe-2-passive-keystone-we-know-so-far.html
- PoE 2 keystone tier list and trade-off structure: https://www.rpgstash.com/blog/path-of-exile-2-best-keystone-passives-guide
- PoE 2 keystone philosophy: https://www.mmoexp.com/News/path-of-exile-2-best-keystone-passives-to-build-around.html
- PoE 2 Giant's Blood design: https://www.u4gm.com/path-of-exile-2/blog-unleashing-power-fantasies-in-path-of-exile-2-the-giant-s-blood-keystone
- PoE 1 Resolute Technique: https://www.poewiki.net/wiki/Resolute_Technique
- PoE 1 Avatar of Fire: https://www.poewiki.net/wiki/Avatar_of_Fire
- PoE 1 Ancestral Bond: https://www.poewiki.net/wiki/Ancestral_Bond
- PoE 1 Necromantic Aegis: https://www.poewiki.net/wiki/Necromantic_Aegis
- PoE 1 Mind Over Matter: https://www.poewiki.net/wiki/Mind_Over_Matter
- Last Epoch mastery system overhaul: https://www.lastepochtools.com/news/article/remastering-masteries-overhauling-the-passive-system-1607
- Diablo 4 Paragon board design: https://maxroll.gg/d4/resources/paragon-boards
- PoE keystone Legion league design discussion: https://massivelyop.com/2019/06/23/path-of-exile-shares-more-eystone-design-discussion-from-the-legion-league/
- QD MAP-Elites research: https://arxiv.org/pdf/1906.05175 (Interactive Constrained MAP-Elites)
- Automatic game mechanic generation: https://arxiv.org/pdf/1908.01420 (Automatic Game Design via Mechanic Generation)
- Strategy/Decorator pattern in game development: https://onewheelstudio.com/blog/2020/8/16/strategy-pattern-composition-over-inheritance
- QD in dungeon design: https://comnplayscience.eu/wp-content/uploads/2019/10/Gravina-et-al.-2019-Procedural-Content-Generation-through-Quality-Dive.pdf
