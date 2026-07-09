# Walls Feasibility Spike (Fork 3) — E10 Leg 3 PREP

**Author:** gamora (simulation seam). **Date:** 2026-07-09. **Mode:** READ-ONLY feasibility assessment (no engine file written/modified; no wall built).
**Question authority:** `canonical/reap-die-rise-engine/mob-affix-system-spec-2026-07-09.md` §5.1 (Fork 3 ruled), §4 spatial-family row (line 81 "Leader-only — one Waller per pack"), §10.3 (named feasibility spike).
**Seams read:** gamora spatial engine (`reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/`) + rocket room/encounter model (`generation/endgame_encounter_catalog.py`). All citations are read-only observations of what the code does today.

---

## VERDICT: DEEP-ARCHITECTURE-CHANGE

A Waller that spawns blocking geometry which **meaningfully alters a fight** (blocks pathing / blocks LoS-or-hits / forces repositioning) cannot be represented on existing structures. The sim's space is **positional but obstacle-free**: entities have concrete (x, y) coordinates, but there is NO representation of a static occluder that partitions space, and none of the three subsystems a wall must intercept (movement, hit-resolution, target-acquisition) consults any third body. Adding one is a new spatial layer, not bounded plumbing.

Nuance worth surfacing to the ruling: the assessment splits cleanly into **two halves**, and only one half is hard.
- **"Dynamically-spawned mid-encounter"** — SOLVED. The mid-fight injection primitive already exists (F4/F3 escape-lane + timed-add-waves, 2026-07-07). A Waller could TRIGGER a spawn on the existing cadence.
- **"Blocking geometry that alters the fight"** — the deep-change. What gets spawned today is an *entity* (a mob body with an entity_radius); there is no *terrain/obstacle* type, and even if there were, movement/hits/targeting would ignore it.

---

## Two-seam evidence

### Seam 1 — Spatial engine: space is CONCRETE-POSITIONAL but OBSTACLE-FREE

The E4 fork-elicitation "distance-abstract" framing is now **partially superseded** by the 2D spatial engine (SOLE SIM since the 1D deletion, `spatial_engine.py:1-9`). Space IS concrete: `SpatialEntity` carries `x: float, y: float` (`spatial_engine.py:565`), `distance_to()` is Euclidean (`:748`), the `Arena` is a rectangle with `width_m`/`height_m` and per-move boundary clamping (`arena.py:124-153`). So the E4 finding's *action cadence derives from cooldown_seconds* remains true, but the *distance-only* half is outdated for spatial fights — positions are real.

**(a) Is there ANY representation of obstacles / blocking terrain / occlusion today?** NO — with one narrow, non-qualifying analog.
- The single spatial-constraint primitive is `ChokeZone` (`arena.py:104-121`): within a y-band `[y_min, y_max]` it clamps x to `[x_min, x_max]`. It is **static (construction-time), axis-aligned, and a position-clamp only** — it narrows the passable corridor (bottleneck modeling, "without full pathfinding" per its own docstring) but is NOT an interior barrier an entity must route around, and it does NOT touch hit-resolution or targeting. It is the *nearest* existing structure to a wall and still cannot be one.
- `ArenaScenario` (`arena.py:275-` fields) has NO obstacle/wall/terrain field. Its spatial content is `width_m`, `height_m`, `choke_zones`, and spawn positions. Nothing holds a wall object.
- Grep of `spatial_engine.py` for `obstacle` / `occlusion` / `line_of_sight` / `blocking` / `terrain`: zero hits (the only `wall` matches are "wall-clock" budget and a demoted diagnostic scenario name).

**(b) Do movement + target-acquisition consult geometry, or scalar distance?**
- **Movement is straight-line vector-toward-target with NO obstacle avoidance / NO pathfinding** (`_navigate_entity`, `spatial_engine.py:1039-1180`): all five behavior branches compute a target (x, y) then step `entity.x/y += dir * speed` (`:1170-1177`), then `arena.clamp_entity` (`:1180`). An interior wall would be walked straight through.
- **Target acquisition is pure scalar `min(distance)`** — `min(alive_mobs, key=lambda m: player.distance_to(m))` (`:1017`, mirrored `:859`). No geometry / no LoS. A wall could not break target lock.
- **Collision** is entity-vs-entity only: boid soft-collision on radius overlap (`_apply_soft_collision`, `:1183-1206`) + a boss hard-body push-out (`:1207-1221`). There is no static-collider concept; both are between live combatant bodies.

**(c) Is there a notion of position a wall could partition?** Positions exist (real (x, y)), but nothing *reads a partition*. Concretely, the hit kernels are pure attacker→target geometric predicates that consult NO occluder:
- circle: `[t for t in targets if attacker.distance_to(t) <= radius]` (`_compute_circle_hits`, `:786`);
- cone: distance + heading-angle test only (`:789-809`);
- line: `_dist_point_to_segment` on attacker→target, half-width band (`:825-839`).
A wall standing between attacker and target would NOT stop any of these hits. So even a "wall entity" placed at coordinates would be inert against the three things walls must do.

**Dynamic-spawn half (the easy half):** `_spawn_reinforcement` (`:1837`) mints an entity mid-run and `self.mobs.append(ent)` (`:1871`); the run loop fires it via the F4/F3 injection block (`:2109-2182`, gated on `continuous_spawn`/`timed_add_waves`, default-OFF, brownfield-safe). So *triggering a spawn mid-encounter* is a shipped primitive — but it spawns a **mob**, not an **obstacle**, and no obstacle type exists to spawn.

### Seam 2 — rocket's room model: ABSTRACT encounter definitions, cannot HOLD a wall

`EndgameReferenceEncounter` (`generation/endgame_encounter_catalog.py:115-160`) is an **abstract encounter definition**, not a concrete spatial layout. Its geometry-relevant fields are `scenario_shell_id: str` (a *string reference* to one of gamora's 6 hand-authored `ArenaScenario`s — see the shell map at `endgame_encounter_catalog.py:50-56`) plus BC-cell 5-tuple + `mob_composition: list[MobSpec]` + difficulty-intent + `arena_interaction: str` (prose). **The catalog holds NO geometry object of its own.** All actual room geometry (width/height/choke_zones/spawn coords) lives in gamora's `ArenaScenario`. So the question "can a room representation HOLD a wall object?" resolves to seam 1: the wall would have to be a field on `ArenaScenario`, and the only spatial primitive there is `ChokeZone`. rocket's layer would only need a *reference/parameter* to select/place a wall — the representational gap is entirely gamora-side.

---

## The gap — what a fight-altering Waller would take

A wall that meaningfully alters a fight must do at least one of {block pathing, block LoS/hits, force repositioning}. To support any of these:

1. **A static-collider / obstacle type** on `ArenaScenario` (new dataclass; a wall is a segment or rect with lifetime — since Waller walls are *dynamically spawned*, it needs a spawn-time + optional duration, mirroring `TimedAddWave`'s bounded-injection shape).
2. **Movement must route around it** — `_navigate_entity`'s straight-line step (`:1170`) must gain obstacle-aware steering or pathfinding. This is the largest single piece; today there is zero avoidance logic.
3. **Hit-resolution must occlude** — the three `_compute_*_hits` kernels (`:779-839`) must add a segment-intersection test (does the wall segment cross attacker→target?) to drop occluded hits. This is the LoS half; tractable per-kernel but touches the damage path (Discipline #12 semantic shift — changes how existing hits resolve).
4. **Target acquisition** may need LoS-gating (or accept "targets through walls, can't hit them" — a design call).
5. **Dynamic spawn** — reuse the existing injection primitive (the one solved piece).

Rough scope: this is a new spatial subsystem, not a bounded patch. Comparable in weight to the original 2D-engine scaffolding effort, scoped down to static segment-colliders (no full nav-mesh needed if steering is "slide along segment"). Estimate: **a multi-dispatch spatial-layer build (math-note-first per Discipline #1), NOT a Leg-3-rider.** The three subsystem touches (nav, hits, targeting) each carry their own smoke + a semantic-shift call-out.

---

## Deferred confirm-probe (NAMED, not written this session — kept read-only)

**Probe:** a minimal runnable test placing ONE static segment-collider between a ranged kit and its target in `open_arena`, asserting three separations from baseline: (i) melee mob path length increases (must route around) vs straight-line baseline; (ii) a line/cone hit through the segment is dropped (occlusion); (iii) win-rate delta is non-trivial (the wall *altered* the fight, not cosmetic). If any assertion cannot be made to pass without new subsystem code, the DEEP-CHANGE verdict is confirmed empirically. **Do NOT write this session** (read-only constraint); park as the Leg-3 confirm-step should Matt/gandalf want empirical backing before the defer ruling.

---

## Recommendation (recommend; Matt/gandalf rule)

**DEFER Walls out of E10 Leg 3 v1.** Pull + immobilize ride existing plumbing (spec §5.1 — `vortex_pull` geometry + control/ailment layer) and carry the displacement family into v1 on their own. Walls require a genuine static-obstacle spatial layer (obstacle type + obstacle-aware nav + hit-occlusion) that does not exist and cannot be bounded onto `ChokeZone`. Shipping a "wall" that entities walk through and shoot through would be a telegraph without a mechanic — the exact Law-2 failure the spec inverts. Worth the spike verdict, not a quiet cut: Walls are a first-class future spatial-layer workstream, sequenced on its own math-note-first dispatch, not a Leg-3 rider.

---

**Signed:** gamora, 2026-07-09. Read-only; no engine file touched. Verdict + evidence for Matt/gandalf ruling.
