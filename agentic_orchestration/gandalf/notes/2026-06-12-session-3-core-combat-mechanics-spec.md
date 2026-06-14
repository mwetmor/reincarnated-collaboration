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

> **NORMALIZATION PASS (gandalf, 2026-06-12, Matt-authorized):** axis vocabulary re-pointed to the locked definitions in `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3; geometry vocabulary re-pointed to the engine's actual three layers (rich 24-type `VALID_GEOMETRY_TYPES` in `generation/geometry_derivation.py` → spatial 6-type enum → Axis 2 BC bins); kernel premises corrected against code. Key corrections in this doc: Axis 5 ALREADY has 7 locked bins including charge-stack (68,040 cells already counts it — the original "6 bins, 81,648 cells" math was wrong); Axis 2B locked bins are damage-pure/mixed/control-pure at 20%/60% effect-budget-weighted (not HIGH/MED/LOW at 50%/25% count-ratio); Axis 3A is locked as damage events-per-second low/medium/high (the first-3-seconds metric here is a NEW proposed "front-load profile" metric, not Axis 3A); Axis 3B is locked as flat/variable/spiky at per-event CV 0.3/0.7 (not HIGH/LOW at 0.60); `beam_channel` EXISTS in engine generation vocabulary (the new work is sim-side beam mechanics, not the geometry type). Delta summary: `gandalf/notes/2026-06-12-normalization-pass-delta-summary.md`.

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

**Burst AOE skills (engine spatial geometry ∈ {circle, cone, line}; predicted Axis 2 ∈ {small-AOE, large-AOE}):**
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
| **GEOMETRY_PROPAGATION (cascade)** ● | `trigger=on_kill` (corpse-burst; gamora kill-event hook; recursion cap 3 is kernel-enforced, not Layer 2), `stackability=non_stacking`, `magnitude_pattern=flat`, `scaling_pattern=player_level` |
| **GEOMETRY_PROPAGATION (overkill)** ● | `trigger=on_hit`, `stackability=non_stacking`, `magnitude_pattern=scaling`, `scaling_pattern=player_level` |
| **RETRIBUTION_ENGINE** ● | `trigger=on_take_damage` (vengeance pool, not stacks; shares SACRIFICE_ASCENDANCY hook), `stackability=non_stacking`, `magnitude_pattern=flat`, `scaling_pattern=gear_tier` |
| **PERSISTENCE_ENGINE** (`_uptime` / `_saturation`) ● | `trigger=periodic`, `stackability=non_stacking`, `magnitude_pattern=escalating`, `scaling_pattern=elapsed_time` |
| **PHASE_MOMENTUM** ● | `trigger=threshold_stack` (Phase stacks; unhit-window accumulation is gamora-handled), `stackability=stacking_capped_5`, `magnitude_pattern=threshold_burst`, `scaling_pattern=player_level` |

● = Session-1 ratified additions (2026-06-12); authoritative spec blocks at `gandalf/notes/2026-06-12-session-1-rulings-q1-q10-t4-catalog-expansion.md` § 2 / § 2.5.

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

### 2.3 Axis 5 bin relationship (corrected at normalization pass)

**The original draft's energy_type → Axis 5 bin identity table was wrong on two counts and has been removed:**

1. **Energy types are NOT Axis 5 bins.** The locked Axis 5 bins (lock doc § 3) are MEASURED resource-usage patterns: **HP-economy / damage-taken-converts / charge-stack / starved / overflow / generator-spender / steady** — 7 bins. Mana/rage/combo/focus are declared `energy_type` values (generation-time structural properties). A mana kit can MEASURE as starved, steady, or generator-spender depending on its rotation economics.
2. **No grid expansion occurs.** The locked 68,040-cell count (6×5×3×3×3×3×4×7) ALREADY includes the 7-bin Axis 5 with charge-stack. Adding the charge-stack `energy_type` populates an existing bin; it does not add one. The original "6 bins (was 5) → 81,648 cells" arithmetic is retracted.

**Q9 — hold-vs-spend: RESOLVED (Matt-ratified 2026-06-12, ruling record § 1 Q9).** The locked charge-stack bin detects build-then-HOLD behavior (mean normalized resource ≥0.75, variance <0.20); a pure spend-all sawtooth never measures into it. **Ruling: keep spend-all AND add a passive per-stack bonus while held.** Rocket varies passive-vs-burst magnitudes per kit so the optimal-rotation solver yields hold-optimal kits (which measure into charge-stack) and spend-optimal kits (which measure into generator-spender). Zero lock amendment; the PoE Discharge hold-vs-spend tension becomes a generation parameter. **Effect: gamora dispatch Item 4 and rocket dispatch Item 10 are UN-HELD.**

---

## 3. Damage geometry types: terrain_reactive + beam

### 3.1 Geometry vocabulary — three layers (corrected at normalization pass)

The original draft's 5-row geometry catalog ("single_target / AoE_burst / DoT_stack / terrain_reactive / beam") matched no engine layer and has been replaced. The engine has **three geometry layers**:

| Layer | Vocabulary | Where |
|---|---|---|
| Rich skill geometry (24 types) | `projectile_single`, `melee_single`, `nova`, `cone_spray`, **`beam_channel`**, `chain_lightning`, `totem`, … | `generation/geometry_derivation.py` `VALID_GEOMETRY_TYPES` |
| Spatial enum (6 types) | circle / cone / line / point / mixed / none | `_RICH_TO_SPATIAL` mapping (`beam_channel` → `line`) |
| Axis 2 BC bins (5, locked) | single-target / small-AOE / large-AOE / chain / multi-spawn | BC pipeline, damage-weighted argmax |

DoT-stacking is a Layer 2 `stackability` property (§ 1.2), not a geometry, at any layer.

**Build status (code-verified):**

| Item | Status |
|---|---|
| `beam_channel` rich geometry type | **EXISTS** in generation vocabulary; maps to spatial `line`. The NEW work is sim-side continuous-beam mechanics (§ 3.3): per-tick damage, duration, path bystanders — the fight engine currently treats it as a discrete-hit line skill |
| `terrain_reactive` | **GREENFIELD** — not a geometry type at any layer; no terrain-damage interaction exists anywhere in the sim. The only terrain-adjacent mechanic is `ChokeZone` movement clamping in `spatial_gauntlet/arena.py` (movement only; zero damage/element interaction). Pending gamora assessment (kernel handoff § 5) |

### 3.2 terrain_reactive geometry — implementation contract

**Design intent:** Skills tagged terrain-reactive deal bonus damage or bonus CC on terrain that matches their element. **Greenfield premise (code-verified at normalization pass):** NO terrain-damage interaction exists in the sim at any layer — the only terrain-adjacent mechanic is `ChokeZone` movement clamping in `spatial_gauntlet/arena.py` (movement-only). The original draft's claim that "terrain zones already exist" overstated this; everything below is new behavior.

**Standard fight implementation (gamora seam):**
```python
# simulate_fight kwarg extension for terrain support (Session 3 kernel item);
# matches the kernel's actual symmetric signature (combatant_a, combatant_b, *, ...):
def simulate_fight(
    combatant_a: Combatant,
    combatant_b: Combatant,
    *,
    proxies_a: list[ProxyCombatant] | None = None,
    proxies_b: list[ProxyCombatant] | None = None,
    terrain_type: str | None = None,  # NEW: "fire_terrain" | "ice_terrain" | "water_terrain" | "elevated" | None
    # ... existing kwargs unchanged
) → FightResult:
```

`terrain_type=None` = standard fight (no terrain bonus; backward compatible with existing behavior).

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

**Rocket generation directive:** terrain-reactivity is a skill TAG (`terrain_reactive: bool` + paired `preferred_terrain` field matching the element-to-terrain table above), NOT a new geometry type — the skill keeps its rich geometry (nova, cone_spray, beam_channel, …) and gains terrain bonus behavior. Rocket assigns preferred_terrain at skill generation based on element.

### 3.3 beam mechanics — implementation contract

**Existing substrate (code-verified):** `beam_channel` is ALREADY a rich geometry type in `generation/geometry_derivation.py` (maps to spatial `line`). What does NOT exist — and what this contract specifies — is continuous-beam SIM MECHANICS: duration, per-tick damage, and path-bystander hits. Today the fight engine resolves a beam_channel skill as a discrete hit.

**Design intent:** A beam is a continuous line of effect from the player's position (or skill origin point) toward the primary target. All enemies in the beam path take proportional damage. Beam has a duration (it persists for N seconds, not a single hit).

**Beam properties:**
- `beam_width_m: float` — beam width (default 0.5m; wider beams hit more enemies in the path)
- `beam_duration_s: float` — how long the beam persists (default 2.0s; skill cooldown begins after beam ends)
- `beam_base_damage_pct: float` — fraction of skill damage delivered per tick to each enemy in path
- `beam_tick_interval_s: float` — how often each enemy in beam takes a damage tick (default 0.25s)
- `beam_primary_target_bonus: float` — extra damage multiplier on the primary (aimed-at) target vs path bystanders (default 1.5× — primary target takes 50% more per tick)

**Standard fight (non-spatial) modeling:** beam is modeled as a multi-target line hit with:
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
1. Has a `cc_effect` field with a non-null value in Layer 2 dimensions (effect type from the closed enum, § 4.5 — aligned with the locked Axis 2B inclusion list)
2. The CC applies to the enemy (not self-buff or player-movement skills)
3. The CC effect duration > 0.5s (instantaneous micro-stuns below 0.5s are NOT counted as CC skills for density purposes; they are damage modifiers)

### 4.2 Axis 2B — locked measurement methodology (re-pointed at normalization pass)

The Axis 2B bin assignment is **already locked** (lock doc § 3) and is NOT re-derived here:

| Control share (effect-budget weighted) | Axis 2B bin (locked) |
|---|---|
| < 20% | damage-pure |
| 20% – 60% | mixed |
| ≥ 60% | control-pure |

"Control share" is **effect-budget weighted** — the fraction of the kit's effect budget allocated to control rather than damage, measured downstream by the BC pipeline from fight behavior. The original draft's HIGH/MEDIUM/LOW bins at 50%/25% with a count-ratio formula conflicted with the lock and are retired.

### 4.3 Generation-time predictor (rocket seam)

The count-ratio formula survives in a different role — as the cheap **generation-time PREDICTOR** of the measured bin:

```
predicted_control_share = cc_skill_count / total_skill_count
```

where `total_skill_count` = all skills in the kit (across all chains). Rocket computes this at kit finalization:
1. Count skills with non-null `cc_effect` AND `cc_effect.duration_s > 0.5`
2. Divide by total skill count in kit
3. Map through the LOCKED thresholds (20% / 60%) to a `predicted_axis2b_bin` ∈ {damage-pure, mixed, control-pure}
4. Store `predicted_control_share` and `predicted_axis2b_bin` in kit record

The MEASURED Axis 2B bin (effect-budget weighted, from the BC pipeline) is the QD cell coordinate. The predictor serves eligibility gates (e.g., NETWORK_AMPLIFIER) and skew priors only. Predictor-vs-measured divergence is itself telemetry worth tracking (calibrates how well count-ratio approximates effect-budget weighting).

### 4.5 CC effect types (closed enum for rocket + gamora — aligned to locked Axis 2B inclusion list)

Valid `cc_effect` values counting toward Axis 2B control share (per lock doc inclusion list):
- `stun` — target cannot act for duration
- `root` — target cannot move for duration; can still act
- `slow` — target movement reduced by configurable % for duration
- `freeze` — target cannot move OR act for duration; fragile (bonus damage); shorter than stun
- `fear` — target flees (away from player) for duration; can't act offensively
- `silence` — target cannot use skills for duration; can still move
- `blind` — target's attacks miss / accuracy heavily reduced for duration *(in locked inclusion list; was missing from original draft)*
- `chill` — movement + action speed reduction; counts as CC only at ≥30% slow magnitude *(locked threshold)*
- `mind_control` / `charm` — target temporarily fights for the player *(in locked inclusion list; rare/T4-adjacent)*

Displacement + aggro effects — valid `cc_effect` values that do NOT count toward Axis 2B control share (not in the locked inclusion list; flag for Session 1 dialogue if Matt wants them counted):
- `knockback` — target displaced from current position; instantaneous or short-duration
- `pull` — target displaced toward player; instantaneous
- `taunt` — enemy preferentially targets the taunting entity (proxy use primarily; not a player kit CC)

---

## 5. Damage tempo (Axes 3A + 3B) — mechanic formalization

### 5.1 Axis 3A — damage tempo (LOCKED) + front-load profile (NEW proposed metric)

**Axis 3A is already locked** (lock doc § 3) as **damage events per second**, measured from fight telemetry:

| Damage events/second | Axis 3A bin (locked) |
|---|---|
| < 2 | low |
| 2 – 6 | medium |
| ≥ 6 | high |

The original draft's burst/sustained/mixed bins built on first-3-seconds damage share are NOT Axis 3A and the lock is not amended. The first-3s metric is retained as a **NEW proposed metric — `front_load_profile`** — because it captures something Axis 3A genuinely does not (WHEN damage lands, vs how often):

**front_load_profile (proposed; stored in telemetry, not a QD cell axis unless Session 5 promotes it):**

| Condition | front_load_profile |
|---|---|
| first_3s_damage / total_damage ≥ 0.50 | front-loaded |
| first_3s_damage / total_damage ≤ 0.25 AND dps CV ≤ 0.30 | even |
| otherwise | mixed |

- Front-loaded characterizes: burst_spike magnitude_pattern skills; TEMPORAL_CHARGE at 5 stacks + first attack; SACRIFICE_ASCENDANCY immediate activation
- Even characterizes: periodic + DoT stacking kits; scaling magnitude_pattern; beam mechanics

### 5.2 Axis 3B — amplitude variance (LOCKED: flat / variable / spiky)

**Axis 3B is already locked** (lock doc § 3) as coefficient of variation of **per-EVENT damage magnitudes** (std_dev / mean across all player damage events in the fight — per-event, not per-tick):

| Per-event damage CV | Axis 3B bin (locked) |
|---|---|
| < 0.3 | flat |
| 0.3 – 0.7 | variable |
| ≥ 0.7 | spiky |

The original draft's two-bin HIGH/LOW split at CV 0.60 conflicted with the lock (3 bins at 0.3/0.7) and is retired.

**Measurement implementation (gamora seam):** gamora adds per-event damage tracking to FightResult (alongside the § Session 2 proxy_damage additions). `damage_event_log: list[float]` with all player-dealt per-EVENT damage magnitudes; CV computed in balance_loop or telemetry post-fight. (Per-event, not per-tick: a beam contributes one event per tick it deals damage; a nova contributes one event per enemy hit — consistent with the locked definition's event basis.)

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
| MOMENTUM_CASCADE kit | 5 | 0 | 1 (momentum stacks) | 1 (Cascade reset timing) | 9.0 | MEDIUM |
| RESONANCE_LOOP + hybrid element | 5 | 2 (Partner A → Partner B) | 2 (Resonance state; 12s window) | 2 (3s seq window; 12s Res window) | 17.0 | HIGH |
| TEMPORAL_CHARGE + charge-stack | 5 | 0 | 2 (charge count; threshold state) | 2 (hold timing; threshold window) | 13.0 | MEDIUM |
| RESONANCE_LOOP + MOMENTUM_CASCADE (3-chain kit) | 6 | 2 | 3 | 3 | 22.0 | HIGH |

*(Scores corrected 2026-06-12 to match the LOCKED § 6.2 formula — prior listed 8.0 / 10.5 / 19.5 on rows 3, 5, 6 were authoring arithmetic slips (dropped `timing×2.5` / `state×1.5` terms); rocket Flag 1 confirmed. Bins unaffected — the formula is the source of truth and rocket implemented it exactly; no code change.)*

### 6.5 Rocket generation directive

Rocket computes cognitive_load_score at kit finalization (after T4 strategy assignment, since T4 contributes the majority of state_conditions and timing_windows). The score and bin are stored in the kit record as `cognitive_load_score: float` and `cognitive_load_bin: str`.

QD engine uses `cognitive_load_bin` as a secondary axis if a Cognitive Load hypothesis axis is added to the BC grid in Session 5. For now: stored but not a primary QD cell axis.

---

## 7. Session 3 open questions

| # | Question | Priority |
|---|---|---|
| 1 | Terrain-reactive: gamora boundary assessment needed before session can fully lock (see gamora kernel handoff § 5). Is terrain_type a caller-side parameter to simulate_fight or a kernel branch? | HIGH — gamora assessment gates spec lock |
| 2 | ~~QD grid cell count expansion~~ RETRACTED at normalization pass — the locked 68,040 cells already include the 7-bin Axis 5 with charge-stack; no expansion occurs (§ 2.3). Replaced by **Q9 (hold-vs-spend)** — **RESOLVED 2026-06-12** (Matt-ratified: spend-all + passive per-stack held bonus; see § 2.3; gamora Item 4 + rocket Item 10 un-held) | ~~HIGH~~ CLOSED |
| 3 | `front_load_profile` (NEW metric, § 5.1 — NOT Axis 3A, which is locked): is the 3-second window the right front-load threshold? PoE uses "hit-count in first 3 skills used" as an alternative. Also: promote to QD axis or keep as telemetry-only? | MEDIUM — design preference |
| 4 | Cognitive load — sequence_depth for chain combos: do chains themselves create sequence requirements, or only T4 strategies? **RULED 2026-06-12 (gandalf):** initially deferred T4-only behind empirical gate. **RESOLVED-VIA-FLIP 2026-06-13 (gandalf):** the empirical gate is SATISFIED. The Season 001010 generation distribution (N=240, rocket) shows **26/240 kits (10.8%) flip a cognitive-load bin under Δscore = 2.0 × max(0, coupling_depth−1), and ALL 26 carry coupling (cd≥2), ALL clustered at the MEDIUM→HIGH boundary.** Coupling is NOT immaterial to bins — it is precisely the variable deciding membership at the one boundary it can cross. This satisfies the commit criterion exactly as authored. **SET `INCLUDE_COUPLING_IN_SEQUENCE_DEPTH = True`.** Design rationale: a coupled (chain-gated) kit demands more working memory than raw skill_count implies — cf. PoE trigger-chain builds where firing order is load-bearing. Ignoring coupling under-reports the kits that feel hardest to pilot; the flip makes the metric track player-felt load. The 26 boundary kits re-bin to HIGH and gain RESONANCE_LOOP / TEMPORAL_CHARGE eligibility — the intended consequence. No further validation gate; this WAS the gate. **Q4 CLOSED.** | ~~HIGH~~ ~~DEFERRED~~ CLOSED — flip True |
| 5 | Axis 3B thresholds are LOCKED at CV 0.3 / 0.7 (per-event) — not open for gut-recalibration. Remaining empirical question: what does the CV distribution on the Season 001010 corpus look like against the locked bins (population coverage, not threshold choice)? | LOW — telemetry read |
| 6 | Displacement effects (knockback / pull / taunt) are outside the locked Axis 2B inclusion list (§ 4.5): leave uncounted, or propose lock amendment to count them? | MEDIUM — Matt call |

---

**Author:** gandalf, 2026-06-12. Matt-authorized Session 3 spec from Pattern B session. Partially independent of Session 1; can begin after Session 2 gamora kernel handoff fires.
