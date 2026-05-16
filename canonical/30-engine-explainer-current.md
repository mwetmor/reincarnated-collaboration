# 30 — Reincarnated Engine Explainer: Current State (post-demo1 v1.2 ship)

**Captured:** 2026-05-11
**Status:** Snapshot of the engine as it exists today, post demo1 v1.2 ship. Known issues + limitations cited inline with cross-references to file 28 (engine queue).

This document describes **Engine 1 (Content Generation Engine)** as currently implemented. Engine 2 (World Generation Engine) per file 29 has not been started; demo1 served as a minimum-viable Engine 2 prototype with a much simpler "level structure" than the eventual town+acts+dungeons.

---

## TL;DR

The engine generates one season of ARPG content — classes, abilities, monsters, trial bosses, gear — by combining:

1. **Deterministic anchor selection** from a 130-entry place library (e.g., "The Deep Trench," "The Cathedral of Bone")
2. **LLM-driven element flavor substitution** (canonical fire/water/earth/wind → seasonal variants like pitch/brine/bone)
3. **Dimensional class generation** along axes of element, energy type, range profile, role orientation, and armor weight; archetype derived post-hoc
4. **Per-class skill generation** sampling geometry + element + role from archetype-allowed combinations
5. **Convergence balance loop** that runs each class against the gauntlet at multiple `damage_modifier` values, finding the modifier that produces ~50% win rate (with gear sampled at 75th percentile per fight)
6. **Multi-stage naming pipeline** cascading from anchor → elements → archetypes → classes → skills → monsters → trial → gear

Output: a JSON packet per season at `/exports/season_NNN/*.json` containing classes, monsters, gear pool, metadata, and supporting documentation.

Current cost per season: **~$0.87 in LLM calls** (verified across 5 production seasons 1001-1005). Balance loop convergence takes ~3-5 minutes per season on commodity hardware.

---

## Level 1: System overview

### The generation pipeline

```
Seed + Config
    ↓
[Anchor Selection]  ──→  130-entry place library; deterministic from seed + history
    ↓
[Element Flavors]   ──→  LLM substitutes 4 canonical elements with seasonal variants
    ↓
[Class Generation]  ──→  Dimensional sampling; 8-10 playable + 2 act-bosses
    ↓
[Skill Generation]  ──→  Per-class kit (typically 5-6 skills); geometry × element × role
    ↓
[Stat Calibration]  ──→  Stat templates per archetype; values set at class build
    ↓
[Balance Loop]      ──→  Convergence finds damage_modifier per class (50% win rate)
    ↓
[Monster Pool]      ──→  Per-tier generation; trash/standard/elite/mini-boss/boss
    ↓
[Gear Pool]         ──→  200 items per season across 5 tiers (common-legendary)
    ↓
[Naming Pipeline]   ──→  LLM cascades names: classes, skills, monsters, gear
    ↓
[Telemetry/Export]  ──→  SQLite recording; JSON packet output
```

### The simulation layer

Used by the balance loop during generation, and as the in-engine combat math:

```
Combatant state (HP, resource, gear, active effects)
    ↓
Action selection (skill choice OR auto-attack fallback)
    ↓
Damage resolution (hit/crit/dodge → magnitude → armor → shield → HP)
    ↓
Status effect application (ailments → active_effects)
    ↓
Tick (cooldowns, regen, DoT, durations)
    ↓
Outcome (win/lose/continue)
```

### Telemetry

- SQLite database records generation runs, LLM calls, convergence metrics
- One DB per project (single-writer; parallel-batch generation causes lock contention)
- Captures all generation decisions for replay + audit

---

## Level 2: Pipeline stages in detail

### Stage 1 — Seasonal foundation (anchor + element flavors)

**Anchor selection.** The engine maintains a curated library of 130 "place anchors" — short evocative phrases describing locations. Examples: "The Deep Trench," "The Cathedral of Bone," "The Throne Room of the Mad King." Anchors fall into categories (water_places, underworlds_and_below, cathedrals_and_temples, specialized_and_archetypal, ruins_and_forgotten_places).

Selection is **deterministic from seed + season history**. The seed determines candidate ranking; history prevents recent-season repeats. No LLM call — this is library lookup.

**Element flavor substitution.** The engine has 4 canonical elements: fire / water / earth / wind. (Plus `physical` as a non-elemental damage type, and `hybrid` for mixed-element classes.) Each season substitutes these with thematically-flavored variants drawn from a 147-entry element pool.

Example for season 1001 (anchor: "The Deep Trench"):
- fire → pitch (black, viscous, adhesive)
- wind → thrum (deep, vibrating, resonant)
- water → brine (salt, bitter, preserving)
- earth → basalt (black, volcanic, dense)

This substitution is **LLM-driven**. The LLM receives the anchor + description and proposes element flavors that thematically fit. Currently no quality filter on the output (see file 28 D1 for the known issue with `milk` / `thrum` etc.).

### Stage 2 — Class generation (dimensional architecture)

The engine generates classes by dimensional composition along these axes:

| Axis | Values |
|---|---|
| `dominant_element` | fire / water / earth / wind / physical / hybrid |
| `energy_type` | mana / rage / combo / focus / stamina-as-resource |
| `range_profile` | close / medium / long |
| `role_orientation` | damage / control / hybrid (support gated to multi-actor contexts) |
| `armor_weight` | light / medium / heavy (implicit) |

The **validity matrix** constrains which combinations are allowed. Example constraints:
- `physical × combo × damage` produces "rogue" archetype (combo physical = build/spend rhythm doesn't fit control or hybrid)
- `physical × focus × damage` produces "hunter" (focus physical = long-range precision, doesn't compose with control or hybrid)
- `physical × rage × damage|control|hybrid` produces "physical_warrior|grappler|skirmisher" (rage is flexible)
- `fire × mana × control` produces "fire_controller" (silence + burn debuff identity)
- ... etc.

After dimensional sampling, an **archetype_tag** is derived post-hoc by `archetype_classifier.py` based on `(element, energy_type, role_orientation)` lookup. Known archetypes:

`fire_mage, water_mage, earth_caster, wind_caster, hybrid_mage, fire_controller, water_controller, earth_controller, wind_controller, hunter, physical_warrior, physical_grappler, physical_skirmisher, rogue` + monster archetypes (`brute, caster, controller, sniper, swarmer, tank`).

Total ~10 playable classes + 2 act-bosses per season. Act-bosses use `INTENTIONAL_OUTLIER` convergence mode (one undertuned ~40% win rate, one overtuned ~60% for harder/easier feel).

### Stage 3 — Skill generation (per-class kit)

Each class receives a kit of 5-6 skills built from role-based templates:

| Skill role | Purpose | Geometry typically |
|---|---|---|
| `primary_attack` | Spam ability; low cost, low cooldown | projectile, melee_strike, single_target |
| `burst_damage` | High-damage spender; high cost, mid cooldown | projectile, single_target, ground_slam |
| `area_damage` | AOE clear; mid cost, mid cooldown | circle, cone, ground_targeted_circle |
| `damage_over_time` | Sustained pressure; mid cost, mid cooldown | aura, totem, beam_channel |
| `defensive` | Survival; varies | self_buff, self_cast, shield |
| Optional `utility` / `control` | Class-specific | varies |

For each slot, the generator samples:
- **Geometry** from archetype-allowed options (e.g., hunter prefers ranged_physical; warrior prefers melee)
- **Element** typically class's dominant (no element diversification within kit — see file 28 B6 for known limitation)
- **Effects** mechanical effect mix (damage / heal / status / buff)
- **Energy cost + cooldown** sampled from role-appropriate ranges

**Known limitation:** the current generator samples each slot independently. Multiple slots within a class can share the same `(geometry, element, role)` combination, producing functional redundancy that the LLM naming layer then has to disambiguate. See file 28 B6 reframing.

### Stage 4 — Stat calibration

Each archetype has stat templates per axis (str / dex / int / wis / vit). Example values:

| Archetype | str | dex | int | wis | vit |
|---|---|---|---|---|---|
| fire_mage | 20 | 30 | 120 | 80 | 50 |
| hunter | 60 | 130 | 30 | 40 | 60 |
| physical_warrior | 130 | 40 | 10 | 20 | 100 |
| physical_grappler | 120 | 20 | 15 | 15 | 110 |
| physical_skirmisher | 100 | 100 | 20 | 30 | 50 |

(Exact values vary by version; canonical values in `class_templates.py`)

Stats determine derived combat values:
- `max_hp = 1000 + vit × HP_PER_VIT` (HP_PER_VIT ≈ 50)
- `max_mana = base_mana_for_archetype(energy_type)` (mana=120, focus=100, etc.)
- `crit_chance = base + dex × CRIT_PER_DEX` (capped at 0.75)
- `dodge_chance = base + dex × DODGE_PER_DEX` (capped at 0.60)
- Resource regen rate scales with int/wis depending on energy_type
- Damage scales with the relevant attribute (str for physical, int for magical)

### Stage 5 — Convergence balance loop

The balance loop is the engine's mechanical-correctness gate. Each class is evaluated against a fixed gauntlet of monsters, and a `damage_modifier` (per-class scaling coefficient) is found that produces ~50% win rate.

Procedure:
```
For each class:
  Initialize damage_modifier = 1.0
  Loop until convergence OR max iterations:
    Run N fights (typically 100-200) against gauntlet
    For each fight:
      Construct fresh combatant with class stats
      Sample gear loadout at GEAR_PERCENTILE = 0.75 (75th percentile gear quality)
      Run sim until win/lose
    Measure win rate
    If win_rate > TARGET + tolerance: damage_modifier *= 0.9 (binary search down)
    If win_rate < TARGET - tolerance: damage_modifier *= 1.1 (binary search up)
    If convergence (win_rate within tolerance of 0.50): break
  Record final damage_modifier
```

Constants:
- `TARGET = 0.50` (50% win rate)
- `GEAR_PERCENTILE = 0.75` (gear sampling baseline)
- `BALANCE_LOOP_MIN = 0.05` (modifier floor; below this rejects class)
- `BALANCE_LOOP_MAX = 1.94` (modifier ceiling; above this rejects class)

Observed result range: hunter classes spread 0.05-1.66× modifier (bimodal — see file 28's analysis of why this is a sign of insufficient kit composition variety).

### Stage 6 — Monster pool generation

Monsters are generated per-tier:

| Tier | HP scale | Damage scale | AI tier | Role in gauntlet |
|---|---|---|---|---|
| trash | 0.3× | 0.4× | simple | Warmup; 3-4 per Wave 1 |
| standard | 1.0× | 1.0× | simple | Wave 2 baseline |
| elite | 2.0× | 1.5× | smart | Wave 3 escalation |
| mini-boss | 4.0× | 2.0× | smart | Wave 4 |
| boss | 8.0× | 3.0× | optimal | Wave 5 |
| act-boss | 10×+ | 3.5× | optimal | Waves 6-7 (separate from monster pool; uses class generation) |

Each tier has multiple monster archetypes (`brute, caster, controller, sniper, swarmer, tank`) with role-appropriate abilities.

Monsters use **infinite resource** (cooldown-limited, not mana-limited) — separates monster instinctive combat from player tactical resource management.

### Stage 7 — Gear pool generation

200 items per season distributed across 5 tiers:
- 40 common
- 40 uncommon  
- 40 rare
- 40 epic
- 40 legendary

Each item carries:
- `gear_id` (unique)
- `slot` (weapon / armor / off_hand / accessory)
- `handedness` (1h / 2h)
- `tier` (common-legendary)
- `dominant_element`
- `power_score` (raw balance budget; higher = stronger)
- `fit_energy_type` / `fit_range_profile` / `fit_role_orientation` (multipliers, 0.0-1.0)
- `color_value`, `color_palette`, `color_signature` (visual)
- `name`, `flavor_text`, `visual_prompt` (LLM)
- `stat_requirements` (optional)

**No explicit stat fields.** Mechanical impact is computed via `fit_for_class()` × `power_score` at equip time. Geometric mean of fit scores × power_score gives effective stat contribution.

**Known limitation (file 28 B5):** legendaries have no `granted_ability`, `aura`, or `on_hit` fields. ARPG-genre-defining "Legendary Power" mechanic is not shipped despite being in Priority 02 design intent.

### Stage 8 — Naming pipeline (LLM cascade)

The naming pipeline produces names at multiple levels, each cascading from prior layers:

1. **Anchor** — library lookup (no LLM)
2. **Element flavors** — 1 LLM call per season (4 elements + their tags)
3. **Archetype mood** — 1 LLM call per season (sets tonal palette for classes)
4. **Class names** — 1 LLM call per class (~10 calls per season)
5. **Skill names** — 1 LLM call per skill (~50-60 calls per season)
6. **Monster names** — 1 LLM call per monster (~35-50 calls per season)
7. **Trial / act-boss flavor** — ~5-10 LLM calls per season
8. **Gear names** — variable; legendaries get rich LLM treatment; lower tiers may use templates

Each call receives parent-layer context. Example: skill naming prompt receives the class's name + flavor text + the skill's geometry/element/role, then asks for a thematically-fitting name.

**Known limitations:**
- Skill name collisions ~40% per season (file 28 D2 — superseded reframe: caused by insufficient kit composition variety; LLM gets same inputs for multiple slots)
- Element naming quality variance (file 28 D1 — `milk`, `thrum` produce weird LLM downstream output)
- Anchor selector duplicate detection fails under DB write contention (file 28 D3)
- Occasional unnamed class (file 28 D4)

### Stage 9 — Telemetry + persistence

All generation decisions recorded to SQLite:
- Anchor selected + history
- Element flavors + LLM call cost
- Per-class stats / skills / archetype tag / final damage_modifier
- Per-monster tier / archetype / abilities
- Gear pool composition
- Naming-pipeline LLM call records (input, output, model, tokens)
- Convergence iteration counts + win-rate trajectories

**Known issue (Phase 1 finding):** SQLite single-writer contention. Parallel-batch generation against one DB produces lock contention and partial writes. Sequential generation is the supported pattern (~21 min for 5 seasons vs ~43 min parallel-with-throttling, plus parallel can lose telemetry).

---

## Level 3: Math, code, iteration procedures

### Combat damage formula (per `damage_resolver.py`)

For a damage-effect skill striking a target:

```python
magnitude = skill.base_magnitude * attacker.damage_modifier
magnitude += attacker.bonus_damage_flat  # gear contribution

# Hit roll
if did_hit(attacker.accuracy, defender.dodge_chance, rng):
    # Damage type: physical or elemental
    if skill.damage_type == 'physical':
        # Percentage armor formula (K = 3000)
        damage = compute_physical_damage(magnitude, attacker_str, defender.armor)
        # = magnitude * (1 + str_modifier) * (1 - armor / (armor + K))
    else:
        # Elemental
        damage = compute_elemental_damage(magnitude, attacker_int_or_wis, defender.resistance)
    
    # Crit roll
    if did_crit(attacker.crit_chance, DEFAULT_CRIT_RESISTANCE, rng):
        damage = apply_crit(damage)  # base × CRIT_MULTIPLIER
        bonus = attacker.ability_modifiers.get("crit_bonus_damage", 0.0)
        damage += damage * bonus
    
    # Shield absorbs first
    damage = defender.absorb_with_shield(damage)
    defender.hp -= damage
```

Constants (per `math_model.py` and `_ENERGY_CONFIGS`):
- `K_ARMOR = 3000` — percentage armor formula constant
- `CRIT_MULTIPLIER = 2.0` (base; modifiable per class)
- `DEFAULT_CRIT_RESISTANCE = 0.0`
- `BASE_AILMENT_CHANCE = 0.35` — every ailment application roll
- `CRIT_CHANCE_CAP = 0.75`
- `DODGE_CHANCE_CAP = 0.60`

### Resource regen formulas

```python
# Per actor type, regen per second:

# mana / int-or-wis-scaled:
mana_regen = MANA_REGEN_BASE * (1.0 + max(int, wis) * 0.002)  # MANA_REGEN_BASE = 5.0

# stamina-as-resource (vit-scaled, flat baseline):
stamina_regen = STAMINA_REGEN  # = 20.0 (flat)

# focus (passive decay):
focus_regen = -FOCUS_DECAY  # = -5.0 (negative; clamps to 0 floor)
# Plus +10 per skill cast (engine FOCUS_RESTORE_PER_SKILL = 10.0)

# rage (no passive regen; on-hit accumulation):
# On hit dealt: +RAGE_PER_HIT_DEALT = 10.0
# On hit taken: +RAGE_PER_HIT_TAKEN = 5.0

# combo (no passive; on-primary accumulation):
# On primary_attack use: +COMBO_BUILD_PER_PRIMARY = 1.0
# Pool max: 5 (file 28 A1 — generator emits costs > pool size; demo overrides)
```

### Status effect: chill slow_factor

```python
# combatant.py:163-170
@property
def slow_factor(self) -> float:
    factor = 1.0
    for e in self.active_effects:
        if e.name == "chill":
            factor *= (1.0 - e.params.get("slow_percent", 0.0))
    return max(0.1, factor)  # floor at 90% slow
```

Engine applies to cast time: `cast_time /= slow_factor`. Demo Phase 8.0.2+ applies to movement velocity.

### Lifesteal mechanic

```python
# damage_resolver.py:150-160
elif name == "lifesteal":
    if total_damage > 0:
        pct = float(effect.params.get("percent", 0.0))  # 0.09-0.12 in JSON
        stolen = min(total_damage * pct, attacker.max_hp - attacker.hp)
        if stolen > 0:
            attacker.hp += stolen
```

### Shield mechanic (flat magnitude, no scaling)

```python
# On cast (damage_resolver.py:109-116):
elif name == "shield":
    magnitude = float(effect.params.get("magnitude", 0.0))  # flat from JSON; always 1000 currently
    duration = float(effect.params.get("duration_seconds", 5.0))
    attacker.active_effects.append(ActiveEffect(name="shield",
        params={"magnitude": magnitude}, duration_remaining=duration))

# On incoming damage (combatant.py:183-196):
def absorb_with_shield(self, damage: float) -> float:
    remaining = damage
    for effect in self.active_effects:
        if effect.name == "shield" and remaining > 0:
            mag = effect.params.get("magnitude", 0.0)
            absorbed = min(mag, remaining)
            effect.params["magnitude"] = mag - absorbed
            remaining -= absorbed
    self.active_effects = [e for e in self.active_effects
        if e.name != "shield" or e.params.get("magnitude", 0.0) > 0]
    return remaining  # unabsorbed damage continues to HP
```

**Known issue (file 28 A4):** shield magnitude is flat 1000 from JSON; no WIS or damage_modifier scaling. Asymmetric with heal (which scales `× (1 + wisdom × 0.002)`).

### Direct heal formula

```python
# damage_resolver.py:104
elif name == "heal":
    magnitude = float(effect.params.get("magnitude", 0.0))
    heal_bonus = 1.0 + attacker.attribute_values.get("wisdom", 0) * 0.002
    healed = min(magnitude * heal_bonus, attacker.max_hp - attacker.hp)
    attacker.hp += healed
```

### Heal over time formula

```python
# damage_resolver.py:122
elif name == "heal_over_time":
    tick_heal = float(effect.params.get("tick_heal", 0.0)) * attacker.damage_modifier
    duration = float(effect.params.get("duration_seconds", 6.0))
    attacker.active_effects.append(ActiveEffect(name="heal_over_time",
        params={"tick_heal": tick_heal}, duration_remaining=duration))
```

### Auto-attack fallback (fight_engine.py:142-148, 193-212)

```python
# When choose_action() returns None (no skill castable):
if elapsed >= actor.action_available_at:
    _auto_attack(actor, target, rng)
    actor.action_available_at = elapsed + AUTO_ATTACK_INTERVAL

def _auto_attack(actor, target, rng):
    magnitude = AUTO_ATTACK_BASE * actor.damage_modifier  # AUTO_ATTACK_BASE = 375.0
    if did_hit(actor.accuracy, target.dodge_chance, rng):
        dmg = compute_physical_damage(magnitude, actor.strength, target.armor)
        if did_crit(actor.crit_chance, DEFAULT_CRIT_RESISTANCE, rng):
            dmg = apply_crit(dmg)
        dmg = target.absorb_with_shield(dmg)
        target.hp -= dmg
    _accumulate_energy_on_hit(actor, dmg, auto=True)  # rage classes: +5 (vs +10 normal)
    _accumulate_energy_on_hit_taken(target, dmg)
```

`AUTO_ATTACK_INTERVAL = 1.0` (once per second when triggered).
`AUTO_ATTACK_BASE = 375.0` (~0.15× tier-50 base of 2500 — "weak but overcomes typical armor").

### Convergence loop pseudocode

```python
def converge_class(cls, gauntlet, target_winrate=0.50, tolerance=0.05):
    modifier = 1.0
    history = []
    for iteration in range(MAX_ITERATIONS):
        wins, losses = run_batch_geared(cls, gauntlet, modifier, n_fights=100,
                                         gear_percentile=0.75)
        winrate = wins / (wins + losses)
        history.append((iteration, modifier, winrate))
        
        if abs(winrate - target_winrate) < tolerance:
            return modifier, history  # converged
        
        # Binary search (simplified)
        if winrate > target_winrate:
            modifier *= 0.9  # too strong
        else:
            modifier *= 1.1  # too weak
        
        # Hit floor or ceiling
        if modifier < BALANCE_LOOP_MIN or modifier > BALANCE_LOOP_MAX:
            return None, history  # reject class
    
    return None, history  # didn't converge in MAX_ITERATIONS
```

Convergence is fragile — observed modifier ranges 0.05-1.94 for hunters; bimodal distribution. **The current loop has no recourse if kit composition is wrong**; only path is to scale damage_modifier. (See file 28 B6 for the proposed shaped-balance refactor.)

### Gear sampling at 75th percentile

```python
def sample_scenario_loadout(catalog, class_stats, rng, stat_floors,
                             gear_percentile=GEAR_PERCENTILE):
    # GEAR_PERCENTILE = 0.75 — calibrated to "above-average gear" expected of player
    
    loadout = {}
    for slot in ('weapon', 'armor', 'off_hand', 'accessory'):
        # Filter items appropriate for class
        candidates = filter_by_class_fit(catalog[slot], class_stats)
        # Sort by power_score
        candidates.sort(key=lambda g: g.power_score)
        # Pick at 75th percentile
        idx = int(len(candidates) * gear_percentile)
        loadout[slot] = candidates[min(idx, len(candidates)-1)]
    
    return loadout
```

This is what `run_batch_geared()` calls per-fight. The damage_modifier produced by the convergence loop is CALIBRATED against this 75th-percentile baseline. Players with high gear rolls overshoot; with low rolls undershoot.

### Fit-for-class scoring (gear_schema.py)

For evaluating gear fit to a class:

```python
def fit_for_class(gear, class_dimensions):
    """Geometric mean of dimension-specific fit scores × power_score"""
    energy_fit = gear.fit_energy_type[class_dimensions.energy_type]
    range_fit = gear.fit_range_profile[class_dimensions.range_profile]
    role_fit = gear.fit_role_orientation[class_dimensions.role_orientation]
    
    # Geometric mean
    fit = (energy_fit * range_fit * role_fit) ** (1/3)
    
    # Combine with power_score
    return fit * gear.power_score
```

This is what Phase 5.5f's Spirit Guide ports to the demo — categorical signals (Strong / Solid / Marginal / Sidegrade / Downgrade) derived from this score relative to currently-equipped gear.

---

## Known limitations (cross-reference to file 28 engine queue)

The engine ships demo1 with documented limitations that will be addressed in post-demo1 engine work:

### Category A — Bug fixes (~3-5 hrs)
- **A1: Combo skill cost generator** — emits costs 13.7-30 against pool max 5. 12 of 24 combo skills uncastable without demo override.
- **A1b: Focus skill cost generator** — emits costs 7.9-35.3 against +10 restore. Focus classes net-lose energy per cast.
- **A2: Per-skill geometry dimensions** — no `range`, `half_angle`, `area_radius` in JSON. Demo applies 870px catch-all for non-melee.
- **A3: `damage_formula.md` doc audit** — 10 documented errors against actual code in `_ENERGY_CONFIGS`, `math_model.py`, `damage_resolver.py`.
- **A4: Shield magnitude scaling** — flat 1000 with no WIS or damage_modifier scaling.

### Category B — Balance tuning + architectural (varies)
- **B1: WIS-on-heal multiplier** — too gentle for stat investment to feel worthwhile (0.002 per WIS → 30% bonus at 151 WIS).
- **B2: Per-skill ailment chance scaling** — currently flat 0.35; design intent: scales with skill cost (high-cost = 100%, mid = 35%, low = <35%).
- **B3: AOE budget rebalancing** — class generation should weight AOE coverage per archetype.
- **B4: Swarm-tier monster generation** — engine doesn't model trash as swarm fodder; demo overrides stats client-side.
- **B5: Legendary gear abilities** — Priority 02 design intent (auras, on-hit, cast-on-attack) never shipped.
- **B6: Class kit composition with shaped-balance + Hierarchical Skill Tree** — primary balance dimension architectural upgrade. Kit composition becomes the balance lever; damage_modifier becomes fine-tune. Reduces 0.05-1.94 modifier range to ~0.85-1.15. Tree structure: 4 tiers × 2-4 chains; cross-chain unlock asymmetry per element distribution.
- **B7: Gear-percentile variance check** — pass/fail gate at multiple percentiles to catch pathological scaling. Demo1 surfaced hunter+legendaries example.
- **B9: Traits + skill point distribution + reset mechanism** — major architectural addition; introduces leveled traits, 120-point skill budget, 10-15 variable kit size, Spirit Guide-as-build-coach.
- **B10: Gauntlet restructure to ARPG genre density** — 7-wave linear → 10-12 room generated act; ~70% trash composition; ~80-100 mobs/min clear target; boss fights remain 1v1. Native swarm-tier monsters (replaces demo-side override). Per-band monster pools (separate flavor per A1/A2/A3 band).
- **B11: Geometry palette expansion (scope locked 2026-05-11)** — 16 → 25 active types via 9 new AOE-coded geometries (3 un-defer: whirlwind/dash_attack/leap_strike; 6 add-new: chain_lightning/ricochet_bounce/fork/vortex_pull/ring/multi_projectile) plus per-skill parameter expansions (collision_mode, angle_distribution, sweep_shape, damage_falloff). Active-discrete-AOE rises 7 → 16. Architecturally co-dependent with B6 + B10 + B7 — must ship as one coordinated sprint.
- **B12: Movement speed + boots + 10-slot gear audit** — engine emits `movement_speed` per class + monster tier; boots primary movement speed affix; +25% gear cap; adds gloves/belt/2-rings slots; gear resistance affixes must support +45% all-element across loadout.
- **B13: Active mobility + telegraphs + evasion + emergence observability** — 5 defensive mobility geometries (roll/defensive_dash/strafe_mode/blink/dodge_stance); palette 25 → 30 active types; engine `cast_time` + `i_frame_window` per skill; demo telegraphs + asymmetric indicator scaling (0.92× player / 1.08× enemy); engine archetype-emergence observability.
- **B14: Multi-band convergence simulator (Option β; 3-band L17/L33/L50)** — 9 convergence runs per class (6 kit+variance + 3 doppelganger validation). Per-band optimal distributions; recompose-first failure handling; per-band gauntlets. ~30-45 min/season cost.
- **B15: Seasonal Sets** — class-specific endgame sets, one per playable class per season; L50-only drops; 2-piece/4-piece/full-set bonuses; trophy value for Earth meta-layer form library.

### Category C — Architectural (deferred unless playtest demands)
- **C1: Multi-target dispatch in sim** — current engine 1v1; demo invented pack semantics client-side.
- **C2: Knockback consumer in sim** — engine has knockback stub; no positional consumer.
- **C3: Convergence-target reshaping for horde** — current binary 50% win rate; horde needs density-aware metrics.

### Category D — Content quality
- **D1: Seasonal element naming quality** — `milk`, `thrum` produce awkward LLM downstream. Design session needed.
- **D2: Class kit composition** — reframed; supersedes the skill-name dedup framing.
- **D3: Anchor selector duplicate detection** — failed under DB write contention.
- **D4: Unnamed class fix** — one observed in season 1002.

---

## Appendix: Key constants reference

| Constant | Value | Location |
|---|---|---|
| `K_ARMOR` | 3000 | math_model.py |
| `CRIT_MULTIPLIER` | 2.0 | math_model.py |
| `CRIT_CHANCE_CAP` | 0.75 | math_model.py |
| `DODGE_CHANCE_CAP` | 0.60 | math_model.py |
| `MANA_REGEN_BASE` | 5.0 | combatant.py `_ENERGY_CONFIGS` |
| `MANA_REGEN_INT_OR_WIS_SCALE` | 0.002 | math_model.py |
| `STAMINA_REGEN` | 20.0 | combatant.py |
| `FOCUS_DECAY` | -5.0/sec | combatant.py |
| `FOCUS_RESTORE_PER_SKILL` | 10.0 | combatant.py |
| `COMBO_POOL_MAX` | 5 | combatant.py |
| `COMBO_BUILD_PER_PRIMARY` | 1.0 | combatant.py |
| `RAGE_PER_HIT_DEALT` | 10.0 | combatant.py |
| `RAGE_PER_HIT_TAKEN` | 5.0 | combatant.py |
| `RAGE_PER_AUTO_ATTACK` | 5.0 | fight_engine.py |
| `BASE_AILMENT_CHANCE` | 0.35 | damage_resolver.py |
| `AUTO_ATTACK_INTERVAL` | 1.0 sec | fight_engine.py |
| `AUTO_ATTACK_BASE` | 375.0 | fight_engine.py |
| `GEAR_PERCENTILE` | 0.75 | balance_loop.py |
| `BALANCE_LOOP_MIN` | 0.05 | balance_loop.py |
| `BALANCE_LOOP_MAX` | 1.94 | balance_loop.py |
| `HEAL_WIS_SCALE` | 0.002 | damage_resolver.py |

## Appendix: Generation cost per season

- ~$0.87 in LLM calls (verified across seasons 1001-1005)
- ~3-5 minutes balance loop convergence on commodity hardware
- ~200 LLM calls per season cumulative across the naming pipeline
- ~$4.30 total LLM spend for the 5 production seasons demo1 ships against

## Cross-references

- **File 16:** project roadmap (tactical near-term; Track A staging A1-A7 + interleaved playtests)
- **File 24:** demo1 implementation spec (historical; demo1 v1.2 shipped)
- **File 28:** engine ARPG rebalance design (post-demo1 engine queue including B12/B13/B14/B15)
- **File 29:** Reincarnated architecture and game scope (strategic anchor)
- **File 31:** Engine explainer — future state (companion to this doc)
- **File 32:** Progression-system design (all 12 sections RESOLVED 2026-05-12)
- **File 33:** Progression skeleton (immutable + decided only)
- **Memory `project_engine_state_findings.md`** — recurring lessons learned + finding history
- **Memory `project_earth_meta_layer.md`** — Earth Self meta-layer design intent
- **Memory `project_pet_system.md`** — pet system design intent (deferred to focused later sprint)
- **Memory `project_design_intent.md`** — design pillars + decisions log
