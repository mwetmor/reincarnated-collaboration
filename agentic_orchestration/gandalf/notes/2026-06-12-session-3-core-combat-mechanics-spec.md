# Session 3 — Core Combat Mechanics Spec

**STATUS:** DRAFT — Matt-authorized 2026-06-12 (Pattern B session, architecture cascade); partially independent of Session 1; can overlap with Session 2 gamora kernel extension work
**Author:** gandalf
**Date:** 2026-06-12
**Grounding docs:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` — PRIMARY (§ 4.13, 4.14, 4.15, 4.16)
- `agentic_orchestration/gandalf/notes/2026-06-12-session-1-t4-architecture-spec.md` — T4 catalog (prerequisite for Layer 2 assignments)
- `agentic_orchestration/dispatches/2026-06-12-gamora-proxy-kernel-handoff.md` — charge-stack kernel item (Item 4)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — BC axis definitions (Axes 2, 2B, 3A, 3B, 5)

**Produces:**
1. Layer 2 generation directive spec (rocket seam implementation contract)
2. Charge-stack mechanic spec from rocket's perspective (gamora kernel item already in handoff)
3. terrain_reactive + beam geometry implementation contracts (gamora + rocket)
4. Control density measurement methodology (Axis 2B formalization)
5. Cognitive load metric definition (enables RESONANCE_LOOP and TEMPORAL_CHARGE eligibility gates)

---

## 0. Design mandate

Formalize the four Layer 2 mechanism-structural dimensions as generation directives rocket can implement at skill construction time. Fill the charge-stack Axis 5 bin from the rocket side. Specify the two unbuilt geometry types (terrain_reactive, beam). Lock measurement methodologies for control density and cognitive load.

These are the substrate-level mechanics that create per-skill combinatorial variation — the PoE skill gem analog. They must be locked before hypothesis tests for Axes 2, 2B, 3A, 3B, and 5 can run.

---

## 1. Layer 2 mechanism-structural dimensions (generation directive)

Each skill in a generated kit is assigned four Layer 2 properties at generation time. These compose with the skill's element, geometry, and damage values to produce the full skill signature. The four dimensions are: **magnitude_pattern × stackability × trigger × scaling_pattern**.

### 1.1 magnitude_pattern — how skill damage is delivered

| Value | Behavior | Typical use |
|---|---|---|
| `flat` | Fixed damage value; does not change per application | Simple damage skills; CC skills |
| `scaling` | Scales smoothly with player level or gear tier | Standard scaling skills |
| `burst_spike` | Front-loaded: full damage on first application; near-zero on subsequent | Opener skills; burst openers |
| `decay` | Starts high; each application within the same fight reduces magnitude by 15% | Diminishing-returns weapons; pressuring openers |
| `escalating` | Starts low; each application within the same fight increases magnitude by 20% (cap: 3× base) | TEMPORAL_CHARGE; ramping DoTs |
| `threshold_burst` | Flat until a threshold condition is met (stack count, HP%, timer); then fires a magnitude spike and resets | MOMENTUM_CASCADE; CHARGED_THRESHOLD_PROXY T4 |

### 1.2 stackability — how the mechanic interacts with repeated application

| Value | Behavior | Notes |
|---|---|---|
| `non_stacking` | Effect applies once; re-application refreshes duration only; magnitude does not increase | Standard CC; simple debuffs |
| `stacking_capped_N` | Stacks up to N; applications beyond cap do nothing (wasted) | DoT stacks; MOMENTUM_CASCADE stacks; N defined per skill |
| `stacking_refreshing_N` | Stacks up to N; additional applications reset the duration of ALL existing stacks | Persistent DoTs; ELEMENTAL_ECHO analog |
| `stacking_decaying` | Stacks decay by 1 per tick automatically; applications add stacks | NETWORK_AMPLIFIER tag duration tracking |
| `stacking_unlimited` | No cap; stacks accumulate indefinitely (restricted to gamora-controlled mechanics only; not a rocket generation value) | Reserved; not a generation directive |

### 1.3 trigger — what activates the mechanic

| Value | Behavior | Notes |
|---|---|---|
| `on_use` | Fires when the skill is activated by the player | Instant effects; buffs; cooldown-based openers |
| `on_hit` | Fires when the skill's projectile or effect lands on an enemy | Delayed skills; projectiles; AoE that requires travel |
| `on_kill` | Fires when any enemy dies while this skill's effect is active | Kill-confirmation mechanics; passive bonuses |
| `on_take_damage` | Fires when the player receives a hit above a threshold | Reactive mechanics; SACRIFICE_ASCENDANCY trigger |
| `periodic` | Fires on a fixed timer interval (configurable tick_interval_s) | Volatile Emitter; DoT ticks; passive auras |
| `threshold_stack` | Fires when stack count (accumulation state) reaches the configured threshold | CHARGED_THRESHOLD_PROXY; charge-stack spend trigger |
| `threshold_hp` | Fires when player OR enemy HP crosses a configured fraction | Execute mechanics; panic buttons |
| `sequence` | Fires when a specified skill sequence has been completed | RESONANCE_LOOP Resonance activation; combo finishers |

### 1.4 scaling_pattern — what the mechanic scales with as the kit grows

| Value | Behavior | Notes |
|---|---|---|
| `player_level` | Scales linearly with player level (standard progression) | Default for most skills |
| `gear_tier` | Additive bonus per gear tier; gear-dependent power curve | Gear-scaling skills; investment profile |
| `resource_current` | Magnitude proportional to current resource amount at time of use | Rage peak-use skills; mana surge mechanics |
| `stack_count` | Magnitude proportional to current stack count | MOMENTUM_CASCADE; charge-stack threshold skills |
| `enemy_hp_remaining` | Magnitude inversely proportional to remaining enemy HP (execute-style) | Execute finishers; low-HP burst |
| `elapsed_time` | Magnitude increases with time elapsed in fight (ramp-up curve; caps at 60s) | Sustained DoT ramp; RESONANCE_LOOP extended value |

### 1.5 Assignment rules (rocket seam implementation contract)

The four dimensions are assigned at skill generation time. Rules by skill type:

**CC skills:**
- `trigger ∈ {on_hit, on_use}` (CC cannot be periodic or sequence-gated by default)
- `stackability ∈ {non_stacking, stacking_capped_N}` (N ≤ 3; CC should not stack infinitely)
- `magnitude_pattern ∈ {flat, scaling}` (CC magnitude is consistent; no decay or escalation)
- `scaling_pattern ∈ {player_level, gear_tier}` (CC duration scales with progression; not with resource)

**DoT skills:**
- `trigger = on_hit` (DoT applies on landing)
- `stackability ∈ {stacking_capped_N, stacking_refreshing_N}` (N ≤ 5; DoT should stack)
- `magnitude_pattern ∈ {flat, scaling, escalating}` (escalating for ramp DoTs)
- `scaling_pattern ∈ {player_level, gear_tier, stack_count}` (stack-count scaling for ramp-up DoTs)

**Burst skills (damage geometry = AoE_burst):**
- `trigger ∈ {on_use, on_hit}` (AoE can be instant or after travel)
- `stackability = non_stacking` (AoE bursts don't stack with themselves)
- `magnitude_pattern ∈ {flat, burst_spike, threshold_burst}` (burst-oriented patterns)
- `scaling_pattern ∈ {player_level, gear_tier, resource_current}` (resource-current for rage/focus synergy)

**T4 capstone skills (assigned to match T4 strategy mechanics):**

| T4 strategy | Capstone skill Layer 2 assignments |
|---|---|
| MOMENTUM_CASCADE | `trigger=on_hit`, `stackability=stacking_capped_10`, `magnitude_pattern=threshold_burst` (Cascade fires at 10 stacks) |
| ELEMENTAL_ECHO | `trigger=on_use`, `stackability=non_stacking` (Echo replaces on each use), `magnitude_pattern=flat`, `scaling_pattern=player_level` |
| SACRIFICE_ASCENDANCY | `trigger=on_take_damage` (or manual `on_use` for activation variant), `stackability=non_stacking`, `magnitude_pattern=burst_spike` |
| TEMPORAL_CHARGE | `trigger=on_use` (held), `stackability=stacking_capped_5`, `magnitude_pattern=escalating`, `scaling_pattern=stack_count` |
| NETWORK_AMPLIFIER | `trigger=on_hit` (CC application), `stackability=stacking_decaying`, `magnitude_pattern=flat` |
| RESONANCE_LOOP | `trigger=sequence`, `stackability=non_stacking`, `magnitude_pattern=threshold_burst` (2.5× on Shatter) |
| GEOMETRY_INVERSION | `trigger=on_use`, `stackability=non_stacking`, `magnitude_pattern=burst_spike` |
| PROXY_FISSION | `trigger` is a death event (gamora-handled; not a player skill trigger) | |

**Charge-stack energy_type kit skills (rocket directive — complements gamora kernel handoff § 4):**
- All skills: `trigger ∈ {on_hit, on_use}` for accumulation-contributing skills; `trigger=threshold_stack` for the threshold burst skill
- Accumulation skills: `scaling_pattern=player_level` (accumulate freely; charge count is the scaling vector, not these skills)
- Threshold burst skill: `magnitude_pattern=threshold_burst`, `stackability=non_stacking`, `scaling_pattern=stack_count`
- Rule: every charge-stack kit must contain exactly 1 threshold burst skill per chain

---

## 2. Charge-stack mechanic spec (rocket generation side)

This complements the gamora kernel handoff (§ 4) which defines the `_ENERGY_CONFIGS` entry. This section defines how rocket generates kits with charge-stack energy_type.

### 2.1 Kit structure rules for charge-stack energy_type

- **Threshold skill requirement:** every chain in a charge-stack kit MUST include exactly 1 skill with `trigger=threshold_stack` (the spend skill). Chains without a threshold skill fail generation validation.
- **Accumulation skills:** all other skills in the chain are accumulation-neutral (they are used normally; the fight_engine accumulates +1 charge per enemy hit regardless of which skill is used)
- **Threshold value per skill:** the threshold burst skill fires at configurable stack count: range 5-10 (rocket assigns at generation; higher threshold = higher burst magnitude)
- **Stack spend model:** threshold burst skill spends ALL stacks on firing (spend-all model per gamora handoff § 4)

### 2.2 T4 strategy compatibility with charge-stack

| T4 strategy | Charge-stack compatible? | Notes |
|---|---|---|
| TEMPORAL_CHARGE | YES — PRIMARY eligibility | charge-stack + TEMPORAL_CHARGE is the core charge-stack experience |
| RESOURCE_CONVERSION | YES | charge-stack overflow converts to damage (stacks at cap → damage burst) |
| MOMENTUM_CASCADE | COMPATIBLE | Momentum stacks are separate from charge stacks; both can coexist |
| DEFENSIVE_TRADEOFF | NO | DEFENSIVE_TRADEOFF requires `energy_type == mana` (see vestigial-ontology register) |
| All others | COMPATIBLE | No eligibility conflict with charge-stack unless explicitly noted |

### 2.3 Axis 5 bin assignment

| energy_type | Axis 5 bin |
|---|---|
| mana | Mana |
| rage | Rage |
| combo | Combo |
| focus | Focus |
| stamina-as-resource | Stamina |
| **charge-stack** | **Charge-Stack (new bin — fills missing Axis 5 slot)** |

QD grid update: Axis 5 now has 6 bins (was 5). The QD grid dimensions expand from 8 axes to accommodate. Total QD cell count delta: existing cells × (6/5) = 68,040 × 1.2 = 81,648 cells at full expansion. This is the generation-side implication of the new energy_type; confirm with gamora + rocket that cell count expansion does not break QD iteration.

---

## 3. Damage geometry types: terrain_reactive + beam

### 3.1 Current geometry type catalog

| Geometry type | Status | Current sim support |
|---|---|---|
| single_target | BUILT | Yes |
| AoE_burst | BUILT | Yes |
| DoT_stack | BUILT | Yes |
| terrain_reactive | NOT BUILT | Pending gamora assessment (kernel handoff § 5) |
| beam | NOT BUILT | Session 3 spec |

### 3.2 terrain_reactive geometry — implementation contract

**Design intent:** Skills with terrain_reactive geometry deal bonus damage or bonus CC on terrain that matches their element or geometry type. In spatial fights, terrain zones already exist (post-Phase-3 spatial repoint). In standard non-spatial fights, terrain_reactive skills receive a configurable terrain bonus parameter.

**Standard fight implementation (gamora seam):**
```python
# simulate_fight signature extension for terrain support (Session 3 kernel item):
def simulate_fight(
    player: Combatant,
    enemy: Combatant,
    player_proxies: list[ProxyCombatant] | None = None,
    terrain_type: str | None = None,  # NEW: "standard" | "fire_terrain" | "ice_terrain" | "water_terrain" | "elevated" | None
) → FightResult:
```

`terrain_type=None` = standard fight (no terrain bonus; backward compatible with existing signature).

**terrain_reactive skill bonus table:**

| Skill element | terrain_type match | Bonus |
|---|---|---|
| fire | `fire_terrain` | +25% damage; ignites terrain (extends DoT by 50%) |
| water / ice | `water_terrain` | +20% damage; freeze probability +15% |
| earth | `elevated` | +20% AoE radius; +10% damage |
| lightning | `water_terrain` | +40% damage (conductor); chain-hit to 1 additional enemy |
| shadow | Any dark terrain (pending gamora assessment for definition) | +15% damage; +CC duration 20% |
| holy | `elevated` | +15% damage; +healing 10% |

**Non-terrain_reactive skills:** receive no bonus regardless of terrain_type; terrain parameter has zero effect on non-terrain_reactive skills.

**Gamora assessment gate:** gamora's terrain-reactive geometry assessment (kernel handoff § 5) determines if `terrain_type` can be a caller-side parameter (preferred) or requires fight_engine branching. If caller-side: above extension applies. If kernel-side: Session 3 authors a kernel-change-protocol item for gamora.

**Rocket generation directive:** skills with geometry = terrain_reactive must have a paired `preferred_terrain` field that matches the element-to-terrain table above. Rocket assigns preferred_terrain at skill generation based on element.

### 3.3 beam geometry — implementation contract

**Design intent:** A beam is a continuous line of effect from the player's position (or skill origin point) toward the primary target. All enemies in the beam path take proportional damage. Beam has a duration (it persists for N seconds, not a single hit).

**Beam properties:**
- `beam_width_m: float` — beam width (default 0.5m; wider beams hit more enemies in the path)
- `beam_duration_s: float` — how long the beam persists (default 2.0s; skill cooldown begins after beam ends)
- `beam_base_damage_pct: float` — fraction of skill damage delivered per tick to each enemy in path
- `beam_tick_interval_s: float` — how often each enemy in beam takes a damage tick (default 0.25s)
- `beam_primary_target_bonus: float` — extra damage multiplier on the primary (aimed-at) target vs path bystanders (default 1.5× — primary target takes 50% more per tick)

**Standard fight (non-spatial) modeling:** beam is modeled as AoE_burst with:
- Primary target: full beam damage per tick × beam_primary_target_bonus
- Secondary targets: up to 2 additional enemies take 60% of primary's per-tick damage
- Total fight contribution: sum across all ticks × beam_duration_s / beam_tick_interval_s ticks

**Spatial fight:** actual line geometry. Enemies within beam_width_m of the line between player and primary target take per-tick damage. The spatial engine handles the geometry; fight_engine receives the beam as a multi-hit event.

**Beam Layer 2 assignments (rocket directive):**
- `trigger = periodic` (beam ticks on interval)
- `stackability = non_stacking` (beam doesn't stack with itself)
- `magnitude_pattern ∈ {flat, scaling}` (per-tick damage is consistent)
- `scaling_pattern ∈ {player_level, gear_tier, elapsed_time}` (elapsed_time for ramping beams)

**Pass/fail criteria (gamora):**
- Beam deals damage to primary target on correct tick interval (±0.05s)
- Secondary targets (up to 2) receive 60% ± 2% of primary's per-tick damage in standard fight
- Beam duration is tracked; final tick fires at or before beam_duration_s
- Beam does not interrupt other player skill uses (beam continues in background while player uses other skills)
- No recursive beam generation (beam hits do not trigger additional beams)

---

## 4. Control density (Axis 2B) — measurement methodology

### 4.1 What counts as a CC skill

A skill is a CC skill if it satisfies ALL of:
1. Has a `cc_effect` field with a non-null value in Layer 2 dimensions (effect type: stun, root, slow, freeze, fear, silence, or knockback)
2. The CC applies to the enemy (not self-buff or player-movement skills)
3. The CC effect duration > 0.5s (instantaneous micro-stuns below 0.5s are NOT counted as CC skills for density purposes; they are damage modifiers)

### 4.2 Control density ratio formula

```
control_density_ratio = cc_skill_count / total_skill_count
```

where `total_skill_count` = all skills in the kit (across all chains).

### 4.3 Axis 2B bin assignment

| control_density_ratio | Axis 2B bin |
|---|---|
| ≥ 0.50 | HIGH |
| 0.25 ≤ ratio < 0.50 | MEDIUM |
| < 0.25 | LOW |

### 4.4 Measurement implementation (rocket seam)

Rocket measures control_density_ratio at kit finalization (after all skills are assigned). The measurement is:
1. Count skills with non-null `cc_effect` AND `cc_effect.duration_s > 0.5`
2. Divide by total skill count in kit
3. Assign Axis 2B bin per table above
4. Store `control_density_ratio` and `axis_2b_bin` in kit record

QD engine uses `axis_2b_bin` as the BC cell coordinate for Axis 2B.

### 4.5 CC effect types (closed enum for rocket + gamora)

Valid `cc_effect` values:
- `stun` — target cannot act for duration
- `root` — target cannot move for duration; can still act
- `slow` — target movement reduced by configurable % for duration
- `freeze` — target cannot move OR act for duration; fragile (bonus damage); shorter than stun
- `fear` — target flees (away from player) for duration; can't act offensively
- `silence` — target cannot use skills for duration; can still move
- `knockback` — target displaced from current position; instantaneous or short-duration
- `pull` — target displaced toward player; instantaneous
- `taunt` — enemy preferentially targets the taunting entity (proxy use primarily; not a player kit CC)

---

## 5. Damage tempo (Axes 3A + 3B) — mechanic formalization

### 5.1 Axis 3A — damage tempo (burst / sustained / mixed)

Tempo is measured from fight telemetry: what fraction of a kit's total damage in a fight lands in the first 3 seconds vs after?

**Burst:** ≥ 50% of fight damage lands in the first 3 seconds. Kit is explosive on entry; diminishes over time.
- Characterizes: burst_spike magnitude_pattern skills; front-loaded openers; threshold burst skills used immediately
- Example kits: TEMPORAL_CHARGE at 5 stacks + first attack; SACRIFICE_ASCENDANCY immediate activation

**Sustained:** ≤ 25% of fight damage lands in the first 3 seconds AND fight DPS variance (std dev / mean) ≤ 0.30. Kit output is relatively flat over fight duration.
- Characterizes: periodic + DoT stacking kits; scaling magnitude_pattern skills; beam geometry
- Example kits: DoT-primary casters; mana economy focus kits with periodic resource use

**Mixed:** everything between burst and sustained — typically 25-50% first-3s damage.
- Most kits land here; mixed is the default bin

**Axis 3A bin assignment:**
| Condition | Axis 3A bin |
|---|---|
| first_3s_damage / total_damage ≥ 0.50 | Burst |
| first_3s_damage / total_damage ≤ 0.25 AND dps_variance ≤ 0.30 | Sustained |
| otherwise | Mixed |

### 5.2 Axis 3B — amplitude variance (high / low)

Amplitude variance measures how spikey the damage output is across the fight.

**Metric:** coefficient of variation of per-tick damage = std_dev(per_tick_damage) / mean(per_tick_damage) across all fight ticks where player dealt damage.

**High variance:** CV > 0.60 — damage has significant spikes (crits, threshold bursts, RESONANCE_LOOP Shatter)
**Low variance:** CV ≤ 0.60 — damage is relatively consistent per-tick

**Axis 3B bin assignment:**
| Condition | Axis 3B bin |
|---|---|
| CV > 0.60 | HIGH amplitude variance |
| CV ≤ 0.60 | LOW amplitude variance |

**Measurement implementation (gamora seam):** gamora adds per-tick damage tracking to FightResult (alongside existing proxy_damage additions). `tick_damage_log: list[float]` with all player-dealt per-tick damage values; CV computed in balance_loop or telemetry post-fight.

---

## 6. Cognitive load metric — execution complexity

### 6.1 Purpose

Cognitive load is a measurement of how demanding the optimal rotation is to execute. It gates:
- RESONANCE_LOOP eligibility: requires `cognitive_load ∈ {medium, high}`
- TEMPORAL_CHARGE eligibility: requires some cognitive_load floor (TEMPORAL_CHARGE is mechanically demanding)
- Hypothesis test: do high-cognitive-load kits perform worse in play vs simulation? (Session 5 hypothesis)

### 6.2 Cognitive load score formula

```
cognitive_load_score = 
    skill_count × 1.0 +
    sequence_depth × 2.0 +
    state_conditions × 1.5 +
    timing_windows × 2.5
```

**Factor definitions:**
| Factor | Definition | How to measure |
|---|---|---|
| `skill_count` | Total distinct skills in the kit | Count at kit finalization |
| `sequence_depth` | Max length of skill sequence required for an optimization (e.g., RESONANCE_LOOP requires 2-skill Partner sequence before 3rd use) | Derived from T4 strategy Layer 2 `trigger=sequence` depth + any chain combo requirements |
| `state_conditions` | Number of distinct active states the player must track simultaneously (e.g., Resonance ON/OFF, Momentum stack count, Ascendancy timer, charge stack count) | Count distinct non-trivial state machines active in the kit |
| `timing_windows` | Number of time-sensitive windows in the rotation (windows where timing matters: RESONANCE 3s window, TEMPORAL_CHARGE hold window, MOMENTUM threshold) | Count distinct timed windows per T4 strategy + per Layer 2 trigger=sequence occurrence |

### 6.3 Cognitive load bins

| cognitive_load_score | Cognitive load bin |
|---|---|
| < 8 | LOW |
| 8 ≤ score < 14 | MEDIUM |
| ≥ 14 | HIGH |

### 6.4 Example calibrations

| Kit description | skill_count | sequence_depth | state_conditions | timing_windows | score | bin |
|---|---|---|---|---|---|---|
| Simple fire AoE, no T4 state machines | 3 | 0 | 0 | 0 | 3.0 | LOW |
| Combo DoT kit, stack tracking | 4 | 0 | 1 (stack count) | 0 | 5.5 | LOW |
| MOMENTUM_CASCADE kit | 5 | 0 | 1 (momentum stacks) | 1 (Cascade reset timing) | 8.0 | MEDIUM |
| RESONANCE_LOOP + hybrid element | 5 | 2 (Partner A → Partner B) | 2 (Resonance state; 12s window) | 2 (3s seq window; 12s Res window) | 17.0 | HIGH |
| TEMPORAL_CHARGE + charge-stack | 5 | 0 | 2 (charge count; threshold state) | 2 (hold timing; threshold window) | 10.5 | MEDIUM |
| RESONANCE_LOOP + MOMENTUM_CASCADE (3-chain kit) | 6 | 2 | 3 | 3 | 19.5 | HIGH |

### 6.5 Rocket generation directive

Rocket computes cognitive_load_score at kit finalization (after T4 strategy assignment, since T4 contributes the majority of state_conditions and timing_windows). The score and bin are stored in the kit record as `cognitive_load_score: float` and `cognitive_load_bin: str`.

QD engine uses `cognitive_load_bin` as a secondary axis if a Cognitive Load hypothesis axis is added to the BC grid in Session 5. For now: stored but not a primary QD cell axis.

---

## 7. Session 3 open questions

| # | Question | Priority |
|---|---|---|
| 1 | Terrain-reactive: gamora boundary assessment needed before session can fully lock (see gamora kernel handoff § 5). Is terrain_type a caller-side parameter to simulate_fight or a kernel branch? | HIGH — gamora assessment gates spec lock |
| 2 | QD grid cell count expansion from Axis 5 adding charge-stack bin (6 bins vs 5): confirm with rocket that 81,648 → does not break iteration or memory bounds | MEDIUM |
| 3 | Axis 3A first-3s-damage measurement: is the 3-second window the right burst threshold? PoE uses "hit-count in first 3 skills used" as an alternative | MEDIUM — design preference |
| 4 | Cognitive load — sequence_depth for chain combos: do chains themselves create sequence requirements, or only T4 strategies? | HIGH — affects most cognitive_load scores |
| 5 | Axis 3B CV threshold 0.60: derived from gut; needs empirical calibration from existing fight telemetry. Has gamora run CV distribution on Season 001010 corpus? | LOW — calibrate from data |

---

**Author:** gandalf, 2026-06-12. Matt-authorized Session 3 spec from Pattern B session. Partially independent of Session 1; can begin after Session 2 gamora kernel handoff fires.
