# Session 1 — T4 Architecture Design Spec

**STATUS:** DRAFT — Matt-authorized 2026-06-12 (Pattern B session); spec translation from hypothesis doc + BC axes lock + today's design decisions; ready for Session 1 architecture session
**Author:** gandalf
**Date:** 2026-06-12
**Grounding docs:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — PRIMARY source
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — BC axis definitions
- `canonical/47-damage-scaling-architecture-2026-05-27.md` — current T4 architecture (two-layer; DIRECT_DAMAGE_AMPLIFICATION scaffold)
- Today's T4 design notes (Pattern B session 2026-06-12)
- Engine state: flag only — flag issues to Matt, do not let engine state constrain design

> **NORMALIZATION PASS (gandalf, 2026-06-12, Matt-authorized):** this spec was originally authored in a mobile session without access to the BC axes lock doc; axis bin vocabulary has been re-pointed to the locked definitions (`qd-engine-bc-axes-lock-2026-05-20.md` § 3). Two conventions introduced by the pass apply throughout:
> 1. **Generation-time vs measurement-time:** BC axis bins are MEASURED (from skill metadata weights or fight telemetry). Eligibility gates fire at GENERATION time, so gates below bind to generation-time structural properties (declared `energy_type`, skill geometry metadata, CC tags, cost types); where a bin name appears in a gate it denotes the kit's **predicted** bin computed at generation from skill metadata, not a post-hoc measurement.
> 2. **Three geometry layers:** engine rich skill-geometry (24-type vocabulary, `generation/geometry_derivation.py` — includes `beam_channel`, `chain_lightning`, `totem`, …) → spatial 6-type enum (circle/cone/line/point/mixed/none) → Axis 2 BC bins (single-target/small-AOE/large-AOE/chain/multi-spawn, damage-weighted argmax). The terms "AoE_burst" and "DoT_stack" used in the original draft belong to NONE of these layers and have been replaced. DoT-stacking is a Layer 2 `stackability` property, not a geometry.
> Delta summary: `gandalf/notes/2026-06-12-normalization-pass-delta-summary.md`.

---

## 0. Design mandate

Deliver 4,000 kit seeds to the engine, receive a minimum of 400 survivors within win-rate band, maximally unique across descending priority of the 28 design categories. T4 strategy is the #1 player-experience-impact category. Session 1 must lock all 21 T4 strategies with engine-implementable pass/fail criteria for gamora and rocket.

**Not a constraint:** doc 47 § 4.6.2 existing catalog entries (current 6 strategies are starting points, not ceilings). Design from the hypothesis doc unconstrained.

---

## 1. Current T4 catalog (baseline)

### 1.1 Scaffold to retire (Discipline #39)

| Strategy | Layer | Status |
|---|---|---|
| **DIRECT_DAMAGE_AMPLIFICATION** | Primary (universal) | **RETIRE at Session 1** — Discipline #39 scaffold; 1.75× vs preferred encounter type; guaranteed in-band but zero felt identity; replaced by full 21-strategy catalog |

The Primary T4 universal slot is retired. All T4 slots draw from the 21-strategy catalog per eligibility gate.

### 1.2 Six current strategies (carry forward as-is)

| # | Strategy | Mechanic | Eligibility gate | Locked magnitude |
|---|---|---|---|---|
| 1 | **ELEMENT_CONVERSION_MONO** | Single-element +50% multiplicative; composes downstream of element-chain multiplicatives | Single-element kit architecture | 1.50× LOCKED (doc 47 v1.2) |
| 2 | **ELEMENT_CONVERSION_HYBRID** | Hybrid +25% multiplicative across dual-element coverage | Hybrid 2-element kit architecture | 1.25× LOCKED (doc 47 v1.2) |
| 3 | **ELEMENT_CONVERSION_PHYSICAL** | Physical +25% additive elemental + ailment trigger per element-support flag | Physical hybrid damage scaling path | 0.25 additive + ailment LOCKED (doc 47 v1.2) |
| 4 | **DEFENSIVE_TRADEOFF** | shadow + holy immunity (t4_chaos_immune flag); mana shield defensive layer (mana absorbs incoming damage) | energy_type == mana + mana shield skill in chain | REINSTATED 2026-06-12; mana shield behavior deferred to this session |
| 5 | **GEOMETRY_COLLAPSE** | Collapses kit's secondary geometry into primary for amplification | Dominant geometry: ≥60% of kit's predicted damage share in a single Axis 2 bin (single-target / small-AOE / large-AOE / chain / multi-spawn); ≥4 skills in dominant bin | Empirical — Session 1 target: derive spec from mechanism |
| 6 | **RESOURCE_CONVERSION** | Converts surplus resource pool into damage or utility output | charge-stack OR overflow resource economy type (Axis 5) | Empirical — Session 1 target: derive spec from mechanism |

**Session 1 action on strategies 5 + 6:** GEOMETRY_COLLAPSE and RESOURCE_CONVERSION are marked "empirical" in doc 47. Session 1 converts them to locked mechanics with explicit pass/fail criteria.

---

## 2. Multi-node T4 selection architecture

### 2.1 Chain count → T4 node count (preserved from doc 47 § 4.6)

| Skill chain count | T4 node slots | Selection rule |
|---|---|---|
| 2 chains | 1 T4 slot | Pick 1 eligible strategy from 21-strategy catalog |
| 3 chains | 2 T4 slots | Pick 2 eligible strategies; must be from different strategy families (no two proxy-family strategies unless DUAL_PROXY + proxy-family are paired) |
| 4 chains | 3 T4 slots | Pick 3 eligible strategies; at most 2 from same family |

**Retired:** Primary (universal) slot = DIRECT_DAMAGE_AMPLIFICATION. All slots now draw from the 21-strategy catalog.

**Selection eligibility:** each strategy's eligibility gate must be satisfied by the kit's properties at generation time. Strategies with conflicting eligibility gates (e.g., DEFENSIVE_TRADEOFF requires mana energy_type; RESOURCE_CONVERSION requires charge-stack or overflow energy_type) are mutually exclusive slots.

### 2.2 T4 strategy families (for multi-slot conflict rules)

| Family | Strategies |
|---|---|
| ELEMENT | ELEMENT_CONVERSION_MONO, ELEMENT_CONVERSION_HYBRID, ELEMENT_CONVERSION_PHYSICAL, ELEMENTAL_ECHO |
| DEFENSE | DEFENSIVE_TRADEOFF, SACRIFICE_ASCENDANCY |
| GEOMETRY | GEOMETRY_COLLAPSE, GEOMETRY_INVERSION |
| RESOURCE | RESOURCE_CONVERSION, TEMPORAL_CHARGE, MOMENTUM_CASCADE |
| PROXY | PROXY_ASCENSION, PROXY_SOVEREIGNTY, PROXY_FISSION, PROXY_INVERSION, PROXY_CONVERGENCE, DUAL_PROXY |
| COMPANION | COMPANION_CONTRACT, MONSTER_PACT |
| COMBAT | NETWORK_AMPLIFIER, RESONANCE_LOOP, ELEMENTAL_ECHO |

Multi-slot conflict rule: at most 1 strategy from ELEMENT family per kit (variants are mutually exclusive). At most 1 from DEFENSE family. No restriction across families.

---

## 3. Fifteen new T4 strategies

### 3.1 Proxy family (6 strategies)

---

#### PROXY_ASCENSION

**Eligibility:** Kit has ≥1 Tier 1 mechanical proxy type already in chain

**Capstone mechanic:** The existing proxy type upgrades to the next behavioral tier at T4:
- Passive Fighter → Autonomous Caster (gains independent skill rotation from a subset of player's skills)
- Totem/Turret → Range-Gated Turret (activates/deactivates based on player proximity; +15% player damage when adjacent)
- Volatile Emitter → Slot-Queue Emitter (becomes a queued slot emitter; passive per-tick + burst-on-evoke dual mode)
- Other types: upgrade table defined in Session 2 proxy spec

**Pass/fail criteria (gamora):**
- Upgraded proxy demonstrates behavior profile matching the tier above its original type
- Proxy fight contribution increases measurably vs non-ASCENSION baseline (≥20% improvement in proxy-attributable damage or utility)
- Zero regression on existing non-proxy fight mechanics

**Seam:** gamora (proxy tier upgrade dispatch in ProxyCombatant + fight_engine)

---

#### PROXY_SOVEREIGNTY

**Eligibility:** Kit has Passive Fighter OR Golem proxy type; energy_type ≠ mana (mana reserved for DEFENSIVE_TRADEOFF); kit has ≥3 chains

**Capstone mechanic:** Primary proxy entity becomes a full parallel combatant — gains independent energy pool (charge-stack type; 10 stacks, accumulates on enemy hit), executes a 3-skill rotation autonomously from a pool drawn from the player's skills (1 skill per skill type: damage / CC / utility). Proxy participates in the fight loop as a full ProxyCombatant. Player's skill use does NOT control proxy timing.

**Pass/fail criteria (gamora):**
- Proxy executes ≥2 distinct skills per fight (not auto-attack only)
- Proxy contributes measurable independent damage tracked separately from player damage
- Proxy has its own energy state visible in fight telemetry
- Proxy can die and be re-summoned via capstone cooldown (20s); re-summon fires correctly

**Seam:** gamora (autonomous skill rotation in ProxyCombatant full tier)

---

#### PROXY_FISSION

**Eligibility:** Kit has Golem, Passive Fighter, OR Bodyguard proxy type; proxy must have HP tracking (mid or full tier)

**Capstone mechanic:** Proxy death event triggers Fission: the dying proxy splits into 2 sub-proxies at 60% original stats each (HP, damage). Each sub-proxy can Fission once more on death (producing 2 sub-sub-proxies at 60% of sub-proxy stats). Maximum entity count: 4 (1 → 2 → 4). Sub-sub-proxies do not Fission. Fission proxies expire after 30 seconds regardless of HP.

**Pass/fail criteria (gamora):**
- Proxy death event correctly triggers 2-entity spawn
- Sub-proxy stats = 60% ± 2% of parent stats
- Recursion cap enforced: sub-sub-proxies do not spawn new entities on death
- 30-second expiration fires correctly for all fission tiers
- Maximum 4 proxy entities active simultaneously; no overflow

**Seam:** gamora (proxy death event handler + Fission spawn mechanic in fight_engine)

---

#### PROXY_INVERSION

**Eligibility:** Kit has Bodyguard, Terrain Anchor, OR Warcry/Buff Spirit proxy type (defensive proxy types only)

**Capstone mechanic:** T4 inverts the proxy's functional role:
- Bodyguard → becomes Sacrificial: player can manually consume the Bodyguard for a burst damage event equal to 150% of the Bodyguard's remaining HP as direct damage to the nearest enemy
- Terrain Anchor → becomes Damage Amplification Zone: the anchor now amplifies player damage (not defense) within its radius by 40% for 8 seconds after placement
- Warcry/Buff Spirit → becomes Reverse-Buff: the spirit applies a debuff to enemies in range (equivalent magnitude to the original buff, applied as enemy damage reduction and movement slow)

**Pass/fail criteria (gamora + rocket):**
- Inverted proxy demonstrates the offensive behavior matching spec (not the original defensive behavior)
- Sacrificial inversion: burst damage formula = 150% remaining HP ± 5%; proxy expires after consumption
- Amplification zone: +40% player damage ± 2% within radius; expires after 8s; placement radius matches spec
- Reverse-buff: enemy stats reduced by equivalent magnitude to original player buff; duration matches original

**Seam:** gamora (proxy type transition at T4 capstone); rocket (proxy assignment in generation must flag INVERTIBLE types)

---

#### PROXY_CONVERGENCE

**Eligibility:** Kit has exactly 2 distinct Tier 1 proxy types (both must be from different proxy families: e.g., Fighter-family + Terrain-family, NOT two Fighter-family types)

**Capstone mechanic:** The two proxy types merge at T4 into a single Convergent Proxy entity combining their behaviors. Merge rules (defined per pair; examples):
- Passive Fighter + Terrain Anchor → Fighting Anchor: auto-attacks enemies while projecting a 40% damage amplification aura for the player
- Volatile Emitter + Resource Conduit → Harvest Bomb: travels to target, explodes for AoE damage, converts 25% of enemy HP lost in explosion to player resource generation
- Bodyguard + Warcry/Buff Spirit → Shielded Augmenter: absorbs hits AND emits player buff simultaneously at 70% efficiency of each type

Convergent Proxy has max HP = average of both parent types × 1.2; damage contribution = sum of both types × 0.8 (merge cost).

**Pass/fail criteria (gamora + rocket):**
- Convergent proxy demonstrates behaviors from BOTH parent types in same fight instance
- Convergent proxy HP and damage contribution match spec formula ± 5%
- No undefined pair combinations at generation (rocket enforces valid pair constraint at kit generation time)
- Each valid pair produces a deterministic named convergence behavior

**Session 1 action:** Define the full valid pair matrix (all combinations of 14 proxy types; select which are valid convergence pairs; define named behavior per valid pair). This is a design decision that must be resolved in Session 1.

**Seam:** gamora (convergence entity behavior dispatch) + rocket (proxy pair assignment + validity gate in generation)

---

#### DUAL_PROXY

**Eligibility:** Kit has exactly 1 Tier 1 proxy type; kit has ≥3 skill chains

**Capstone mechanic:** A second proxy type from a compatibility pool is unlocked. The second type is filtered to COMPLEMENT the existing type (no same-family duplicates; no convergence-conflicting pairs). Compatibility pool is pre-defined per primary proxy type. Examples:
- Primary = Passive Fighter → secondary pool: {Terrain Anchor, Warcry/Buff Spirit, Totem/Turret}
- Primary = Golem → secondary pool: {Resource Conduit, Warcry/Buff Spirit, Fragile Escort}
- Primary = Volatile Emitter → secondary pool: {Trap/Mine, Resource Conduit, Delayed Position Shadow}

Both proxies operate independently. No convergence between them (that's PROXY_CONVERGENCE).

**Pass/fail criteria (gamora + rocket):**
- Two distinct proxy types visible in fight telemetry operating simultaneously
- Secondary proxy type drawn from correct compatibility pool per primary type
- No cross-proxy interference (each operates on its own HP, targeting, and timing)
- Fight outcome shows measurable multi-proxy benefit vs single-proxy baseline

**Session 1 action:** Define the compatibility pool per primary proxy type (all 14 types need a pool).

**Seam:** gamora (multi-proxy fight loop; independent operation guarantee) + rocket (secondary proxy assignment per compatibility pool)

---

### 3.2 Companion and monster strategies (2 strategies)

---

#### COMPANION_CONTRACT

**Eligibility:** attribute ∈ {INT, WIS}; energy_type ∈ {mana, focus}; kit faction is defined (cultural lineage × period × register maps to a faction with companion pool)

**Capstone mechanic:** Unlocks a persistent NPC companion slot. Companion kit drawn from NPC/Mercenary season pool, filtered to player kit's faction. Companion persists across fights within a session. Player gears the companion separately (companion has a 4-slot gear loadout: weapon, armor, accessory, convergence item). Companion contribution modeled as a BC-archetype modifier vector applied to player kit's effective parameters (see companion modifier vector spec, Session 2).

**Convergence item slot:** The companion's 4th gear slot (convergence item) checks companion T4 + player T4 compatibility. On compatible pair: unlocks a named convergence aura (see convergence item design, § 4). On non-compatible pair: fallback effect (generic support buff, 50% reduced magnitude).

**Pass/fail criteria (gamora + rocket):**
- Companion modifier vector applies correctly to player kit baseline in sim
- Modifier stays within cap bounds across 400-kit pairing validation run
- Faction filter enforced: companion kit faction matches player kit faction
- Convergence item compatibility check fires correctly for valid and invalid pairs

**Seam:** gamora (companion modifier vector application) + rocket (companion kit assignment per faction filter) + star-lord (companion kit telemetry tracking)

---

#### MONSTER_PACT

**Eligibility:** element ∈ {shadow, holy} OR kit has a coercion-type skill in chain (defined as skill with CC + target_debuff semantic in Layer 2 mechanism dimensions); attribute = WIS

**Capstone mechanic:** Unlocks a captured/pacted monster slot. Monster drawn from monster season pool (Meshy pipeline), filtered by player kit's binding category eligibility:
- shadow element → spirit binding category
- holy element → radiant binding category
- coercion skill → physical chaining category

Monster companion contributes CC/debuff modifier vector (not raw damage): increases enemy CC duration, reduces enemy armor, or applies persistent terrain debuff. CC/debuff contribution modeled as modifier vector (see Session 2 monster modifier spec).

**Pass/fail criteria (gamora + rocket):**
- Monster modifier vector applies correctly
- Monster category matches binding eligibility filter
- Monster modifier type is CC/debuff-only (no raw damage contribution in Cycle 15; deferred)
- Modifier stays within cap bounds across pairing validation

**Seam:** gamora (monster modifier vector application) + rocket (monster assignment per binding category) + star-lord (monster season kit telemetry)

---

### 3.3 Combat and synthesis strategies (7 strategies)

---

#### MOMENTUM_CASCADE

**Eligibility:** Predicted Axis 2 bin ∈ {small-AOE, large-AOE, chain, multi-spawn} (any multi-target geometry bin); kit has ≥2 multi-target skills. *(Normalization note: the original draft's "damage tempo = burst OR sustained" clause was vacuous against the locked Axis 3A bins — low/medium/high events-per-second — and has been dropped; tempo does not gate this strategy.)*

**Capstone mechanic:** Each skill hit adds 1 Momentum stack (max 10). At 10 stacks: a Cascade fires — all enemies hit by any skill in the past 5 skill uses take 40% of the original hit's damage simultaneously. Cascade resets the stack counter. Creates a temporal damage-history explosion: the last 5 skill uses all land again at once.

**Pass/fail criteria (gamora):**
- Momentum stack state tracked in fight_engine; accumulates correctly per hit
- Cascade fires when stack reaches 10; stack resets to 0 after Cascade
- Cascade damage = 40% × sum of most-recent-5-uses' damage ± 3%
- Cascade targets: all enemies who received any hit in the most recent 5 uses
- Cascade does not itself generate Momentum stacks (no recursive cascade)

**Seam:** gamora (Momentum stack state machine + Cascade event in fight_engine)

---

#### ELEMENTAL_ECHO

**Eligibility:** Kit architecture = hybrid 2-element; kit_sub_element_1 ≠ null; kit has ≥3 skills with primary element

**Capstone mechanic:** Each skill use leaves an Echo tied to the sub-element. The Echo fires 1.5 seconds later at the same target for 35% of the triggering skill's damage, applying the sub-element (not the primary element). Each kit has exactly 1 active Echo at a time — a new skill use replaces the pending Echo. Rewards sustained engagement vs the same target.

**Pass/fail criteria (gamora):**
- Echo timer fires correctly at 1.5s ± 0.1s after triggering skill use
- Echo uses sub-element (not primary element) in damage resolver
- Echo damage = 35% of triggering skill damage ± 2%
- Only 1 active Echo at a time: new skill use cancels pending Echo and creates new one
- Echo generates no additional Echoes (no chain recursion)

**Seam:** gamora (Echo state tracking + delayed damage dispatch in fight_engine)

---

#### SACRIFICE_ASCENDANCY

**Eligibility:** Kit has ≥1 skill with an HP-cost mechanic (generation-time structural property; predicted Axis 5 bin = HP-economy); predicted Axis 4 bin ≠ glass (tank / mitigator / dodger acceptable); kit has ≥20% HP above safety floor of 20% at typical gauntlet fight entry

**Capstone mechanic:** Player voluntarily spends 15% current HP to activate Ascendancy state (15-second duration). During Ascendancy: +60% damage dealt; -30% incoming damage (momentum converts defense to offense). Ascendancy can be extended: re-activating at ≥12 seconds remaining resets the timer (requires another 15% HP). Ascendancy cannot activate below 25% HP (safety floor).

**Pass/fail criteria (gamora):**
- HP deduction triggers Ascendancy state correctly
- Damage multiplier = +60% ± 2% during state
- Incoming damage reduction = -30% ± 2% during state
- Extension mechanic: timer resets on re-activation if ≥12s remaining; HP cost applies again
- Safety floor: Ascendancy cannot activate at or below 25% HP; attempt at floor produces no effect
- Ascendancy state visible in fight telemetry

**Seam:** gamora (Ascendancy state machine in fight_engine; HP deduction event)

---

#### GEOMETRY_INVERSION

**Eligibility:** Dominant geometry: ≥60% of kit's predicted damage share in a single Axis 2 bin; kit has ≥4 skills in the dominant bin. *(For the Instant Actualization variant only, the gate is a Layer 2 property, not geometry: ≥60% of kit's predicted damage delivered via skills with `stackability = stacking` DoT mechanics.)*

**Capstone mechanic:** T4 capstone skill inverts the kit's primary delivery mode:
- AOE dominant (predicted Axis 2 ∈ {small-AOE, large-AOE}) → Focused Convergence: all potential AoE targets' damage is summed and delivered to a single designated target (full AoE damage on one enemy; zero on others). Magnitude cap: 4× single-target baseline.
- Single-target dominant (predicted Axis 2 = single-target) → Resonant Burst: single-target hit radiates 70% of damage as AoE to all enemies within 5 tiles of the primary target.
- DoT-stacking dominant (Layer 2 `stackability = stacking`; this is a mechanism-structural property, NOT an Axis 2 geometry bin) → Instant Actualization: all active DoT stacks on the target are consumed simultaneously for 80% of their remaining damage total as instant damage.

**Pass/fail criteria (gamora + rocket):**
- Capstone skill demonstrates inverted geometry behavior
- Damage calculations match spec formula ± 5%
- Geometry measurement (Axis 2 bin) shifts toward inverted geometry for fights using the capstone
- Generation correctly assigns capstone per dominant geometry type (rocket)

**Seam:** gamora (capstone geometry dispatch + stack-consume event) + rocket (capstone assignment per dominant geometry)

---

#### TEMPORAL_CHARGE

**Eligibility:** Declared `energy_type` = charge-stack (generation-time structural property; predicted Axis 5 bin = charge-stack — note the hold-vs-spend design question, Q9: whether a given charge-stack kit MEASURES into the Axis 5 charge-stack bin depends on its hold-vs-spend optimal rotation); kit has ≥1 skill with cast_time > 0 (not instant)

**Capstone mechanic:** Skills with cast_time > 0 gain a Charge Phase. Holding the skill input for 0.5s builds 1 Charge stack (max 5). Each Charge stack adds +25% damage multiplicatively. At 5 stacks (full charge), the skill's delivery upgrades one tier (engine rich-geometry terms): single-target delivery (e.g., `projectile_single`, `melee_single`) → circle AOE of radius 3 tiles at the target; existing AOE geometries → radius ×2, capped at arena-wide; DoT-applying skills → instant trigger (applies full DoT damage immediately). Releasing before max charge uses partial stacks proportionally.

**Pass/fail criteria (gamora):**
- Charge stacks accumulate at 1 per 0.5s while held; release at any stack count
- Damage multiplier per stack: +25% per stack (compound) ± 2%
- Geometry upgrade fires at max stacks (5); no upgrade at 1-4 stacks
- Partial charge (1-4 stacks): proportional damage bonus, no geometry change
- Charge state visible in fight telemetry

**Seam:** gamora (Charge state + geometry override in fight_engine; ProxyCombatant charge if proxy uses this skill)

---

#### NETWORK_AMPLIFIER

**Eligibility:** Predicted Axis 2B bin ∈ {mixed, control-pure} (locked bins: damage-pure <20% / mixed 20–60% / control-pure ≥60% control share, effect-budget weighted); kit has ≥3 distinct CC effect types drawn from the locked CC closed enum (stun, root, slow, freeze, fear, silence, blind, chill ≥30%, mind-control/charm — see Session 3 § 4)

**Capstone mechanic:** CC effects applied by the player generate a Network tag on the target. Tagged enemies take +35% damage from all sources (player and proxy) for the CC duration. On tagged enemy death: Network tag transfers to the nearest non-tagged enemy within 8m (1 transfer only; tag does not re-transfer). Network tag expires when CC duration expires or on tag-transfer death.

**Pass/fail criteria (gamora):**
- Network tag applies on any CC skill use
- Tagged enemy incoming damage = +35% ± 2% from all sources
- Tag expires with CC duration (tied to CC duration state in fight_engine)
- Death-transfer fires to nearest eligible enemy within 8m; no re-transfer from transferred tag
- No infinite propagation; tag chain terminates at 2 enemies maximum

**Seam:** gamora (Network tag state + damage modifier routing in fight_engine)

---

#### RESONANCE_LOOP

**Eligibility:** Kit has ≥2 skills sharing an element OR geometry type (Resonance Partner pair); kit cognitive_load ∈ {medium, high}; kit has ≥3 skill chains

**Capstone mechanic:** Two skills in the kit are designated Resonance Partners at generation (rocket assigns based on shared element/geometry type). When both Resonance Partners are used within a 3-second window (in any order), Resonance state activates (12-second window). During Resonance: the 3rd use of either Resonance Partner skill within the 12-second window deals 2.5× damage and triggers Shatter — all player skill cooldowns reset to 0. Resonance state ends immediately after Shatter. If the 3-second sequence window is broken (>3s between Partner uses), Resonance does not activate.

**Pass/fail criteria (gamora + rocket):**
- Resonance Partner pair assigned deterministically at generation (rocket)
- Resonance state activates correctly on both-Partners-within-3s sequence
- 3rd use within 12s window: damage = 2.5× ± 0.1×; Shatter fires (all cooldowns reset to 0)
- Resonance state ends after Shatter; must re-enter sequence to re-activate
- Window timeout (>12s without 3rd Partner use) clears Resonance state with no effect
- Resonance state visible in fight telemetry

**Seam:** gamora (Resonance sequence state machine in fight_engine) + rocket (Resonance Partner designation in generation)

---

## 4. Companion convergence item design

The companion's 4th gear slot is a **convergence item** — the runeword-analog. Zero power on its own. Activates a named convergence effect when companion T4 strategy and player T4 strategy form a compatible pair.

### 4.1 Compatibility matrix principle

Compatible pairs are thematically coherent — the companion's T4 amplifies or extends the player's T4 strategy. Incompatible pairs receive a generic fallback buff (flat 15% player stat increase; no narrative coherence required).

### 4.2 Example valid convergence pairs (Session 1: define full matrix)

| Player T4 | Companion T4 | Convergence effect |
|---|---|---|
| ELEMENT_CONVERSION_MONO | NETWORK_AMPLIFIER | Player's element hits propagate Network tag automatically (no CC required); tag duration = 4s |
| DEFENSIVE_TRADEOFF | PROXY_SOVEREIGNTY | Companion's sovereign proxy inherits chaos immunity (shadow + holy resistant) from player |
| MOMENTUM_CASCADE | GEOMETRY_COLLAPSE | Cascade hits trigger Geometry Collapse on all targets (AoE collapse bonus on each Cascade instance) |
| GEOMETRY_INVERSION | ELEMENTAL_ECHO | Echo fires with inverted geometry (Echo from AoE kit is single-target focused; from single-target kit is AoE) |
| RESONANCE_LOOP | DUAL_PROXY | Both player proxies enter Resonance state with the player's skill Resonance — proxies deal 2.5× on the Shatter tick |

**Session 1 action:** Define the full compatibility matrix for all 21 × 21 player+companion strategy pairs (select valid pairs; define named convergence effect per valid pair; define fallback for invalid pairs).

### 4.3 Balance parameters

- Maximum convergence effect magnitude: equivalent to +40% player fight performance (WR delta ≤ 0.10 above non-convergence baseline)
- Fallback effect: flat +15% player stat (no compatibility required); ensures convergence item is never a dead slot
- Convergence item is companion-exclusive (player cannot equip it)

---

## 5. DEFENSIVE_TRADEOFF mana shield mechanics (Session 1 action)

DEFENSIVE_TRADEOFF was reinstated 2026-06-12 with mana shield behavior DEFERRED to this session. Session 1 must lock:

1. **Absorption ratio:** what percentage of incoming damage does mana absorb before HP? (Candidate: 100% absorption while mana > 0; transitions to full HP exposure at mana = 0)
2. **Damage type coverage:** which damage types does mana shield absorb? (Candidates: all types; elemental only; shadow + holy excluded since already immune under t4_chaos_immune)
3. **Depletion behavior:** when mana reaches 0, does damage spill to HP (spill = damage that would have been absorbed by mana overflows to HP) or does the player take full raw HP damage at that point?
4. **Passive vs active vs always-on:** always-on per current implementation intent; confirm or revise

---

## 6. 5-property scoring as generation directive

Per the hypothesis doc, P1-P5 scores (0 / 0.5 / 1) determine whether a mechanic is BUILD_DEFINING_CANONICAL / SUB_AXIS / ABSENT in a given kit cell. This is both a measurement framework AND a generation directive.

**Generation directive (rocket seam):**
- Each skill in the kit is assigned a P1-P5 score at generation time
- At least 1 skill per kit must score BUILD_DEFINING_CANONICAL (P-score = 1) on P1 (Identity-axis transformation)
- T4 strategy capstone skill automatically scores BUILD_DEFINING_CANONICAL on P1
- Non-capstone skills may score BUILD_DEFINING_CANONICAL on other P-axes (P2 multiplicative composition, P3 system-substitution, P4 creation-moment memorability, P5 composition unlock)

**Pass/fail criteria (rocket):**
- Every generated kit has ≥1 BUILD_DEFINING_CANONICAL skill
- T4 capstone skill P1-score = 1 (BUILD_DEFINING_CANONICAL)
- P-score distribution per kit measurable in telemetry

**Session 1 action:** Confirm P1-P5 score assignment rules per T4 strategy. Define which score axis each new T4 strategy primarily satisfies.

---

## 7. Support-eligible T4 subset (companion/monster seasons)

NPC/Mercenary season and Monster season kits draw from a SUPPORT-ELIGIBLE subset of T4 strategies. These strategies produce kits whose combat contribution is support/CC-primary, not damage-primary.

**Support-eligible strategies (companion season):**
- NETWORK_AMPLIFIER — CC amplification; augments player output
- DEFENSIVE_TRADEOFF — defensive layering; reduces companion damage intake
- RESONANCE_LOOP — rotation-support; enables player Resonance state
- PROXY_SOVEREIGNTY — companion proxy fights independently; companion focuses on survival
- COMPANION_CONTRACT (nested — companion can have its own sub-companion via this strategy; rare)

**CC-eligible strategies (monster season):**
- NETWORK_AMPLIFIER — CC propagation from monster
- GEOMETRY_COLLAPSE — focus-fires the player's target
- MOMENTUM_CASCADE — amplifies monster's own multi-target CC output

**Excluded from companion/monster seasons:** SACRIFICE_ASCENDANCY (HP-spend risk), TEMPORAL_CHARGE (requires player-level precision), ELEMENT_CONVERSION variants (damage-primary). Monster season additionally excludes COMPANION_CONTRACT and MONSTER_PACT (no nested pacting).

---

## 8. Session 1 open questions (must resolve)

| # | Question | Priority |
|---|---|---|
| 1 | GEOMETRY_COLLAPSE and RESOURCE_CONVERSION: derive locked mechanics from mechanism infrastructure + Phase 4 empirical data | HIGH — current strategies need locking, not just "empirical" |
| 2 | PROXY_CONVERGENCE valid pair matrix: which of the 14×14 proxy type pairs produce valid convergence? What is each named behavior? | HIGH — needed before Session 2 proxy spec |
| 3 | DUAL_PROXY compatibility pools: per-type secondary proxy pools for all 14 primary types | HIGH — needed before Session 2 |
| 4 | Companion convergence item full compatibility matrix: 21×21 strategy pairs → select valid pairs + name each convergence effect | MEDIUM — Session 2 gated |
| 5 | DEFENSIVE_TRADEOFF mana shield behavior: absorption ratio, coverage, depletion, activation model | HIGH — blocks gamora implementation |
| 6 | Chain count → kit generation rules: how many chains does a kit have? Is chain count a generation parameter or derived from skill count? | HIGH — affects T4 node count per kit |
| 7 | DIRECT_DAMAGE_AMPLIFICATION retirement migration: kits currently relying on DDA for in-band guarantee — do they get re-evaluated or are they grandfathered? | MEDIUM — Season 001010 corpus decision |

---

**Author:** gandalf, 2026-06-12. Matt-authorized Session 1 spec. Open questions in § 8 resolve in Session 1.
