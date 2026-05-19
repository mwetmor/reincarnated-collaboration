# ARPG Mod-Target Database — KPIs, Modding Interfaces, Compatibility Scoring (2026-05-18)

**Status:** Extended research artifact. Companion to `arpg-fight-mechanics-database-2026-05-18.md` (combat-axis comparator data) and `arpg-gap-analysis-2026-05-18.md` (gap synthesis). This database adds: (1) Reincarnated engine KPI/pattern/schema inventory, (2) KPI extraction for original 4 comparators, (3) survey + KPIs for expanded candidate set with active modding communities 2024-2026, (4) modding interface specifications per candidate, (5) compatibility scoring matrix Reincarnated → each candidate.

**Authored by:** gandalf — synthesis across multiple parallel Legolas Mode-A research returns + Explore engine-codebase audit.

**Authored:** 2026-05-18 late evening.

**Goal-statement (Matt's mandate):** *Understand Reincarnated's ability to tune to quick-modding capability.* Every section ladders to this. Methodology revisable per gandalf wisdom + hive mandate.

---

## § 0 — Scope and methodology

**Producer side:** Reincarnated emits structured content (substrates, classes, skills, monsters, gear, balance reports). The full producer profile lives in § 4.

**Consumer side:** Host games accept content through modding interfaces. Each host has its own KPI patterns (combat math, geometry, AI, balance) AND its own input contract (file formats, schemas, required fields). Both must be catalogued for fit-scoring.

**Compatibility scoring:** For each producer-consumer pair, score on 4 axes:
1. **KPI / pattern compatibility** — does the host model fights similarly to how Reincarnated does? (similar = lower translation overhead)
2. **Schema compatibility** — does Reincarnated's output JSON map cleanly to the host's required input schema?
3. **Modding pipeline accessibility** — can a human or automated exporter actually publish content to this host?
4. **Community vitality** — is there an audience for the published mod?

Each axis scored 1–5; weighted average = **Modding Fit Score (MFS)**. Top-MFS targets are the recommended mod-first candidates.

**Methodology revisable:** if the scoring exposes a goal-misalignment (e.g., highest-MFS target isn't actually the best commercial play), the weighting or the question gets revised. The mandate is *"understand the ability to tune to quick modding capability,"* not *"compute a fixed score."*

---

## § 1 — KPI / pattern schema (consistent across all games)

Every game profile addresses these dimensions:

| Category | Dimensions |
|---|---|
| **Mathematical** | Damage formula chain; variance bands; HP/armor/resistance scaling; DPS calc; balance convergence math; PackProxy or equivalent; geometry multipliers; trait/affix scaling; crit/accuracy math; cooldown math |
| **Geometrical** | Skill geometry catalog; AOE/cone/ring/line shapes; range threshold model; pack composition; spatial primitives (2D/3D coordinates) |
| **Logical** | AI framework (BT/FSM/utility/scripted); skill rotation logic; balance rules; generation rules (if procgen); pool filtering |
| **Temporal** | Tick rate / timestep; fight duration limits; cooldown system; animation timing; balance loop iteration cap |
| **Geospatial** | Distance bands; range thresholds in units; movement speed; kite mechanics; spatial substrate (1D scalar / 2D iso / 3D world) |
| **Output / Input schema** | Per-artifact field inventory: monster, class, skill, gear, affix, substrate, season, balance report, telemetry, trait pool |
| **Content generation** | Procedural authoring (if any); LLM layer (if any); grammar/templates; validation/retry |
| **Catalogue structure** | Internal library; substrate definitions; element pool; geometry palette; trait/affix/skill pools |
| **Modding interface** | Tool name(s); file format(s); injection ceiling; schema requirements; validation pipeline; distribution channel; cross-mod compatibility |

---

## § 2 — Reincarnated engine (producer profile) — FULL INVENTORY

*Comprehensive KPI inventory returned 2026-05-18 late evening via Explore agent on engine codebase.*

### § 2.1 — Mathematical KPIs (COMPLETE)

**Damage formula chain** (per `foundation/math_model.py:116-142` + `simulation/damage_resolver.py:122-240`):

```
base_magnitude
  × (1.0 + attribute × DAMAGE_SCALING_RATE)         [DAMAGE_SCALING_RATE = 0.005]
  × (1.0 + buff_damage%) × damage_modifier × (1.0 + bonus_damage%)
  × geometry_multiplier                              [per B11/B24 geometry type]
  × hit_check                                        [accuracy=0.90 - dodge_chance]
  × crit_multiplier                                  [if crit; CRIT = 1.5×]
  × armor_mitigation                                 [physical: 1 - armor/(armor + 3000)]
  × elemental_resistance                             [non-physical: 1 - min(0.95, res)]
  × substrate_matrix[attacker][defender]             [holy/shadow vs opposed: ±25%]
  × pack_proxy_size                                  [if AOE geometry vs PackProxy]
  × per_hit_variance                                 [uniform(0.80, 1.20)]
```

**Stat scaling formulas:**
- HP = `10_000 + vitality × 75 + strength × 20` (HP_BASE/HP_PER_VIT/HP_PER_STR)
- Armor mitigation = `armor / (armor + 3000)` (ARMOR_MITIGATION_K, no hard cap)
- Crit chance = `min(0.75, 0.05_base + dex × 0.001)`
- Dodge chance = `min(0.60, 0.05_base + dex × 0.0015)`
- Status resistance = `min(0.80, wis × 0.002)`
- Max mana = `base + int × 1.0 + wis × 0.5`
- Mana regen = `base × (1.0 + max(int,wis) × 0.002)`

**Variance bands:**
- Per-hit damage: ±20% (uniform 0.80–1.20)
- Per-fight DPS: ±25% (uniform 0.75–1.25, applied once at fight start)
- Cooldown jitter: ±10% proportional + ±50ms absolute floor

**Balance loop convergence** (`balance_loop.py:36-75`):
- Binary search on `damage_modifier` (B14.5 two-phase: recompose-first then redistribute)
- Tolerance: ±3% WR (`TOLERANCE = 0.03`)
- Max iterations: 10 (`MAX_ITERATIONS`)
- Adjustment step: `mod *= (1 ± 0.20 × |gap| / 0.03)`
- RECOMPOSE_MAX_ATTEMPTS = 3 per lever; RECOMPOSE_DELTA_FLOOR = 0.02
- Modifier thresholds: LOW = 0.30, HIGH = 3.0
- Secondary loop: SECONDARY_STEPS = (0.05, 0.10, 0.20) element redistribution

**Gauntlet:** 100 fights/class vs reference 8-monster pool at GEAR_PERCENTILE = 0.75; trial: 50 fights/class vs doppelganger (HP_BONUS = 1.05).

**PackProxy (B10.2):**
- PACK_PROXY_SIZE = 8 (single proxy entity)
- Pack HP = `base_hp × 8` (linear M1+M2)
- AOE damage × 8 if geometry in AOE_GEOMETRIES
- Single-target damage applied once per pack

**Geometry multipliers** (B11/B24 — full table in § 2.2)

**Role magnitude multipliers** (`foundation/math_model.py:49-76`):
- primary_attack: 0.25, burst_damage: 1.0, area_damage: 0.6, damage_over_time: 0.3
- control/mobility/defensive/utility: 0.0 (non-damage)
- sustain: 0.5

**Trait aggregation** (`generation/trait_schema.py:241-297`):
- STAT (flat): sum per stat_key
- STAT (proportional): sum separately
- ABILITY (additive keys): sum per key (e.g., crit_bonus_damage)
- ABILITY (multiplicative keys): compose via product, identity 1.0 (cooldown_factor, energy_cost_factor)
- GRANTED: dedup by role; source priority (gear > progression) first-wins

### § 2.2 — Geometrical KPIs (COMPLETE)

**Geometry type catalog: 24 types** (per `generation/geometry_derivation.py:31-56`):

```
ground_targeted_circle, circle, self_buff, single_target,
vortex_pull, multi_projectile, beam_channel, teleport,
ring, aura, line, cone,
melee_strike, ground_slam, melee_arc,
chain_lightning, ricochet_bounce, dash_attack,
totem, defensive_dash, blink,
fork, whirlwind, leap_strike
```

**MELEE_GEOMETRIES set** (`combatant.py:45`): `{melee_strike, melee_arc, ground_slam}` — gated by `at_melee_range` boolean.

**AOE_GEOMETRIES set** (per `b6_archetype_templates.py`): vortex_pull, multi_projectile, ring, aura, line, cone, chain_lightning, ricochet_bounce, whirlwind, leap_strike, ground_slam.

**Geometry multiplier formulas** (`damage_resolver.py:307-383`):

| Geometry | Multiplier formula | Defaults | Total mult |
|---|---|---|---|
| chain_lightning / ricochet_bounce | `(1 - decay^(n+1)) / (1 - decay)` | n=3, decay=0.7 | ~2.43× |
| fork | `1.0 + n × per_fork_mult` | n=2, per=0.6 | 2.2× |
| multi_projectile | `n × per_projectile_mult` | n=4, per=0.65 | 2.6× |
| ring | `damage_multiplier` (donut positioning bonus) | 1.2 | 1.2× |
| leap_strike | `landing_multiplier` (impact burst) | 1.3 | 1.3× |
| vortex_pull / dash_attack / whirlwind | 1.0× metadata-only in 1v1 sim | 1.0 | 1.0× |

**Archetype → geometry bias weights** (`b6_archetype_templates.py:25-30`):
- BIAS_PREFERRED = 2.0 (sampled pool ×2)
- BIAS_NEUTRAL = 1.0
- BIAS_PENALIZED = 0.1 (low weight; not forbidden)

**Distance bands (3-band Gate-3b model):**
| Constant | Value | Meaning |
|---|---|---|
| CLOSE_THRESHOLD | 1.5 m | Melee engagement boundary |
| MID_THRESHOLD | 12.0 m | Max active-engagement; FAR above |
| ENGAGEMENT_DISTANCE_START | 6.0 m | All fights begin here |
| KITE_TRIGGER_DISTANCE | 4.5 m | Ranged retreats when monster closer |
| DISTANCE_BAND_CLOSE | 0 | d ≤ 1.5m — melee zone |
| DISTANCE_BAND_MID | 1 | 1.5m < d < 12m — ranged/kiting |
| DISTANCE_BAND_FAR | 2 | d ≥ 12m — re-engagement, no actions |

**Movement speed baselines** (per `export/schemas.py:52-77`; canonical/story/movement-speed-baseline.md VERDICT REVERSAL 2026-05-16):
- Player base: 8.0 m/s (end-game gear-only; PoE-1-excluded T1 mean)
- Monster trash: 5.75 m/s (parity with player base, AI-speed ratio 0.719)
- Fast archetypes (swarmer, sniper): 7.5 m/s
- Demo pixel ratio: 48 px/m (locked)

**Spatial substrate:** Engine sim is **1D scalar `distance_m`** (no 2D coordinates). Demo runtime has 2D pixel positions but **no entity-entity collision** (deferred at `world/movement.ts:197-199`).

**Per-skill range:** NONE in catalogue. Only binary `at_melee_range` gate.

**Per-skill spatial footprint:** Geometry TYPES are catalogued (24); spatial PARAMETERS (radius, cone angle, line length, etc.) are NOT surfaced as fields — the multiplier formulas above use abstract parameters (chain_count, fork_count, etc.) without geometric dimensions.

### § 2.3 — Logical KPIs (COMPLETE)

**AI strategies** (`ai_strategies.py:52-274`):
- Per-archetype role priority list (18 explicit entries for Phase-3 composed archetypes)
- Example: `ARCHETYPE_ROLE_PRIORITY["water_controller"] = ["control", "damage_over_time", "burst_damage", "primary_attack"]`
- Fallback: `_REGISTRY_DEFAULT_PRIORITY` for unknown archetypes
- Action selection: iterate roles in priority → find ready skill → if none ready, return None (wait/regen)
- Auto-attack fallback: 1× per second when all skills on CD

**Role registry — 9 canonical roles** (`config/roles.yaml`):

| Role | AI Priority | Damage Cat | Key Constraints |
|---|---|---|---|
| primary_attack | 5 | damage | min_1_dps_early_tier |
| burst_damage | 2 | damage | — |
| area_damage | 3 | damage | — |
| damage_over_time | 4 | damage | — |
| control | 1 | nondamage | control_first, min_4_dps_skills, min_1_dps_aoe |
| mobility | 6 | nondamage | mobility_identity |
| defensive | 8 | nondamage | defensive_floor |
| sustain | 7 | nondamage | sustain_identity |
| utility | 9 | nondamage | utility_identity |

**Ailment registry — 8 canonical ailments** (`config/ailments.yaml`):

| Ailment | Category | Control | Substrate | Default params |
|---|---|---|---|---|
| burn | dot | none | fire | duration 5s (3–7) |
| chill | soft_control | soft | water | slow 35% (20–50%), duration 3s (2–5) |
| root | hard_control | hard | earth | duration 2.5s (1.5–4) |
| knockback | hard_control | hard | wind | distance 5m (3–8), stagger 0.5s |
| bleed | dot | none | physical | duration 5s (3–7) |
| shock | hard_control | hard | lightning | duration 1s (0.5–2) |
| consecrate | amplification | none | holy | zone 5s (3–8), heal amp 10% (5–20%) |
| drain | dot | none | shadow | duration 6s (4–9) |

**Balance rules:**
- Gauntlet WR target: 50% (band 47–53%, ±3% tolerance)
- **Aggregate mean only — NO per-tier WR thresholds** (this is the Axis-2 gap in canonical doc)
- 100 fights per class vs reference pool
- 50 fights per class vs doppelganger (DOPPELGANGER_HP_BONUS = 1.05)

**Generation rules** (`generation/season_orchestrator.py`):
1. Element selection (LLM) → canonical pool + proposals
2. Mechanical generation (deterministic, per seed) — class, monster, trial, gear
3. Balance loop (iterative convergence on damage_modifier toward 50% WR)
4. Naming phase (LLM, ~317 calls)
5. Output serialization to season_*/ directory

**Element affinity** (`b6_archetype_templates.py:36-46`): fire ↔ {wind, earth}; water ↔ {earth, wind}; etc.

**Hybrid restrictions:** `HYBRID_FORBIDDEN_PAIRS` derived at boot from `config/substrate_identities/*.yaml`.

**Class composition taxonomy:**
- role_orientation: damage / control / support / hybrid
- range_profile: close / medium / long
- energy_type: mana / rage / combo / focus / stamina-as-resource

### § 2.4 — Temporal KPIs (COMPLETE)

**Tick / fight timing** (`fight_engine.py:18-104`):
- TICK_SIZE = 0.1 s (100 ms)
- DEFAULT_MAX_DURATION = 120.0 s (2-min hard cap)
- AUTO_ATTACK_INTERVAL = 1.0 s
- CLOSE_TO_MELEE_TIME = 0.5 s
- POTION_THRESHOLD = 0.30 (use at <30% resource)
- POTION_COUNT = 2 per combatant
- POTION_HP_FRACTION / POTION_MANA_FRACTION = 0.50 (restore 50%)

**Resource accumulation:**
- Rage: per-hit-dealt 10.0, per-hit-taken 5.0, per-auto-attack 5.0
- Combo: per primary_attack 1.0
- Focus: per skill use restore 10.0 (decays passively)

**Balance loop cadence:**
- MAX_ITERATIONS = 10 (binary search)
- RECOMPOSE_QUICK_ITERS = 10 (safety cap for quick modifier estimates)
- RECOMPOSE_MAX_ATTEMPTS = 3 per lever

**Season cadence:** ~1 week per season (external orchestration; not engine-enforced).

**Telemetry sampling** (`telemetry/recorder.py`): schema v2.5, per-season aggregates (not per-tick).

### § 2.5 — Geospatial KPIs (COMPLETE)

Per § 2.2 above — single scalar `distance_m` between exactly two combatants in engine sim. No 2D. No mob-to-mob distances. No spatial substrate.

**Demo runtime** (`reincarnated-demo/src/world/`):
- 2D pixel positions per entity
- PREFERRED_RANGE: { close: 90, medium: 420, long: 660 } (TS constants — NOT from JSON)
- KITE_TRIGGER: 300 (TS constant)
- **NO entity-to-entity collision** (`movement.ts:197-199` explicitly deferred)
- **NO leash / aggro radius / outrun mechanics**

### § 2.6 — Output JSON schemas (COMPLETE — see § 2.6.x sub-sections)

#### § 2.6.1 — Monster JSON
**Path:** `season_*/monsters/monster_NNNNN.json`. Full schema:

```json
{
  "id": "monster_00005", "name": "...", "flavor_text": "...",
  "threat_tier": "swarm|magic|trash|elite|mini-boss|boss",
  "archetype_tag": "brute|caster|swarmer|sniper|controller|tank",
  "energy_type": "mana|rage|combo|focus|stamina-as-resource",
  "role_orientation": "damage|control|support|hybrid",
  "range_profile": "close|medium|long",
  "dominant_element": "fire|water|earth|wind|lightning|holy|shadow|physical",
  "seasonal_dominant_element": "char|brine|...",  // Stage 3 cosmological name
  "max_hp": 2047.0, "armor": 8.0,
  "elemental_resistances": {"fire": 0.37, "water": 0.08, ...},
  "skills": [/* Skill schema § 2.6.3 */],
  "balance_metadata": {/* convergence data */},
  "movement_speed": 5.75
}
```

#### § 2.6.2 — Class JSON
**Path:** `season_*/classes/class_NNNN.json`. Full schema:

```json
{
  "id": "class_0007", "name": "...", "title_completion": "...", "flavor_text": "...",
  "archetype_tag": "water_controller",
  "energy_type": "mana", "role_orientation": "control",
  "range_profile": "medium",
  "dominant_element": "water", "seasonal_dominant_element": "brine",
  "color_palette": [461347, 615662, /* 13 colors */],
  "stat_distribution": {"strength": 16, "dexterity": 13, "intelligence": 156, "wisdom": 5, "vitality": 80},  // 270 budget
  "skills": [/* Skill schema */],
  "carried_gear": {/* Gear schema § 2.6.4 */} | null,
  "balance_metadata": {"damage_modifier": 1.23, "convergence_iteration": 7, "final_win_rate": 0.501},
  "movement_speed": 8.0
}
```

#### § 2.6.3 — Skill JSON
17+ fields, both player and monster:

```json
{
  "id": "skill_000144", "name": "Exhumation Surge",
  "composition_mode": "single|layered|fused|triadic",
  "role": "primary_attack|burst_damage|area_damage|damage_over_time|control|sustain|mobility|defensive|utility",
  "canonical_element": "fire|water|earth|wind|lightning|holy|shadow|physical",
  "seasonal_element": "char|brine|...",
  "geometry_type": "/* one of 24 — see § 2.2 */",
  "effect_category": "damage_over_time|area_damage|control|sustain|damage|defensive|utility",
  "canonical_pair_ref": "canonical/wind/area_damage",
  "energy_cost": 28.4, "cooldown_seconds": 3.7, "damage_multiplier": 1.0,
  "effects": [
    {"name": "damage|burn|chill|root|knockback|bleed|shock|consecrate|drain|shield|heal|heal_over_time|buff_*|silence|lifesteal",
     "params": {"magnitude": 1500, "element": "wind", "duration_seconds": 0.9, "distance": 4.0, ...}}
  ],
  "color_value": 461347, "flavor_text": "...",
  "tier": 1,
  "chain_id": "chain_A|chain_B|flat|null",
  "chain_position": 1,
  "parent_skill_ids": [],
  "scaling_coefficient": 1.065,
  "trait_slots": [],
  "unlock_flavor": null, "cast_time": null, "damage_resolution_time": null, "i_frame_window": null
}
```

**Note:** `cast_time`, `damage_resolution_time`, `i_frame_window` fields EXIST but are NULL in current outputs — telegraph/wind-up schema reserved but unused.

#### § 2.6.4 — Gear JSON
**Path:** `season_*/gear_pool_staged.json` or `season_*/gear/[slot]/[tier]/item_NNNNN.json`. 25+ fields:

```json
{
  "id": "gear_3169691", "base_type_id": "bow",
  "slot": "weapon|armor|accessory|off_hand",
  "tier": "common|uncommon|rare|epic|legendary", "rarity_score": 1,  // 1–5
  "handedness": "1h|2h",
  "dominant_element": "fire|...|physical",
  "stats": {"bonus_hp": 0.0, "bonus_armor": 0.0, "bonus_crit_chance": 0.0, "bonus_damage_flat": 1404.1, "bonus_damage_percent": 0.0, "bonus_mana_regen": 0.0, "elemental_resistances": {"fire": 0.12, ...}, "block_chance": 0.0, "block_value": 0.0},
  "rolled_effects": [{"effect_type": "damage|burn|...", "element": "wind|null", "trigger": "on_hit|on_crit|on_kill|passive", "magnitude": 693.6}],
  "ability_modifiers": {"cooldown_factor": 0.85, "energy_cost_factor": 0.9, ...},
  "traits": [{"trait_id": "gear_123", "category": "stat|ability|granted", "stat_key": "bonus_damage_flat", "stat_value": 100.0}],
  "stat_requirements": {},
  "power_score": 0.1573,
  "class_fit_profile": {"energy_type": {"mana": 0.211, ...}, "range_profile": {"close": 0.053, "medium": 0.316, "long": 1.0}, "role_orientation": {"damage": 1.0, ...}, "armor_weight": {"all": 1.0}, "damage_type": {"all": 1.0}},
  "canonical_pair_ref": null,
  "color_value": 319470, "color_palette": [436576, 255597],
  "color_signature": null,  // legendary only
  "set_id": null, "set_position": null, "set_piece_count_required": [],
  "name": "Rootwood Bow", "flavor_text": null, "visual_prompt": null,
  "season_id": null, "generation_mode": "mechanics_only|named"
}
```

#### § 2.6.5 — Trait JSON (aggregated in CombatantState)
```python
AggregatedTraits {
  stat_deltas: dict[str, float],         # {stat_key: total_flat}
  stat_proportional_deltas: dict[str, float], # {stat_key: total_prop}
  ability_modifier_totals: dict[str, float],  # {key: aggregated_value}
  granted_abilities: list[tuple[str, str|None]]  # [(role, element), ...]
}
```

#### § 2.6.6 — Season Manifest JSON
**Path:** `season_*/manifest.json`. Schema:

```json
{
  "manifest_version": "1.6",
  "season_id": "season_002017",
  "generated_at": "2026-05-18T15:22:27Z",
  "engine_git_sha": "97cbaaf", "engine_version": "1.4-d3-path-a",
  "generation_seed": 2017, "season_theme_element": "water",
  "anchor": {"id": "...", "name": "...", "category": "...", "description": "..."},
  "elements": {"fire": {"element_id": "char", "name": "char", "tags": [...], "is_new": true}, ...},
  "seasonal_elements": {"ignition": {"element_id": "char", "canonical_slot": "fire", ...}, ...},
  "elements_metadata": {"new_in_this_season": [...], "proposals_added_to_pool": []},
  "cosmological_vocabulary": {"grouping_layer_version": "v1.2", "slot_fills": {...}},
  "summary": {"classes_generated": 11, "monsters_generated": 44, "trial_defeat_rate_actual": 0.489, "convergence_failures": 5, "generation_duration_seconds": 3777.3},
  "validation_passed": false
}
```

#### § 2.6.7 — Cosmological Vocabulary JSON
**Path:** `season_*/cosmological_vocabulary.json`. **8 canonical slots:**

```json
{
  "grouping_layer_version": "v1.2",
  "slot_fills": {
    "ignition": "Pyre Debt", "suffusion": "Burial Seep", "bulwark": "Interment Lock",
    "displacement": "Exhumation Surge", "impact": "Ossuary Strike", "radiance": "Census Light",
    "penumbra": "Unregistered Absence", "resonance": "Catacomb Transit"
  }
}
```

#### § 2.6.8 — Trial JSON
**Path:** `season_*/trial.json`. Schema matches Monster JSON with `threat_tier: "boss"`.

#### § 2.6.9 — On-disk structure
```
season_*/
├── manifest.json
├── cosmological_vocabulary.json
├── validation_report.json
├── gauntlet_recipe.json
├── reference_gauntlet.json
├── trial.json
├── generation_log.txt
├── fights.jsonl                  # newline-delimited fight telemetry
├── classes/class_NNNN.json
├── monsters/monster_NNNNN.json
├── gear/[slot]/[tier]/item_NNNNN.json
└── gear_pool_staged.json
```

### § 2.7 — Content generation patterns (LLM layer — COMPLETE)

**LLM call timeline** (per `canonical/19-llm-call-map.md` + agent inventory):
1. Season setup: element selection [1 call]
2. Mechanical generation: 0 LLM calls (deterministic)
3. Balance / convergence loop: 0 LLM calls
4. **NAMING PHASE** (_name_everything):
   - Class skills: ~50 calls
   - Class names: ~10 calls
   - Monster skills: ~120 calls
   - Monster names: ~40 calls
   - Trial skills: ~5 calls
   - Trial name: 1 call
   - Gear pool naming (epic/legendary): ~80 calls
   - Carried gear naming (epic/legendary): ~10 calls
5. Season writeup / persistence: 0 LLM calls

**Total: ~317 calls / season. Cost: ~$0.74 / season (Sonnet pricing).**

**Naming output schema:** Each naming call returns consolidated JSON `{name, flavor_text, visual_prompt, [color_signature for legendary]}`.

**Validation/retry:** Element selection validates against allowed set; naming validates JSON schema; up to 2-3 retries on failure.

### § 2.8 — Catalogue structure (internal canonical library — COMPLETE)

**File:** `reincarnated-engine/src/reincarnated/canonical/library_schema.py`

**CanonicalEntry schema:**
```python
class CanonicalEntry:
    id: str                              # "canonical/fire/area_damage"
    element: str                         # "fire"
    effect_category: str                 # "area_damage"
    canonical_name: str                  # ≤5 words
    canonical_alternates: list[str]      # ≥2 alternates
    flavor_descriptor: str
    particle_theme: str                  # VFX placeholder
    audio_theme: str                     # audio placeholder
    color_signature: str                 # hex e.g. "#E25822"
```

**Substrate coverage:**
- Canonical-four: fire / water / earth / wind (rotating; always present)
- Canonical-seven Phase-1 P1: + lightning / holy / shadow (rotating; optional)
- Physical: non-rotating (static; always present)
- Total: 7 substrates + physical = 8 (the "canonical-7" + physical effectively 8)

**Effect categories (9 roles):** primary_attack / burst_damage / area_damage / damage_over_time / control / sustain / mobility / defensive / utility.

**Canonical library size:** ~40+ entries (one per element × effect_category combination).

**Substrate identity declarations** (`config/substrate_identities/[element].yaml`):
- forbidden_hybrid_with
- Cosmological slot fills (8 slots)
- AI priority override for composed archetypes
- Canonical ailment assignment

**Element pool (D1 pool)** in `config/elements.yaml`:
- 156 entries total per memory
- Fields per element: name, display, ailment, rotating (bool), resistance_type (percentage|armor), dodgeable (bool), scales_with (intelligence|wisdom|strength), theme_tags, color_range
- Multi-round Matt-vetted overrides: allow-list / eligible / quarantine status

**Internal canonical library is rocket's domain** per AGENTS.md.

### § 2.9 — Reincarnated as producer — summary

**What Reincarnated reliably produces** (per the comprehensive inventory):

*Mechanical contracts (fully deterministic, no LLM):*
- Substrate × element vocabulary (canonical-7 + physical; 156-entry element pool with D1 scoring)
- Per-class kit: archetype tag, role orientation, range profile, energy type, stat distribution (270 budget), 9-role skill set, color palette (13 colors), balance metadata
- Per-monster stat block: threat_tier (7 tiers), archetype_tag, energy_type, role_orientation, range_profile, dominant_element, seasonal_dominant_element, max_hp, armor, elemental_resistances (per-element dict), skills list, movement_speed, balance_metadata
- Per-skill record: 17 fields including composition_mode, role, canonical_element, seasonal_element, geometry_type (24 options), effect_category, canonical_pair_ref, energy_cost, cooldown_seconds, damage_multiplier, effects (list of typed {name, params} pairs), color_value, scaling_coefficient, optional tier/chain_id/chain_position/parent_skill_ids
- Per-gear record: 25+ fields including base_type_id, slot, tier, rarity_score, handedness, dominant_element, stats dict (10 fields), rolled_effects, ability_modifiers, traits list, stat_requirements, power_score, class_fit_profile (5 dimensions), color signatures, set membership
- Per-trait record: category (stat/ability/granted), stat_key, stat_value, source attribution, dedup rules
- Season manifest: ID, theme, anchor, elements (canonical + seasonal), cosmological_vocabulary (slot_fills), summary stats, validation_passed
- Telemetry per fight: schema v2.5 anchor + element + class + monster + trial + gear + LLM call records + fight aggregates

*LLM-authored layers (~317 calls/season, ~$0.74/season):*
- Element selection per season + new element proposals
- Class names (≤5 words)
- Monster names + flavor + visual prompt
- Skill names + flavor (per skill, ~50 class + ~120 monster + ~5 trial)
- Gear naming (epic/legendary only, ~80 + ~10 carried)
- Cosmological vocabulary slot fills (8 slots: ignition / suffusion / bulwark / displacement / impact / radiance / penumbra / resonance)

**What Reincarnated does NOT produce (gaps for modding-export):**

*Spatial / behavioral fields the engine has no concept of:*
- Per-skill range published in tooltips (engine only has at_melee_range gate)
- Per-skill geometry footprint with spatial parameters (engine has 24 geometry TYPES but no radius/cone-angle/cylinder-dimension values surfaced for spatial rendering)
- Aggro radius / leash distance / per-mob spatial behavior
- Telegraph window / wind-up timing per skill
- AI behavior specification beyond archetype-priority rotation (no threat-targeting rules, no kite-distance preferences, no positional skill choice)
- Spatial layout / encounter placement (where mobs spawn in a room; engine is 1v1 sequential gauntlet)
- Visual model references (3D mesh, sprite, animation rigs)
- Skill VFX particle/audio references (canonical entries have *placeholders* — particle_theme, audio_theme — but no actual asset bindings)
- Sound effect / dialog references
- Map / world geometry (no level data)
- Quest / narrative structure
- NPC dialog

*These gaps fall into 3 fix-tier buckets:*

| Tier | Gap type | Fix cost |
|---|---|---|
| **R3-tier** (schema migration) | Range, geometry params, aggro radius, leash, telegraph, AI behavior fields | 2–4 wk (rocket + star-lord + elrond) |
| **Asset-binding tier** | VFX, audio, visual model references | Out of scope for engine; host-game-side or human-art-side |
| **World-content tier** | Map geometry, quest structure, NPC dialog | Out of scope; host-game-side authoring |

**Modding-export observation:** Reincarnated's mechanical layer is **highly structured and exportable**. The LLM layer is **isolated to naming/vocabulary** (post-mechanical). This separation means a modding-export pipeline can:
1. Run mechanical generation deterministically (no LLM cost for the mechanics export)
2. Run naming pass per host-game (potentially per-language, per-style)
3. Translate JSON output to host-game schema (DBR for Grim Dawn, Lua for DD2 REFramework, ESM for Skyrim Creation Kit, etc.)

The structural cleanliness is a **major asset** for modding-export. Far better positioned than if mechanics and narrative were tangled.

---

## § 3 — Modding interface schema (consistent across all games)

Every host game profile addresses:

| Field | Description |
|---|---|
| **Tool name(s)** | Official or community modding tool (Asset Manager, GUTS, Creation Kit, REFramework, etc.) |
| **File formats** | JSON / XML / DBR / Lua / Plugin / SDK / Binary |
| **Required fields per entity** | What MUST a mod author provide for: class, skill, monster, item, zone |
| **Optional fields** | What CAN a mod author provide |
| **Validation pipeline** | How does the host ingest mods; runtime vs. compile-time validation; failure modes |
| **Injection ceiling** | Cosmetic / QoL / Balance / Content-Injection / Total-Conversion |
| **Cross-mod compatibility** | Single mod at a time? Load order? Merge tools? Conflict resolution? |
| **Distribution channel** | Steam Workshop / Nexus Mods / ModDB / bespoke loader / forum direct |
| **Community vitality (2024-2026)** | Vibrant / Active / Sustained / Niche / Declining / Dormant |

---

## § 4 — Original 4 comparators — extended profiles

### § 4.1 — Wolcen: Lords of Mayhem

**Combat KPIs** (from existing research):
- Spatial: full 3D, fixed isometric, CryEngine 5
- Per-skill range: real internal metric (meters), not surfaced in vanilla tooltips; Better Skill Descriptions mod surfaces it
- AOE: geometrically real (3D volumes, radius/cone/cylinder)
- AI: Kythera behavior trees (web-authored) + contextual steering + Spatial Query System (bosses dodge DoT zones)
- Collision: hard entity↔entity (defining feature, contested)
- Boss phases: HP-threshold transitions
- Movement: universal Spacebar dodge with i-frames + class-specific (Aether Jump, Evasion, Leap)
- Balance: empirical reactive; no public sim infrastructure

**Modding interface:**
- Tools: **None official.** XML file replacement.
- File formats: XML in CryEngine .PAK archives (encrypted with PakEncrypt — unpacker tool required)
- Distribution: NexusMods + ModDB. **No Steam Workshop.**
- Injection ceiling: Cosmetic + light mechanical + balance tweaks. **Cannot mod Gate of Fates, AI behaviors, skill animations, enemy models, dungeon layouts.**
- Cross-mod: file-replacement Umbra folders; manual conflict management
- Community: **Dormant (~24 avg concurrent May 2026; last patch July 2023; multiplayer shut down Sept 2024).**

### § 4.2 — Dragon's Dogma 2

**Combat KPIs:**
- Spatial: full 3D third-person, RE Engine
- Per-skill range: **no numeric tooltips**; range via animation reach + projectile travel + spell radius
- AOE: geometrically real (3D, terrain-interactive); Maelstrom = persistent tornado; Meteoron = 5-impact field
- AI: Goal-based Pawn AI (learning, knowledge-sharing); per-species behaviors
- Collision: **hard entity↔entity + climb-the-monster physics** (defining feature)
- Boss: handcrafted, climbable; phase transitions HP-threshold
- Movement: stamina-gated; vocation-specific; no standard dodge roll (mod adds it)
- Balance: handcrafted, no scaling, no NG+; Itsuno: "didn't make a Nintendo game"

**Modding interface:**
- Tools: **REFramework** (Lua API) — community-built, foundational
- File formats: Lua scripts + asset replacement; RE Engine internals largely compiled C++
- Distribution: NexusMods (~1,100+ mods)
- Injection ceiling: **Recombination only** via SkillMaker / DD2_VocationKit. **Total-conversion not feasible.** No level editor, no quest system, no scripted-dialog editor.
- Cross-mod: REFramework manages load order; December 2024 patch broke many mods (recurring RE Engine fragility)
- Community: **Active but narrow capability ceiling.**

### § 4.3 — Grim Dawn

**Combat KPIs:**
- Spatial: 2.5D isometric (modified Titan Quest engine, single-threaded sim)
- Per-skill range: **published Radius + Projectile in tooltips**; scales with skill level on some skills
- AOE: explicit radius circles, cones, lines; no universal falloff
- AI: simple FSM ("approach until in range, attack" — engine constraint single-threaded)
- Collision: hard player↔mob; mob↔mob unclear (likely passthrough per standard ARPG)
- Boss: HP-threshold phase gates; AI "barely different from random champion encounters"
- Movement: 3 mastery-native (Blitz / Shadow Strike / Vire's Might) + medal-slot runes + v1.2 universal Evade
- Balance: empirical, holistic (Zantai philosophy); 8+ years of patches; no sim infrastructure

**Modding interface — STRONGEST OF THE 4:**
- Tools: **Crate's full internal toolset shipped** — Asset Manager, World Editor, Database Editor, Quest Editor, Conversation Editor, Particle Editor, Lua scripting
- File formats: **DBR** (database records — text-based, per-entity), .arc archives, .lua scripts
- Required fields per entity: documented in DBR templates; Asset Manager validates
- Distribution: **No Steam Workshop;** NexusMods + Crate forum + ModDB; manual install to `mods/` dir
- Injection ceiling: **Full content injection** — masteries (classes), skills, items, monsters, zones, factions all proven. **NOT procedural maps** (engine doesn't support procgen — community workaround: Enemy/Item Randomizer at content layer)
- Cross-mod: **Engine loads ONE mod at a time.** Mod Merger / WanezToolsGD / ComboMod tools handle DBR merging; clean file namespace from inception required.
- Community: **Vibrant 10+ year ecosystem.** Empirical proof: Dawn of Masteries 53-class compilation mod; Grimarillion (Zenith + Grim Quest + D3 port + density mods); Grim Quest (TQ mastery port).

**Reincarnated → Grim Dawn schema fit (preliminary):**
- ✅ Substrate × element → maps cleanly to Mastery system (Crate has classes themed by element/role/archetype)
- ✅ Class kit (skills + traits) → maps to DBR skill records + tier system (9 mastery tiers)
- ✅ Per-monster stat block → maps to MonStats DBR records
- ✅ Gear/affix pool → maps to Item DBR records + affix tables
- ⚠️ Per-skill geometry footprint (radius/cone) → translation: Reincarnated's 9 B11 geometries need mapping to GD's Radius / Projectile / chain parameters
- ❌ Procedural per-season regen → not supported by World Editor; alternative: roll fresh mod per season
- ❌ AI behavior fields → Reincarnated lacks the data; GD AI is simple anyway (lower bar)

### § 4.4 — Genre baseline (D2 / D3 / D4 / PoE1 / LE)

**Combat KPIs aggregate** (from genre-baseline research):
- Spatial: all isometric or near-iso; all have 2D-or-3D position vectors
- Per-skill range: **all five publish per-skill range** (D2 since year 2000 via Weapons.txt rangeadder + Size; D3 implicit; D4 per-skill; PoE explicit modifiable; LE per-skill implicit)
- AOE: all spatial; D3 most relies on Area Damage stat for stacking optimization
- AI: D2 FSM with 8-param tables; D3/D4/PoE/LE FSM-per-archetype mostly
- Collision: D3 softest (deliberate for Area Damage meta); PoE2 hardest; D4 medium-hard
- Boss: phase transitions universal; D4 stagger system (Ashava arm geometry change) is recent innovation
- Movement: D2 partial (Teleport-Sorc outlier); D3/D4/PoE1/LE all universal dedicated movement skill
- Balance: GGG (PoE) most public-philosophy documented; EHG (LE) most math-first; Blizzard via patch notes

**Modding interfaces (all minimal-to-none):**
- D2 (LoD): community modding (Project Diablo 2, Median XL, plugY — open source for D2R is limited)
- D2R: **no official modding**
- D3: **no official modding** (cosmetic only)
- D4: **no official modding** (cosmetic only)
- PoE 1: **no official modding** (no SDK; cosmetic stash tabs via API only)
- PoE 2: **no official modding** (Early Access)
- Last Epoch: **no significant official modding scene**

**Conclusion:** None of the genre-baseline games are viable modding targets. Their value is as **design reference**, not as **modding host**.

---

## § 5 — Expanded candidates (Wave 1 survey returns — full corpus)

**Survey returned 2026-05-18 late evening.** 47 candidates evaluated across 5 genre clusters. ~20 reach Content-Injection-or-better ceiling with active 2024-2026 communities. Wave 2A (4 deep-dive modding-interface investigations) in flight at time of writing: Titan Quest AE, Torchlight 2, Terraria/tModLoader, Baldur's Gate 3.

### § 5.1 — Full survey at-a-glance (top tier only)

| Rank | Game | Ceiling | Community | Adjacency | Could Host Reincarnated? |
|---|---|---|---|---|---|
| **1** | **Grim Dawn** | TC | Vibrant | Strong | **Yes — class injection proven (Dawn of Masteries 53 classes)** |
| **2** | **Titan Quest AE** | TC | Active | **Strong (direct GD ancestor; mastery system structurally identical)** | **Yes — primary mod type is new masteries** |
| **3** | **Torchlight 2** | TC | Active | Strong | **Yes — SynergiesMOD proves 3-class injection** |
| **4** | **Terraria (tModLoader)** | TC | Vibrant | Moderate | **Yes — Calamity / Thorium / N Terraria proof** (presentation: 2D side-scroller) |
| **5** | Minecraft (Forge/Fabric modpacks) | TC | Vibrant (largest mod ecosystem) | Moderate | **Yes — Vault Hunters / RPG modpacks prove ARPG loop** (presentation: voxel) |
| **6** | Rimworld | TC | Vibrant | Tangential (colony sim) | Maybe — traits/roles moddable; loop mismatch |
| **7** | Baldur's Gate 3 | CI | Vibrant | Moderate (turn-based CRPG) | Maybe — subclass injection common; real-time vs turn-based fundamental mismatch |
| **8** | Elden Ring | TC | Vibrant | Moderate | Maybe — Convergence proves spell/weapon/enemy injection; not class-system-deep |
| **9** | Dark Souls 3 | TC | Active | Moderate | Maybe — Cinders / Archthrones proof; same Souls audience concerns |
| **10** | Crusader Kings 3 | TC | Vibrant | Tangential (dynasty sim) | **Speculative interesting** — trait/event system deepest in any strategy game; structurally parallels Reincarnated's spirit-swap |
| **11** | Mount & Blade: Bannerlord | TC | Vibrant | Weak | No — sandbox combat, not ARPG loop |
| **12** | **V Rising** | CI | Active | Moderate | **Maybe — Bloodcraft proves class/perk injection via BepInEx; boss-gallery loop is mechanically resonant** |
| 13 | TL2 SynergiesMOD platform | Nested | Active | Strong | Investigate as add-on host to TL2 base |
| 14 | D2 Median XL / Project D2 | TC | Active | Strong | No — archaic MPQ pipeline; D2R explicitly excluded |
| 15 | Starfield | CI | Active | Weak | No — sci-fi genre mismatch despite Creation Kit power |
| 16 | Skyrim SSE | TC | Vibrant (72k+ mods) | Moderate | No — class architecture too Bethesda-specific; high translation cost |
| 17 | Dark Souls 1 / Remastered | CI | Sustained | Moderate | Maybe — Daughters of Ash precedent; smaller community than DS3 |
| 18 | Starbound | CI | Sustained | Moderate | No — game dev frozen since 2019; no growth audience |
| 19 | Pathfinder: Wrath of the Righteous | Balance/QoL | Active | Moderate | No — modding ceiling too low for content injection |
| 20 | Outward | CI | Niche | Moderate | Maybe — SideLoader works; small audience |

### § 5.2 — Excluded candidates and rationale

Confirmed-no-modding-or-no-meaningful-scene (drop from consideration):
- Diablo 3 / Diablo 4 / PoE 1 / PoE 2 / Last Epoch (covered in genre baseline; no official content injection)
- Torchlight Infinite (GaaS mobile-first; no mods)
- Lost Ark / Undecember (live-service MMO; no mods)
- Fallout 76 (modding bannable per Bethesda policy)
- Sekiro / Lies of P (cosmetic-only mod ceilings)
- Avowed (too new; 51 mods at survey time; all QoL — revisit in 12-18mo)
- The Long Dark (minimal modding; no RPG systems)
- Pathfinder: Kingmaker (superseded by WotR for this analysis)
- Stardew Valley (farming sim — loop too distant for ARPG content)
- Valheim / 7 Days to Die / Kenshi / Project Zomboid / Don't Starve (survival genre; tangential)
- Stellaris / EU4 / Total War WH3 / Civ 6 (strategy genre; tangential except CK3)
- Cyberpunk 2077 (REDmod is powerful but sci-fi mismatch)
- The Witcher 3 (REDkit released 2024 but single-protagonist story-driven; no class system)
- Divinity Original Sin 2 (GM Mode works but custom monsters require Editor; mid-tier ceiling)
- Pillars of Eternity 2 / Mount & Blade Warband / KCD2 (various reasons — genre or ceiling)

### § 5.3 — Top-15 ranked profiles (compact form)

#### Rank 1 — Grim Dawn
*Profile in § 4.3. **CONFIRMED #1.** No change.*

#### Rank 2 — Titan Quest Anniversary Edition (THQ Nordic, 2016)
- **Combat KPIs:** 2.5D isometric (Titan Quest engine), mastery × mastery dual-class system, per-skill range published, AOE explicit, FSM AI, boss phase transitions
- **Modding:** ARC tools (official, well-documented); titanquestfans.net + Nexus + Steam Workshop (lighter); mastery injection is the **primary** mod type; ShadowChampions Multimaster (Mar 2025), Legion of Champions 2024, TQ-to-GD mastery ports established
- **Critical advantage:** Mastery system **structurally identical** to Grim Dawn (Crate is Iron Lore alumni). Cross-porting between TQ and GD is **already established community practice** — content authored for one transfers to the other with low friction.
- **Caveat:** Steam Workshop activity lighter than GD. Verify concurrent players before committing dev time.
- **Wave 2A research in flight** — full modding interface schema deep-dive returning.

#### Rank 3 — Torchlight 2 (Runic / Echtra, 2012)
- **Combat KPIs:** 2.5D isometric, class-based (4 base classes), skill trees, procedural loot
- **Modding:** **GUTS editor (official, comprehensive)** + Steam Workshop + Nexus; supports new skills, items, monsters, maps, quests
- **Critical precedent:** SynergiesMOD — 3 entirely new classes (Necromancer, Warlock, Paladin) + raid dungeons + world bosses. Direct proof of Reincarnated-scale injection.
- **Caveat:** 2012-era tooling; engine age caps visual fidelity; community smaller than TQAE
- **Wave 2A research in flight.**

#### Rank 4 — Terraria via tModLoader (Re-Logic, 2011)
- **Combat KPIs:** 2D side-scrolling tile-based; class system via mods (melee/ranged/magic/summon + Thorium's 3 new); boss progression; gear tiers; procedural worlds
- **Modding:** **tModLoader (official, Steam-integrated, C# API)** — most developer-friendly on the list; excellent documentation
- **Precedents:** Calamity Mod (massive content), Thorium Mod (3 new classes), N Terraria (RPG classes + leveling)
- **Critical mismatch:** 2D side-scrolling presentation vs. Reincarnated's expected top-down HD-2D ARPG. Art assets would need re-authoring for Terraria's vocabulary.
- **Wave 2A research in flight.**

#### Rank 5 — Minecraft via Forge/Fabric modpacks (Mojang/MS, 2011)
- **Combat KPIs:** voxel 3D, melee + ranged primitives; ARPG loop must be modded in
- **Modding:** Forge + Fabric + CurseForge (800M monthly downloads — largest mod ecosystem in gaming); modpacks as host containers
- **Precedents:** Vault Hunters (full ARPG looter), various dungeon-crawl modpacks with talent trees + classes
- **Reach:** 11M+ active monthly modded-Minecraft users — largest audience among all candidates
- **Critical mismatch:** Voxel aesthetic + Minecraft UX conventions deeply distinct. Reincarnated's spirit-swap and class systems must adapt to voxel paradigm. Genre adjacency drops to Moderate-Low in practice.

#### Rank 6 — Rimworld (Ludeon Studios, 2018)
- **Combat KPIs:** colony management → individual combat; trait-driven character variation
- **Modding:** Steam Workshop XML + C# DLLs (very accessible API)
- **Precedents:** Star Wars KOTOR, TiberiumRim, Rim-Effect, Call of Cthulhu — full TC into entirely different genres
- **Adjacency:** trait/role injection paradigm loosely maps to Reincarnated trait surface. Loop mismatch (colony sim vs ARPG).
- **Speculative inclusion** based on demonstrated TC flexibility.

#### Rank 7 — Baldur's Gate 3 (Larian, 2023)
- **Combat KPIs:** D&D 5e turn-based tactical; class/subclass system; action economy
- **Modding:** BG3 Script Extender + official mod manager (added late 2024); 9th most-modded on Nexus
- **Precedents:** Class/subclass injection is dominant mod type
- **Critical mismatch:** Real-time vs turn-based fundamental architectural divide
- **Wave 2A research in flight.**

#### Rank 8 — Elden Ring (FromSoftware, 2022)
- **Combat KPIs:** action; character-skill-execution > build-deep
- **Modding:** Mod Engine 2 + Elden Mod Loader + Nexus
- **Precedents:** The Convergence mod (new spells, weapons, areas, enemies); ER Reforged
- **Adjacency concern:** Souls audience expects punishing action, not procedural ARPG class gen. Class system is bespoke (Souls "class" is just starting equipment).
- **Volatility:** Shadow of the Erdtree DLC (2024) disrupted mod compatibility; stabilized by early 2025.

#### Rank 9 — Dark Souls 3 (FromSoftware, 2016)
- Same audience concerns as Elden Ring; more mature toolchain
- Cinders (Feb 2025), Archthrones (Mar 2025) — actively maintained TCs

#### Rank 10 — Crusader Kings 3 (Paradox, 2020) — speculative wildcard
- **Trait/event system deepest character-attribute injection pipeline in any strategy game**
- Reincarnated's spirit-swap design has structural parallel in CK3's dynasty/trait engine
- Elder Kings 2 (TES TC) proves cross-genre transplant possible
- **Profound core-loop mismatch** — dynasty management ≠ real-time combat
- Viability depends on whether Reincarnated can be expressed as narrative/event gameplay

#### Rank 11 — Mount & Blade II: Bannerlord
- Vibrant TC scene but sandbox combat ≠ ARPG dungeon-crawl. Low audience overlap.

#### Rank 12 — V Rising (Stunlock Studios, 2022)
- **MECHANICAL RESONANCE** with Reincarnated: vampire boss-hunt-for-powers loop parallels Reincarnated's boss-gallery + form-library
- Bloodcraft mod proves class/leveling/professions/familiars/perk-tree injection via BepInEx
- Community smaller than top-tier; Thunderstore discovery lower than Nexus

#### Ranks 13-15 — TL2 SynergiesMOD platform / D2 Median XL / Starfield
- TL2 SynergiesMOD: investigate as nested-host
- D2 Median XL: archaic MPQ pipeline; D2R excluded
- Starfield: Creation Kit (official, 2024) + Star Wars Genesis TC proven; sci-fi genre wrong

### § 5.4 — Knowledge gaps from survey (queued for Wave 2 or later)

1. SynergiesMOD openness to third-party class additions (Wave 2A — TL2 deep-dive)
2. Titan Quest AE concurrent player counts 2025-2026 (Steam Charts check pending)
3. Grim Dawn v1.2 modding compatibility status (verify before Track-F commitment)
4. BG3 Script Extender procedural stat generation depth (Wave 2A — BG3 deep-dive)
5. Project Diablo 2 third-party class loader status
6. Avowed official modding announcement (revisit 6-12mo)
7. V Rising Bloodcraft mod license / openness (could serve as nested platform)

---

## § 6 — Modding-fit scoring matrix

### § 6.1 — Methodology (revisable per gandalf wisdom + hive mandate)

For each target, score on **4 axes** (1–5 scale):

| Axis | What it measures | 5 = best | 1 = worst |
|---|---|---|---|
| **KPI compatibility** | Does the host model fights similarly to Reincarnated? Similar = lower translation overhead in mechanical math | Identical patterns (damage formula, geometry types, distance bands) | Fundamentally different paradigm (e.g., turn-based vs real-time) |
| **Schema compatibility** | Does Reincarnated's JSON output map cleanly to host's required input schema? | One-to-one field translation, no missing fields | Reincarnated lacks data host requires; cannot author mod without source-engine work |
| **Pipeline accessibility** | Can a human or automated exporter actually publish content to this host? | Steam Workshop + free SDK + script-friendly file formats | No modding pipeline; binary-only; source code required |
| **Community vitality** | Is there an audience for the published mod? | Vibrant 100k+ player active modding scene | Dormant or zero player base |

**Weighting** (revisable):
- KPI compatibility: 20%
- Schema compatibility: 35% *(highest — this is the actual translation overhead)*
- Pipeline accessibility: 30% *(elevated from initial 25% — accessibility is what determines feasibility)*
- Community vitality: 15%

**Modding Fit Score (MFS)** = weighted average, max 5.0.

**Decision bands:**
- MFS ≥ 4.0: **Recommended primary mod target** — ship-here-first candidate
- MFS 3.0–3.9: **Viable secondary** — worth considering, with caveats
- MFS 2.0–2.9: **Niche / proof-of-concept only** — significant translation cost vs. limited audience
- MFS < 2.0: **Not viable** — either platform-dead or technically intractable

**Methodology revision triggers** (per Matt's mandate to revise if questions don't get to goal):
- If MFS top-ranked candidate is commercially impotent (e.g., dead platform), re-weight community-vitality up
- If MFS top-ranked candidate requires fundamental engine work (R3+) that defeats the "quick modding capability" goal, re-weight schema-compatibility up
- If multiple candidates tie at high MFS, introduce **5th axis: Pipeline maturity** (how stable / patch-resistant is the modding stack)

### § 6.2 — Preliminary scoring (original 4 comparators only — pre Wave-2 expansion)

| Target | KPI compat | Schema compat | Pipeline access | Community | **MFS** | Recommendation |
|---|---|---|---|---|---|---|
| **Grim Dawn** | **3** (simple FSM AI is below our complexity; per-skill range published; spatial substrate present) | **4** (DBR template system maps cleanly to our mastery/class/skill/monster/gear schemas — verified via Dawn of Masteries 53-class mod precedent) | **5** (Crate ships full toolset; Asset Manager + DB Editor + World Editor + Lua; clean DBR format) | **4** (Vibrant 10+ yr ecosystem; Fangs of Asterkarn sustains long-tail; NexusMods + forum active) | **4.05** | **Primary recommended target** |
| Dragon's Dogma 2 | 2 (full 3D physics; climb-the-monster; goal-based learning AI — much richer than ours) | 2 (no system-level injection; SkillMaker is recombination only; no class/skill/monster injection at content level) | 3 (REFramework Lua is accessible but ceiling-bounded; periodic patch-breakage) | 3 (active ~1100 Nexus mods but narrow capability ceiling) | **2.50** | **Niche only — best framed as "engine-as-design-input tool"** |
| **Wolcen** | 3 (Kythera BT AI is more sophisticated; per-skill range internal-only; spatial substrate present) | 1 (XML-only; cannot mod Gate of Fates, AI behaviors, skill animations; no path to inject mastery/class equivalents) | 2 (CryEngine .PAK encrypted; no Workshop; file-replacement Umbra folders; no tool support) | 1 (Dormant ~24 avg concurrent; last patch Jul 2023; multiplayer shut down Sept 2024) | **1.65** | **Not viable — platform end-of-life** |
| ARPG baseline (D2/3/4/PoE/LE) | — | — | 1 (none have official modding open enough for content injection; D2R community mods exist but on weak legal footing) | — | **<2.0** | **Not viable as mod targets — value is as design reference** |

### § 6.3 — Comprehensive scoring (15 candidates — REFINED after Wave 2A returns)

**Scoring rubric (1–5):**
- **KPI**: spatial substrate similarity, geometry-system parity, range/AOE/AI pattern match, balance methodology fit
- **Schema**: how cleanly does Reincarnated JSON map to host's content schema (1 = lacks data; 5 = direct 1:1)
- **Pipeline**: official tools / SDK quality, distribution channel, mod-merging ease, learning curve
- **Community**: 2024-2026 active modder base, reachable audience, mod-creator engagement
- **Weights:** KPI 20% / Schema 35% / Pipeline 30% / Community 15%

| Rank | Target | KPI | Schema | Pipeline | Comm | **MFS** | Tier |
|---|---|---|---|---|---|---|---|
| 1 | **Grim Dawn** | 3 | 4 | 5 | 4 | **4.05** | **PRIMARY** |
| 2 | **Titan Quest AE** | 4 | 3.5 | 3.5 | 2.5 | **3.275** | **Secondary (revised down from 3.85)** |
| 3 | Torchlight 2 | 4 | 3.5 | 4 | 2 | **3.525** | Secondary (revised up from 3.50) |
| 4 | Terraria/tModLoader | 2 | 2 | 5 | 4 | **3.20** | Secondary (compile-time-only + presentation mismatch) |
| 5 | Minecraft/Forge | 2 | 2 | 4 | 5 | **2.85** | Audience-play; deep aesthetic translation |
| 6 | Rimworld | 1 | 2 | 4 | 4 | **2.50** | Loop mismatch; speculative |
| 7 | Baldur's Gate 3 | 1 | 1.5 | 3.5 | 5 | **2.525** | Refined: pipeline+community stronger, mechanical fit weaker — net tier unchanged (Niche) |
| 8 | Elden Ring | 2 | 2 | 3 | 5 | **2.65** | Souls audience; not class-deep |
| 9 | Dark Souls 3 | 2 | 2 | 3 | 4 | **2.50** | Same as ER, smaller community |
| 10 | Crusader Kings 3 | 1 | 1 | 4 | 4 | **2.20** | Trait/event interesting, but combat loop missing |
| 11 | Bannerlord | 1 | 1 | 4 | 4 | **2.20** | Sandbox not ARPG |
| 12 | V Rising | 2 | 2 | 3 | 3 | **2.40** | Mechanical resonance but small audience |
| 13 | TL2 SynergiesMOD nest | (= TL2 path) | — | — | — | — | Investigate via TL2 path |
| 14 | D2 Median XL | 4 | 3 | 1 | 3 | **2.70** | Archaic pipeline penalty |
| 15 | Starfield | 1 | 2 | 4 | 4 | **2.45** | Genre wrong |
| (4-set ref) | Dragon's Dogma 2 | 2 | 2 | 3 | 3 | **2.50** | (Director-rec; recombination only) |
| (4-set ref) | Wolcen | 3 | 1 | 2 | 1 | **1.65** | (Director-rec; platform end-of-life) |

### § 6.4 — Decision tiers (REFINED after Wave 2A)

**Tier 1 — PRIMARY target (MFS ≥ 4.0):**
1. **Grim Dawn (4.05)** — proven 53-class mod precedent, full toolset, vibrant community. **Sole primary target.**

**Tier 2 — SECONDARY targets (MFS 3.0–3.99) — viable with caveats:**
2. **Torchlight 2 (3.525)** — Wave 2A revealed DAT text format directly editable (no GUTS required at authoring time); 10-mod simultaneous limit better than GD/TQ's 1-mod-at-a-time; Steam Workshop auto-sync. SynergiesMOD has NO license for third-party building on top (drops SynergiesMOD-nest option). Community small (~250 daily concurrent) but stable. **Realistic reach: hundreds to low-thousands of active players per mod.**
3. **Titan Quest AE (3.275)** — Wave 2A revealed significant UI authoring overhead (8+ DBR files + art assets per mastery), affix library structural mismatch with Reincarnated's rolled_effects model, community smaller than initially scored (~742 avg concurrent May 2026). **Mastery system is structurally identical to Grim Dawn (Crate-Iron-Lore lineage confirmed), so the cross-porting leverage holds engineering-wise — but the audience reach is smaller than expected.** Still a real Phase-2 candidate but the "killer pairing" framing is softened.
4. **Terraria/tModLoader (3.20)** — Wave 2A confirmed compile-time-only constraint is real (no runtime JSON); per-season cadence requires weekly rebuild + Workshop push OR kRPG-style pre-allocated-slot ModConfig workaround (unvalidated). Calamity at 9.18M subscribers demonstrates pipeline maturity. 2D side-scroller art re-authoring required.

**Tier 3 — SPECULATIVE / niche (MFS 2.0–2.9):**
- Minecraft Forge (audience play; deep aesthetic translation)
- Elden Ring / DS3 (huge audience; not class-deep; Souls vocabulary mismatch)
- Rimworld (loop mismatch but vibrant ecosystem)
- V Rising (mechanical resonance worth investigating)
- D2 Median XL (genre match but archaic pipeline)
- DD2 (recombination only; sub-genre mismatch)

**Tier 4 — NOT VIABLE (MFS < 2.0):**
- Wolcen (platform end-of-life)
- BG3 (architecture mismatch; subclass-only)
- Others below threshold

### § 6.5 — Reframed recommendation under expanded data

**The Grim Dawn + Titan Quest AE pairing is the killer finding.** Both target the same mastery-system architecture; cross-porting is established practice; combined audience and credibility doubles the reach of single-target investment. **This was not in scope of the Director's three named recommendations.**

**Revised mod-first recommendation:**
1. **Phase 1 — Grim Dawn primary** (Track F R1 + R3-subset + Grim Dawn DBR exporter, ~7–9 weeks)
2. **Phase 2 — TQAE secondary** (TQAE ARC exporter adapter, leveraging the GD work, +~2–3 weeks). Demonstrates portability across mastery-system hosts.
3. **Phase 3 — Tier 2 expansion** (Torchlight 2 SynergiesMOD nest OR Terraria/tModLoader pivot if 2D side-scroller is acceptable presentation), evaluated based on Phase-1+2 results

**Phase-1+2 combined: ~10–12 weeks** of focused mod-export work, reaching the two mastery-system ARPG hosts with the largest established modder communities. **This is the engineering-leverage discovery the database makes possible.**

---

## § 7 — Updates log

- **2026-05-18 late evening (initial)** — File created. Scaffolding + § 0 methodology + § 1 KPI schema + § 2 Reincarnated producer profile preliminary + § 3 modding interface schema + § 4 original 4 comparators populated from existing research. § 5 / § 6 / § 7 await Wave 1 + Wave 2 research returns.

---

*Database opens 2026-05-18 evening. Will close when all waves return and scoring is complete. Mithrandir works through the night.*
