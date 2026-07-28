# KIT-CAL-1 / G-5b — sim opposition census (READ-ONLY)

**Run:** KC1-2026-07-27 (charter `gandalf/notes/2026-07-27-kit-cal-1-run-charter.md`, conductor gandalf)
**Work-package:** G-5b — can the sim's opposition be PINNED to externally measured monster stats?
**Author:** gamora (simulation seam) · **Date:** 2026-07-28
**Mode:** survey / census. **No production code written.** All numbers below are MEASURED or CITED.
**Repo under census:** `/Users/admin/Games/reincarnated-engine/`

Probe scripts used (throwaway, `/tmp`, not banked): `/tmp/g5b_probe.py` (injection A/B + pack-proxy
reachability), `/tmp/g5b_probe2.py` (per-hit transfer function). Their outputs are quoted inline
under §2.3 / §3.4 so the note stands without them.

---

## §0 — Headline

**Injection question: YES — no engine code change.** A fight or batch can be run with fully
externally specified monster stats today, through the existing public entry points
`run_spatial_fight(scenario, class_dict, mob_dicts, ...)` and `SpatialFightEngine(scenario, player,
mobs, ...)`. The mob contract at the seam is a **plain Python dict**, not a generated `Monster`
object. There is already an in-tree precedent that pins a mob to *Grim Dawn* source values
(`tsf6_track_a_harness.py`, GD `zombie_a01`).

Two carve-outs, both on the **player** side, not the opposition side (§5):
- player `max_hp` is **derived**, not settable — `compute_max_hp(vit, str)` with a hard floor of
  10,000 HP;
- player **defensive** stats (armor / resists / block / dodge / crit) are hardcoded zeros on the
  projection path that the KF-4 kit compiler targets.

`pack_proxy_size == 0` on every default-config path (§4). The assertion is safe for G-5 pre-flight.

---

## §1 — Monster stat model: what a sim monster carries, and where it comes from

### 1.1 The two state objects

There are **two** representations of a monster in a live fight, and they are different objects:

| Object | File:line | Role |
|---|---|---|
| `SpatialEntity` | `simulation/spatial_gauntlet/spatial_engine.py:1046` | position / heading / HP / movement / skills / cooldowns / energy — the thing the 2D fight loop steps |
| `CombatantState` | `simulation/combatant.py:148` | the kernel resolver's attacker+defender surface — armor, `elemental_resistances`, crit, dodge, accuracy, `attribute_values`, `substrate` |

Each `SpatialEntity` carries a `combatant_state` reference. The fight loop moves and times the
`SpatialEntity`; every damage number is computed by `damage_resolver.resolve_skill` off the
`CombatantState` pair.

### 1.2 The fields a monster actually carries

`CombatantState` (`combatant.py:148-381`), monster-relevant subset:

- `hp` / `max_hp` (`:160-161`)
- `armor` (`:170`) — flat, mitigated as `armor/(armor+K)`, `K = ARMOR_MITIGATION_K = 3000.0`
  (`foundation/math_model.py:34,141`)
- `elemental_resistances: dict[str,float]` (`:171`) — per-element, clamped 0–0.95
- `crit_chance` / `dodge_chance` / `accuracy` / `status_resist` (`:172-175`)
- `attribute_values: dict[str,int]` (`:176`) — the damage-scaling stat pool
- `skill_states` (`:179`), `energy_type` + pool (`:183`, `mana`/`max_mana`/`mana_regen`)
- `movement_speed` (`:245`), `substrate` (`:266`)
- R3 AI block (`:200-215`): `preferred_behavior`, `aggro_radius_m`, `leash_distance_m`,
  `skill_rotation_priority`, `range_profile_redistribution`
- `pack_proxy_size: int = 0` (`:281`) — see §4

`SpatialEntity` (`spatial_engine.py:1046-1105`) monster-relevant subset: `spawn_x/y`, `x/y`,
`heading_rad`, `entity_radius`, `hp`/`max_hp`, `damage_modifier`, `movement_speed`, `skills`
(list of dicts), `skill_geometries`, `skill_cooldowns`, `skill_energy_costs`, `energy`/`max_energy`/
`energy_regen`/`energy_type`, `armor_factor`, plus the R3 AI block and `resolver_skills`.

**Size/geometry.** A monster's body is a single scalar: `entity_radius`, set from the scenario's
`SpawnSpec`, not from the monster. Defaults: `ENTITY_RADIUS_STANDARD = 0.5` m,
`ENTITY_RADIUS_BOSS = 1.5` m (`spatial_engine.py:114-115`). Soft collision only
(`SEPARATION_FORCE_CONSTANT = 2.0`, `SOFT_COLLISION_FRACTION = 0.8`, `:163-164`).

**There is no monster `level` field.** `monster_schema.Monster` (`generation/monster_schema.py:18`)
has no level. Difficulty is carried entirely by `threat_tier` ∈ {swarm, magic, trash, standard,
elite, mini-boss, boss}.

### 1.3 Where the numbers come from at fight time — three sources, all live

**(a) Generated bestiary (per-season JSON).** `generation/monster_generator.py` rolls HP/armor/skills
per tier:
- `CLASS_HP_REFERENCE = 20_000` (`:20`) — "average tier-50 class HP", the anchor for all monster HP
- `TIER_HP_FACTOR_RANGE` (`:32-40`), `TIER_ARMOR_FRACTION` (`:43-50`, fraction of `max_hp`),
  `TIER_SKILL_COUNT` (`:55-62`), `ARCHETYPE_MOVEMENT_SPEED` (`:84-91`)
Loaded as `Monster` objects → `combatant.from_monster()` (`combatant.py:1246`).

**(b) Per-tier constant table in the sim seam.** `TIER_EFFECTIVE_ATTRIBUTE`
(`combatant.py:66-75`) — the monster's stand-in for a stat budget, keyed by `threat_tier`:
swarm 7 / magic 20 / trash 40 / standard 60 / elite 100 / mini-boss 150 / boss 200 / trial 220.
It feeds `attribute_values` uniformly across all five stats. Its only damage effect is
`compute_damage_scaling(a) = 1 + a·0.005` (`math_model.py:113`), i.e. swarm ×1.035 … boss ×2.00.

**(c) Endgame spec profile.** `generation/endgame_mob_stat_profile.py`:
`ENDGAME_TIER_HP_FACTOR_RANGE` (`:113`), `ENDGAME_TIER_ARMOR_FRACTION` (`:135`),
`ENDGAME_MOB_PROFILES` (`:195`). This is the L45-50 regime the endgame-BC gauntlet consumes
(`t4_sim_cycling.py:1127 _synthetic_mob_dict_for_spatial`). It is ~9× the generic swarm HP.

**Runtime multipliers layered on top at fight setup** (`spatial_engine.py:6140-6163`):
`MOB_HP_DIFFICULTY_MULTIPLIER = 1.5` (`arena.py:49`) applied when
`scenario_id ∈ {open_arena, chokepoint_corridor}` (`arena.py:55`) **and**
`threat_tier ∈ {swarm, magic, elite}` (`arena.py:52`) **and** the caller leaves
`apply_mob_hp_difficulty_multiplier=True` (the default, `spatial_engine.py:5978`).

### 1.4 Where monster DAMAGE comes from

Two routes, selected per hit at `spatial_engine.py:4676-4682`:

- **TYPED route (production).** `_typed_death_route` = mob has a `combatant_state` **and** the player
  has one **and** `skill_idx` is index-aligned into `mob.resolver_skills`. Damage is
  `resolve_spatial_hit(attacker=mob, defender=player, ...)` → the same kernel
  `damage_resolver.resolve_skill` the player's offense uses. `PLAYER_ARMOR_FACTOR_*` is **inert** on
  this route.
- **FLAT fallback** (`:4752`), fires only when the mob carries no index-aligned resolver skill:
  `raw = skill.damage_multiplier × 300.0 × MOB_DAMAGE_SCALE` then `× (1 − player.armor_factor)`.
  `MOB_DAMAGE_SCALE = 0.40` (`spatial_engine.py:787`);
  `PLAYER_ARMOR_FACTOR_VS_STANDARD = 0.85`, `..._VS_BOSS = 0.95` (`:254-255`).

**Monster attack cadence** is `float(skill.get("cooldown_seconds", 2.0))`, written to both
`skill_cooldowns[idx]` and `action_available_at` at `spatial_engine.py:4830-4832`. There is no
separate attack-speed stat. Range gating is `skill["range_m"]` (default 2.0,
`spatial_engine.py:2243`); `range_m == 0.0` means self-cast.

**Magnitude → damage transfer (legacy flat-magnitude path, `damage_resolver.py:882-884`):**
```
magnitude = effect.params["magnitude"] × skill.damage_multiplier + attacker.bonus_damage_flat
magnitude *= buff_dmg_mult                      # = (1+buff_damage) × attacker.damage_modifier × (1+bonus_pct)   :816-820
magnitude *= geometry_multiplier                # neutralized to single_target on the spatial path
magnitude *= U[0.80, 1.20]                      # per-hit variance, :947-948 (_DMGVAR_LO/HI :578-579)
dmg = compute_{physical,elemental}(magnitude, scaling_stat, armor|resist)
```
`scaling_stat` is looked up by `skill.scaling_attribute` (`:815`). Monster JSON skills carry **no**
`scaling_attribute`, so the projection shim sets it `""` (`spatial_resolver_adapter.py:115-117`) →
`scaling_stat = 0` → **`TIER_EFFECTIVE_ATTRIBUTE` does not amplify a mob's spatial attack.** It
reaches the resolver only on the full-`Monster` path via `attribute_values`, and even there only if
the skill names a scaling attribute.

---

## §2 — The injection question: **YES, no engine code change**

### 2.1 The entry points, by name

| Level | Entry point | File:line | Mob input |
|---|---|---|---|
| Batch runner | `run_spatial_fight(scenario, class_dict, mob_dicts, n_fights, ...)` | `spatial_engine.py:5953` | `mob_dicts: list[dict]`, one per `scenario.mob_spawns` slot |
| Per-entity factory | `entity_from_monster_dict(monster_dict, spawn_spec, hp_multiplier=, armor_multiplier=, monster=None)` | `spatial_engine.py:5820` | plain dict |
| Engine constructor | `SpatialFightEngine(scenario, player, mobs, seed, session_id, ...)` | `spatial_engine.py:2613` | pre-built `SpatialEntity` list |

The `SpatialFightEngine` docstring states the contract outright: *"Caller is responsible for
providing pre-built SpatialEntity objects (created from class/monster JSON dicts)."*

`run_spatial_fight` asserts only `len(mob_dicts) == len(scenario.mob_spawns)`
(`spatial_engine.py:6049`). Nothing validates the dict against a `Monster` schema; nothing consults
the season bestiary; `monster=None` (the default) routes to
`combatant_projection_from_monster_dict` (`spatial_resolver_adapter.py:218`), which reads the dict
directly.

### 2.2 The externally-specifiable mob-dict schema (read sites, verbatim keys)

Read by `entity_from_monster_dict` (`spatial_engine.py:5844-5944`) and
`combatant_projection_from_monster_dict` (`spatial_resolver_adapter.py:218-251`):

| Key | Default | Consumer |
|---|---|---|
| `id` | *required* | entity id |
| `max_hp` | 1000.0 | `hp`, `max_hp` (× `hp_multiplier`) |
| `armor` | 0.0 | resolver mitigation |
| `elemental_resistances` | `{}` | resolver mitigation, per element |
| `dominant_element` | `"physical"` | `substrate` (resistance matrix) |
| `archetype_tag` | `""` | label only |
| `range_profile` | `"medium"` | preferred engagement distance |
| `energy_type` | `"mana"` | pool identity |
| `movement_speed` | 5.75 | m/s |
| `preferred_behavior` | `"melee_aggressive"` | AI behavior enum |
| `aggro_radius_m` | 8.0 | engagement gate |
| `leash_distance_m` | 18.0 | leash (SpawnSpec override wins) |
| `skill_rotation_priority` | `[]` | AI ordering |
| `range_profile_redistribution` | `None` | AI ordering |
| `skills` | `[]` | **the whole damage + cadence surface** |

Per-skill dict keys read (`spatial_engine.py:2243,2315,4830` +
`spatial_resolver_adapter._resolver_skill_from_dict:97-133`):
`id`, `role`, `geometry_type`, `canonical_element`, `damage_multiplier`, `cooldown_seconds`
(= attack cadence), `energy_cost`, `range_m`, `geometry_params`, `damage_scaling_type`,
`scaling_attribute`, and `effects: [{"name": "damage", "params": {"magnitude": …, "element": …}}]`.

**Pack size is externally specifiable too**, one level up: `ArenaScenario` /
`Arena` / `SpawnSpec` are plain dataclasses (`arena.py`) and a harness can construct a bespoke one —
arena dimensions, spawn count, spawn positions, per-spawn `threat_tier`, per-spawn leash override,
`max_duration_s`, `win_condition`. Existing precedent: `tsf6_track_a_harness.py:174` and `:267`.

### 2.3 In-tree precedents, including a GD one

1. **`spatial_gauntlet/tsf6_track_a_harness.py`** — pins a mob to **Grim Dawn `zombie_a01`**
   controller values from legolas's `.arz` extraction, via `_zombie_mob_dict()` (`:115-140`) and a
   hand-built `ArenaScenario` (`:174`, `:267`), driving `SpatialFightEngine` directly (`:215`). Its
   header states: *"builds NO new sim MECHANISM — it configures the existing SpatialFightEngine
   with GD's actual zombie_a01 controller parameters."* This is the exact shape G-5 needs.
2. **`t4_sim_cycling._synthetic_mob_dict_for_spatial`** (`:1127`) + `_run_spatial_w4g_batch`
   (`:1204`) — the endgame-BC gauntlet builds a synthetic mob dict and duplicates it across
   `scenario.mob_spawns` (`:1264`).
3. **`kit_compiler/smoke_kf4_compiler.py:72`** and **`smoke_kf5_expected_pct.py:51`** — hand-built
   mob walls at `max_hp` 2000 / 4000.

### 2.4 Empirically verified (probe `/tmp/g5b_probe.py`, scenario `open_arena_wall_diag`, 8 spawns, 3 fights, seed 90210, class `season_001010/class_0001`)

```
A_no_skills        wr=1.00 mobs_killed=8.00 elapsed=16.20s dmg_taken=[0.0, 0.0, 0.0]
B_injected_skill   wr=1.00 mobs_killed=8.00 elapsed=18.87s dmg_taken=[7168.4, 7156.2, 7550.5]
```
Arm B injected a mob-dict skill `{cooldown_seconds: 1.2, damage_multiplier: 1.0,
effects:[{damage, magnitude 300, physical}]}` and nothing else changed. The injected values are
live.

### 2.5 Three pre-flight facts a G-5 harness must carry (none require code change)

1. **A mob dict with `skills: []` deals ZERO damage.** `_select_skill_for_entity` returns `None`
   with no skills, so the mob-action branch (`spatial_engine.py:4613-4644`) never fires. Arm A above
   is the receipt: `dmg_taken = 0.0` across three fights, 8 mobs, 16 s. This is the state of
   `_synthetic_mob_dict_for_spatial` (`skills: []`, `t4_sim_cycling.py:1159`) and of both
   kit-compiler smokes — **the endgame-BC gauntlet's mobs currently deal no damage at all.**
   (`smoke_kf5_expected_pct.py:50` carries the comment *"Give mobs some HP + a token attack skill so
   mob→player (received) hits can land"* above a dict with no `skills` key.)
2. **`MOB_HP_DIFFICULTY_MULTIPLIER = 1.5` will silently multiply an injected `max_hp`** in
   `open_arena` / `chokepoint_corridor` for swarm/magic/elite tiers unless the harness passes
   `apply_mob_hp_difficulty_multiplier=False` (`spatial_engine.py:5978`, applied `:6146-6152`).
3. **`SPATIAL_DAMAGE_SCALE = 0.6`** (`spatial_engine.py:840`) multiplies the caller's
   `damage_modifier` into the *player's* output at `spatial_engine.py:6115`
   (`spatial_dm = damage_modifier × SPATIAL_DAMAGE_SCALE`). It does **not** touch mob output. A
   pinned comparison must decide whether it stays at 0.6 or is neutralized by passing
   `damage_modifier = 1/0.6`.

---

## §3 — What the sim generates today at an "early game" tier

**Framing constraint, stated because it governs any side-by-side:** the engine has **no character or
monster level**. Its single anchor is `CLASS_HP_REFERENCE = 20_000` = *"average tier-50 class HP"*
(`monster_generator.py:20`). There is no L12 regime in-tree. The nearest structural analogues to
"early-game trash" are the **low threat tiers** (swarm / magic / trash) of the **generic**
generation table — which is what a live season bestiary carries.

### 3.1 Generic regime — MEASURED from `seasons/season_001010/monsters/*.json` (44 monsters)

| tier | n | HP min–max (median) | armor min–max | spec HP range (`TIER_HP_FACTOR_RANGE` × 20,000) |
|---|---|---|---|---|
| swarm | 12 | 1,722 – 2,302 (1,985) | 7 – 23 | 1,600 – 2,400 |
| magic | 8 | 4,056 – 5,720 (5,192) | 51 – 98 | 4,000 – 6,000 |
| trash | 12 | 8,858 – 11,722 (10,842) | 198 – 387 | 8,000 – 12,000 |
| elite | 6 | 27,172 – 34,512 (31,141) | 1,084 – 2,104 | 25,000 – 35,000 |
| mini-boss | 4 | 77,805 – 86,220 (79,640) | 5,330 – 6,117 | 60,000 – 100,000 |
| boss | 2 | 146,521 – 184,917 (165,719) | 18,740 – 19,949 | 120,000 – 200,000 |

### 3.2 Damage-per-hit and cadence — MEASURED, same corpus, damage-role skills only

| tier | attack `cooldown_seconds` min–max (median) | `damage` magnitude min–max (median) | skills/mob |
|---|---|---|---|
| swarm | 0.0 – 8.7 (**1.4**) | 625 – 2,500 (**625**) | 1.8 |
| magic | 0.2 – 9.9 (4.6) | 625 – 2,500 (1,500) | 1.8 |
| trash | 0.5 – 8.9 (1.4) | 625 – 2,500 (625) | 2.5 |
| elite | 0.1 – 9.5 (2.75) | 625 – 2,500 (1,062) | 3.3 |
| mini-boss | 0.4 – 8.3 (1.4) | 625 – 2,500 (625) | 3.5 |
| boss | 0.6 – 8.7 (5.4) | 625 – 2,500 (1,500) | 4.0 |

`damage_multiplier` is **1.0 on every skill of every monster in the corpus** (44/44 monsters).

**Structural finding: monster per-hit magnitude is tier-INVARIANT.** The magnitude ladder is
`base_magnitude = tier² × role_multiplier` (`math_model.py:44,52-62`) — power-tier 50 → 2,500;
`primary_attack` ×0.25 → 625, `area_damage` ×0.6 → 1,500, `burst_damage` ×1.0 → 2,500,
`damage_over_time` ×0.3 → 750. A swarm mob and a boss draw from the same magnitude set. Tier
threat is expressed through HP, armor, skill count and `TIER_EFFECTIVE_ATTRIBUTE` — and the last of
those does not reach a spatial mob attack at all (§1.4).

### 3.3 Endgame regime (`ENDGAME_MOB_PROFILES`, used by the endgame-BC gauntlet)

swarm 21,000–32,000 (mid 26,500) · magic 64,000–96,000 · elite 65,000–100,000 ·
mini-boss 190,000–231,000 · boss 210,000–252,000. Armor fraction 0.005–0.015 (swarm) up to
0.130–0.200 (boss). ~9–13× the generic low-tier HP.

### 3.4 Player-side reference and the per-hit transfer function (probe `/tmp/g5b_probe2.py`)

```
player projection: max_hp(compute_max_hp) = 14555  armor = 0.0  resists = {}  crit = 0.0  dodge = 0.0
  mob magnitude=  300 physical -> per-hit mean=  296.8  min=  242.0  max=  359.9
  mob magnitude=  625 physical -> per-hit mean=  618.4  min=  504.2  max=  749.7
  mob magnitude= 2500 fire     -> per-hit mean= 2473.6  min= 2016.9  max= 2998.8
  player skill (mag 2500, fresh state) -> per-hit mean= 2473.6  min= 2016.9  max= 2998.8
```
Against a zero-armor / zero-resist defender the transfer is the **identity** modulo the
`U[0.80,1.20]` per-hit roll. This makes the injected `magnitude` directly interpretable as
"damage per hit before the target's mitigation" in both directions — a clean unit for a GD
side-by-side.

### 3.5 Pack sizes and clocks — MEASURED from `ALL_SCENARIOS` / `DIAGNOSTIC_SCENARIOS`

| scenario | mobs | composition | `max_duration_s` | win condition |
|---|---|---|---|---|
| `open_arena` | 40 | 37 swarm + 3 elite | 120 | all_mobs_killed |
| `chokepoint_corridor` | 24 | 20 swarm + 4 magic | 120 | all_mobs_killed |
| `magic_pack` | 24 | 23 swarm + 1 magic | 120 | all_mobs_killed |
| `dense_cell` | 24 | 20 swarm + 4 magic | 120 | all_mobs_killed |
| `escape_lane` | 12 | 12 swarm | 60 | escape_reached |
| `scenario_overrun` | 55 | 51 swarm + 4 elite | 120 | all_mobs_killed |
| `elite_pack` | 3 | 1 elite + 2 magic | 180 | all_mobs_killed |
| `boss_with_adds` | 3 | 1 boss + 2 elite | 240 | boss_killed |
| `mini_boss` | 3 | 1 mini-boss + 2 elite | 240 | mini_boss_killed |
| `open_arena_wall_diag` (diag) | 8 | 8 swarm | 120 | all_mobs_killed |

Tick: `TICK_SIZE = 0.1` s; `REDUCED_TICK_SIZE = 0.5` s available (`spatial_engine.py:107,113`).

---

## §4 — Pack handling and the `pack_proxy_size` disposition

### 4.1 Pack size enters as INDIVIDUAL ACTORS

One `SpawnSpec` in `scenario.mob_spawns` → one `SpatialEntity` → one independently positioned,
independently HP-tracked, independently attacking actor. AOE is resolved geometrically against real
positions (`_compute_aoe_hits`, `spatial_engine.py:1487`), one `resolve_spatial_hit` call per hit
target, with the resolver's own geometry multiplier **neutralized** to `single_target` so the
spatial target list is the sole multi-target model (`_SingleTargetSkillView`,
`spatial_resolver_adapter.py:252-281`). There is **no aggregate proxy** in the current opposition
model.

### 4.2 `pack_proxy_size` — DEPRECATED, and NOT reachable in default config

- Field: `CombatantState.pack_proxy_size: int = 0` (`combatant.py:281`).
- Consumers: `damage_resolver.py:1084-1085` (physical branch) and `:1166-1167` (elemental branch):
  `if defender.pack_proxy_size > 0 and skill.geometry in AOE_GEOMETRIES: dmg *= defender.pack_proxy_size`.
- **Sole writer:** `from_pack_proxy(pack)` (`combatant.py:1191`, sets `pack_proxy_size=pack.pack_size`
  at `:1242`). `PackProxy` itself is marked `DEPRECATED (W0.9.1, 2026-05-21)` (`combatant.py:1149-1170`).
- **Callers of `from_pack_proxy` / `PackProxy(...)` across the repo:** `balance_loop.py:24` imports
  them but only ever uses `isinstance(..., PackProxy)` as a dead safety guard (`:1026`, `:1996`,
  `:2286`, each annotated "will not fire on convergence-path gauntlets post-W0.9.1"); the only
  construction site anywhere is `tests/test_resistance_matrix.py:813`.
- **Neither spatial mob factory writes the field.** `combatant_from_monster` → `from_monster`
  (`combatant.py:1246`) and `combatant_projection_from_monster_dict`
  (`spatial_resolver_adapter.py:218`) both omit it, so it takes the dataclass default `0`.
- The 1D fight engine that the `PackProxy` path served is deleted; `run_spatial_fight` is the sole
  battle sim (`balance_loop.py:27-29`, `t4_sim_cycling.py:1245`).

**Empirically verified** (`/tmp/g5b_probe.py`):
```
mob combatant_state.pack_proxy_size = 0
CombatantState default pack_proxy_size = 0
```

**G-5 pre-flight assertion is safe.** Suggested form, cheap and total:
```python
assert all(m.combatant_state.pack_proxy_size == 0 for m in engine.mobs)
assert engine.player.combatant_state.pack_proxy_size == 0
```
(The `SpatialFightEngine` exposes `.mobs` and `.player` as public attributes, `spatial_engine.py:2651-2652`.)

---

## §5 — Player-side pinning

### 5.1 What IS pinnable through `class_dict`, no code change

`run_spatial_fight(class_dict=..., player_class=None)` (the **projection path**, and the path the
KF-4 kit compiler explicitly targets) reads, at `entity_from_class_dict` (`spatial_engine.py:5512`)
and `combatant_projection_from_class_dict` (`spatial_resolver_adapter.py:173`):

- `id`, `archetype_tag`, `energy_type`, `range_profile`, `dominant_element` → `substrate`
- `movement_speed`
- `stat_distribution` → `attribute_values` **and** `max_hp`
- `skills[]` → cadence (`cooldown_seconds`), cost (`energy_cost`), geometry (`geometry_type`),
  element (`canonical_element`), and **damage per hit** (`effects[].params.magnitude` ×
  `damage_multiplier`)
- `resource_economy{}` (cost/regen/cadence scale, reservations, charge-stack, Wave-C mark grammar)
- `aura_geometry{}`, `proxies[]`

`kit_compiler.compile_kit(kit_id)` (`simulation/kit_compiler/kit_compiler.py:532`) already emits
exactly this dict from an external corpus record (`:616-636`) — D2 / PoE1 / PoE2 pilot kits today,
with a GD kit HELD pending its rank table. **So the player kit is already pinnable to externally
measured source-game numbers, and there is a compiler that does it.**

### 5.2 Two carve-outs — what is NOT pinnable through `class_dict`

**(a) Player `max_hp` is DERIVED and floored.** `entity_from_class_dict:5543`:
`max_hp = compute_max_hp(vitality, strength)` = `10_000 + 75·vit + 20·str`
(`math_model.py:27-29,41`). This holds on **both** the projection path and the full-`PlayerClass`
path — the spatial entity's HP pool never reads a gear `bonus_hp`. Consequences:
- there is **no `max_hp` key** on `class_dict`; HP is reachable only by choosing `vitality`/`strength`;
- the reachable HP is a lattice with step 20 (str) / 75 (vit) and a **hard floor of 10,000**.
GD at level 12 is in the hundreds of HP, so absolute player-HP parity is **not reachable without a
code change**. The *ratio* (player HP ÷ mob damage-per-hit) is fully reachable by scaling injected
mob magnitudes — §3.4 shows the magnitude→damage transfer is the identity.

**(b) Player DEFENCE is hardcoded to zero on the projection path.**
`combatant_projection_from_class_dict` (`spatial_resolver_adapter.py:207-212`) sets
`armor=0.0`, `elemental_resistances={}`, `crit_chance=0.0`, `dodge_chance=0.0`, `accuracy=1.0`,
`status_resist=0.0`, and leaves `block_chance`/`block_value` at their `0.0` defaults. The
kit-compiler's own `class_dict` carries `"defense": {"riders": []}` with the comment *"received-side
mitigation is GAP (R-G5); no riders"* (`kit_compiler.py:630`). On the typed mob→player route the
`PLAYER_ARMOR_FACTOR_*` constants are inert, so a projection-path player takes the **full**
un-mitigated magnitude. Verified: §3.4, `armor = 0.0`, `resists = {}`.

The alternative today is the **full-object path** — pass a real `PlayerClass` as `player_class=`
(+ optional `measured_gear_stats=`), which routes to `from_player_class` and produces real armor /
resists / crit / block. That requires a generated `PlayerClass`, which is precisely what the kit
compiler was built to avoid.

### 5.3 Smallest seam-clean changes if the carve-outs must close (DESCRIBED, NOT IMPLEMENTED)

Both are inside `simulation/`, additive, and byte-identical when the new key is absent — the
established brownfield pattern in this seam.

1. **Player defensive pinning.** In `combatant_projection_from_class_dict`
   (`spatial_resolver_adapter.py:173`), soft-read an optional `class_dict["defense"]` block —
   `armor`, `elemental_resistances`, `crit_chance`, `dodge_chance`, `accuracy`, `block_chance`,
   `block_value`, `status_resist` — each defaulting to the current hardcoded literal. The
   `"defense"` key already exists in the kit compiler's output, so no new contract is invented.
   ~8 lines. Byte-identical for every existing caller (no caller emits those sub-keys today).
2. **Player HP pinning.** In `entity_from_class_dict` (`spatial_engine.py:5543`), read an optional
   `class_dict["max_hp"]` and fall back to `compute_max_hp(vitality, strength)`. ~1 line.
   Byte-identical when the key is absent.

Both are within-seam and, per ADR-002, jack-ryan can approve directly. Both would need a math note
first (Discipline #1) and a MIGRATION entry only if they alter an emitted field (they do not).
Neither is required to answer §2 — **the opposition side needs nothing.**

---

## §6 — Consolidated answer table

| Question | Answer |
|---|---|
| 1. Monster stat model | `SpatialEntity` (pos/HP/skills/cadence/AI) + `CombatantState` (armor/resists/crit/dodge/attributes/substrate). Sourced from generated bestiary JSON, `TIER_EFFECTIVE_ATTRIBUTE`, `ENDGAME_MOB_PROFILES`, plus runtime `MOB_HP_DIFFICULTY_MULTIPLIER`. No level field; `threat_tier` carries difficulty. Body = `entity_radius` scalar from `SpawnSpec`. |
| 2. Injection | **YES, no engine code change.** `run_spatial_fight(scenario, class_dict, mob_dicts, …)` / `entity_from_monster_dict(dict, spawn_spec, …)` / `SpatialFightEngine(scenario, player, mobs, …)`. Mob contract is a plain dict; pack size and arena come from a caller-constructed `ArenaScenario`. GD precedent in-tree: `tsf6_track_a_harness.py`. |
| 3. Early-game-comparable ranges | §3.1/§3.2. Swarm HP 1,722–2,302; magic 4,056–5,720; trash 8,858–11,722. Attack cadence median 1.4 s (swarm/trash). Per-hit magnitude 625 (primary) / 1,500 (area) / 2,500 (burst), tier-invariant. Player HP 14,555 (floor 10,000). |
| 4. Pack handling | Individual actors, geometric AOE, no aggregate proxy. `pack_proxy_size` DEPRECATED, sole writer `from_pack_proxy` has zero production callers, both spatial mob factories leave it `0`. **`pack_proxy_size == 0` is assertable and true.** |
| 5. Player-side pinning | Offense/cadence/geometry/element/economy: **YES** via `class_dict` (kit compiler already does it). `max_hp`: **NO** — derived, floor 10,000. Defence: **NO** on the projection path — hardcoded zeros. Both closable with ~9 lines of default-inert change (§5.3). |

---

## §7 — CLOSING: recommendations (clearly separated from the census above)

Everything above is what EXISTS. The following are "should" statements and bind nothing.

1. The G-5 harness should follow the `tsf6_track_a_harness.py` shape: a hand-built `ArenaScenario`
   sized to the GD engagement + hand-built `mob_dicts`, driving `SpatialFightEngine` directly. That
   keeps every GD number one hop from its extraction source and touches no production default.
2. The G-5 pre-flight should assert four things, not one: `pack_proxy_size == 0`,
   `apply_mob_hp_difficulty_multiplier=False`, `len(mob["skills"]) > 0` for every injected mob
   (§2.5 item 1 — a skill-less mob is silently pacifist), and an explicit decision recorded on
   `SPATIAL_DAMAGE_SCALE`.
3. Because absolute player HP cannot be pinned below 10,000, the comparison should be run in
   **normalized** units — TTK in seconds and damage-intake as a fraction of max HP — rather than
   raw HP. This aligns with the charter's stated primary targets (engagement-level TTK shape +
   damage-intake distribution) and makes the HP floor a non-issue rather than a fudge.
4. If the ratified acceptance bands turn out to depend on player *mitigation* shape, §5.3 item 1
   should land before the comparison runs, not after — a zero-armor player is a mitigation
   assumption, and preregistration means naming it up front.

---

**Discipline notes.** #11 empirical inspection: every "reachable / not reachable" claim above is
backed by an executed probe, not by reading. #12: no semantic shift — this census changed nothing.
No production code was written; no telemetry was written.
