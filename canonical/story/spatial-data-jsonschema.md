# Spatial-Data JSON Schema — Engine-Emitted Spatial / Floor / Wall / Combatant-Position Recommendation

**Status:** **Canonical-RECOMMENDATION.** Authored 2026-05-16 by gandalf on Matt-approved knight-rider dispatch (`agentic_orchestration/dispatches/2026-05-16-gandalf-spatial-data-jsonschema-recommendation.md`). Companion to `canonical/story/movement-speed-baseline.md` — that doc locked the *values* of movement speed; this doc locks the *spatial container* those values move through, and the *JSON packet shape* the engine emits to carry both.

**Why this doc exists:** Matt's verbatim 2026-05-16 Day 4 directive: *"Can you commission Gandalf to let you know what the most appropriate spatial / floor / wall data to build into the JSON packet (matching to Tier 1 ARPG precedent) so that we can synthesize the movement speed of Tier 1 ARPG characters and monsters? This gameplay decision should map into JSON and I want it to be exact."* Plus the load-bearing follow-on: *"the movement speed must be added into the core of the engine once we come to a decision so that the gauntlet simulation will be balanced."* The first ask defines the schema shape; the second ask makes the implementation cascade **gauntlet-balance-load-bearing**, not Stage-A2-polish.

**Companion docs:**
- `canonical/story/movement-speed-baseline.md` — locked m/s values (5.75 base; 6.0/7.5/8.0 progression; 48 px/m demo scale; AI_SPEED_MULTIPLIER=0.767)
- `canonical/story/engine-balance-stewardship.md` § Gate 3 + Recommendation 3b — the original framing this doc operationalizes alongside the movement-speed-baseline doc; Lock 3 source-of-truth on the abstraction limitation
- `canonical/story/engine-generic-meta-structure.md` — the L1/L2/L3 three-layer model this schema operates within
- `canonical/story/form-bias-cadence-strategy.md` § strategic-axis lock — sub-lock (a) ARPG-canon-primary at substrate; sub-lock (b) Isekai-canon-primary at narrative-skin
- `canonical/story/drift-audit.md` Drift-9 — *"Q2 movement empirically unknown"* — closed by movement-speed-baseline; spatial-container side closed by this doc

**Engine + demo references:**
- `reincarnated-engine/src/reincarnated/simulation/fight_engine.py` (current simulator-internal positional state: range_profile, at_melee_range, CLOSE_TO_MELEE_TIME=0.5)
- `reincarnated-engine/src/reincarnated/simulation/combatant.py` (combatant carries range_profile + at_melee_range)
- `reincarnated-engine/src/reincarnated/export/season_exporter.py` (current JSON export — NO spatial fields)
- `reincarnated-demo/src/world/arena.ts` (current invented spatial container: 1800×944 canvas; 1640×744 floor; elliptical playable area; semi-axes 784×336; spawn positions inset 200px from major-axis ends)
- `reincarnated-demo/src/world/movement.ts` (current invented px/s values + AI multiplier; the consumer being rebased)

**Pending:**
- Knight-rider drafts a decisions-log entry from this recommendation; jack-ryan reviews Gate 1; Matt approves; entry lands at `reincarnated-engine/design/decisions/decisions-log.md`
- Knight-rider authors rocket-schema dispatch + gamora-sim-extension dispatch + drax-render dispatch + (optional) star-lord-telemetry dispatch per Section 6's cascade
- Legolas Mode A precursor commission filed at end of this doc; knight-rider routes if/when needed (recommended optional — current knowledge base is sufficient for the schema lock; Mode A is for *implementation-detail validation* not *schema lock*)

---

## What this doc is — and isn't

**It is** the design recommendation for the engine's spatial-data JSON packet schema — what fields the engine should emit per encounter / room / combatant so that downstream consumers (simulator, demo, telemetry) operate on a single source of truth aligned with Tier-1 ARPG precedent. Plus the cross-seam wiring map, the implementation cascade sequencing, and the open-questions parking lot.

**It is not** the schema implementation itself. No code changes; no actual JSON files; no migration scripts. Those are downstream dispatches.

**It is not** the per-embodiment movement-profile lock. The `movement_profile` enum gets *initial values* here; the final per-embodiment list lands with form-bias Stage 4 narrative-skin work (drax + gandalf future).

**It is not** the procedural-vs-fixed room generation decision. The schema is compatible with either; that decision is a future dispatch chain.

**It is not** a physics-simulation specification. The schema enables movement-speed-synthesis at simulation tick-rate (per Lock 3b's 4-band distance spectrum); it does not require continuous-space physics.

---

## Section 1 — Tier-1 ARPG precedent inventory

The vendors below each made a foundational *spatial-data architecture* choice that drives every downstream consumer (renderer, AI, pathfinder, modding tools). The choice is between **tile-grid** (discrete cells with explicit walkability), **continuous-coordinate** (floating-point positions within bounded regions with implicit collision-shape geometry), and **hybrid** (one for storage / generation; the other for runtime simulation). Below is what the genre actually did, derived from Legolas's existing design-philosophy knowledge base plus published modding-community / developer-talk material in the gandalf training base. Where gaps exist, they are flagged for the Legolas Mode A precursor commission at end of this doc.

### Path of Exile (GGG; 2013–present)

- **Architecture: hybrid.** Tile-prefab assembly at generation time; continuous-coordinate at runtime simulation. Maps are assembled from a library of "tile" prefabs (each tile is a continuous-coordinate sub-scene with predefined wall geometry, monster spawn anchors, and door connection points). Final maps composite tiles into a connected layout; combatants move through them as continuous-coordinate agents.
- **Unit: continuous-coordinate ("units"; loosely calibrated against a notional 1-unit = small-character-step).** GGG has not published a canonical "1 unit = N meters" conversion; the movement_speed stat-line operates as a percent-of-base multiplier rather than against a real-world absolute.
- **Spatial data exposed at data-layer:** modders can see (via the .ggpk content extraction tools the community maintains) the tile prefab library, monster spawn anchors per tile, and the algorithmic tile-composition rules per map type. Runtime positional state (live combatant positions) is server-authoritative and not exposed.
- **Movement_speed reference:** documented as a base + percent-modifier stat; PoE 1 base is 3.7 m/s (per Legolas research — the value is community-derived from sprite-scale + animation-time measurement, not GGG-published).
- **Lesson for Reincarnated:** the hybrid pattern works at PoE's scale because the *renderer* and *simulator* both speak continuous-coordinate, but generation operates at tile-prefab granularity for compositional reuse. If Reincarnated's engine emits continuous-coordinate runtime data AND tile-prefab composition metadata, it inherits PoE's architectural durability.

### Diablo II / Diablo II Resurrected (Blizzard North; 2000 / Vicarious Visions 2021)

- **Architecture: tile-grid (sub-tile-fractional positions allowed at runtime).** D2's map system is the **most-documented Tier-1 spatial-data architecture in the modding community.** The map is a tile-grid where each cell is walkable / non-walkable / has-overlay; combatants store sub-tile-fractional coordinates for smooth interpolation. The yards/second movement convention (player 9 yards/s run; player 6 yards/s walk) maps directly to grid cells with sub-tile motion between cell-aligned game-state updates.
- **Unit: yards (1 yard ≈ 0.9144 meters — the original Blizzard convention; D2R preserved it for mechanical compatibility).** Tile size relates to yards-per-tile via the .dt1 / .ds1 tile format; community modding tools (Phrozen Keep) expose the conversion explicitly.
- **Spatial data exposed at data-layer:** .ds1 (Diablo Stamp 1) files contain tile layouts; .dt1 (Diablo Tile 1) contain individual tile bitmaps + walkability bitmasks. Monster spawn positions stored per .ds1 stamp; door positions explicit. The format is **fully understood by the modding community** — every spatial property of the game can be inspected and modified.
- **Movement_speed reference:** D2 run = 9 yards/s = 8.23 m/s base (per Legolas research). FRW (Faster Run/Walk) modifies via DR formula: effective = (150 × FRW) / (150 + FRW); every 1% effective adds 0.06 yards/s.
- **Lesson for Reincarnated:** D2's spatial-data format is the **gold standard for modder-friendliness** — every spatial property maps to a named, inspectable file format. If Reincarnated's engine emits spatial data with D2-tier explicitness, modders and downstream tooling get a similar surface area.

### Diablo III (Blizzard; 2012)

- **Architecture: tile-grid (with chunk-based world composition).** D3 uses a tile-grid per scene + chunk-based composition for the broader world map. The tile format is internal (.SNO format; less community-modder-friendly than D2's .ds1/.dt1). Combatants store continuous-coordinate sub-tile positions.
- **Unit: yards (Blizzard convention preserved across the franchise).** Base movement speed 100% = ~6 yards/s = 5.49 m/s (per Legolas research).
- **Spatial data exposed at data-layer:** limited modding surface; the SNO format is internally documented at Blizzard but community-modders have less complete access than to D2. Datamining tools exist but are less mature.
- **Movement_speed reference:** hard 25% gear-cap from boots+Paragon; total maximum ~125% of base (~6.85 m/s); active skills bypass cap.
- **Lesson for Reincarnated:** D3 demonstrates that tile-grid + sub-tile-fractional combatants is the *industry-standard* runtime pattern for isometric ARPG. The 25% MS cap design lesson (Loot 2.0 era community-criticized; later softened) is separately consumed by `movement-speed-baseline.md`.

### Diablo IV (Blizzard; 2023)

- **Architecture: continuous-coordinate + chunk-streamed open world.** D4's shift to an open-world structure forced the franchise away from tile-grid-per-scene toward chunk-streamed continuous-coordinate. Combat encounters still operate within bounded sub-regions but the world topology is continuous.
- **Unit: yards (preserved); base 100% = ~6 yards/s = 5.49 m/s (per Legolas research).**
- **Spatial data exposed at data-layer:** minimal modding surface (Blizzard's closed-platform shipping model; battle.net-only).
- **Movement_speed reference:** post-launch cap raised from 125% to 200%; mounts added as a separate movement layer.
- **Lesson for Reincarnated:** D4's open-world choice was driven by the genre-expansion goal (overworld exploration + MMO-ish content); not relevant to Reincarnated's gauntlet-content scope. Reincarnated's gauntlet-encounter scale aligns with D2/D3/PoE per-encounter scoping, NOT D4's open-world scoping. **The chunk-streamed pattern is the wrong reference for Reincarnated's encounter-scale design.**

### Last Epoch (Eleventh Hour Games; 2024)

- **Architecture: tile-grid (per scene; sub-tile-fractional combatants); hybrid with continuous-coordinate movement-skill calculations.**
- **Unit: continuous-coordinate ("units"; not yards or meters); movement_speed scaled against base.**
- **Spatial data exposed at data-layer:** limited modding surface; the game is closer to D3/D4 than D2/PoE in modder-accessibility.
- **Lesson for Reincarnated:** Last Epoch sits in the same architectural family as D3 (tile-grid runtime; sub-tile combatants). The mature genre-convergence pattern.

### Grim Dawn (Crate Entertainment; 2016)

- **Architecture: tile-grid + chunked-world streaming (similar to D3 but with more modder-accessible tooling).**
- **Unit: continuous-coordinate ("units").**
- **Spatial data exposed at data-layer:** **highly modder-friendly** — Grim Dawn ships with an official ModTools package exposing the spatial-data format. Custom maps possible; the community has built a substantial modding ecosystem.
- **Lesson for Reincarnated:** Grim Dawn demonstrates that **modder-friendly spatial-data exposition is a Diablo-derivative design choice that survived the 25-year genre evolution.** If Reincarnated's engine-licensing pitch (per `engine-generic-meta-structure.md`) is to be credible, the spatial-data format should follow D2/Grim-Dawn-tier inspectability — NOT D3/D4-tier opacity.

### Genre-convergent patterns (across all six)

1. **Continuous-coordinate at the combatant layer is universal.** Every Tier-1 ARPG (including the tile-grid ones) stores combatant positions as sub-tile-fractional continuous coordinates. Tile-grid is for *map composition + walkability*, not for *combatant position state*.
2. **Tile-grid at the map-composition layer is the dominant pattern (4 of 6: PoE, D2, D3, Last Epoch).** D4's chunk-streamed open world is the outlier; Grim Dawn is hybrid-leaning-tile.
3. **Movement_speed is *always* a per-combatant scalar applied to continuous-coordinate motion.** No Tier-1 game uses tile-step movement; all use sub-tile continuous motion with movement_speed driving the rate.
4. **Spawn positions are *always* explicit per encounter** — no Tier-1 game algorithmically derives spawn positions at runtime; they are baked into the encounter / map definition.
5. **Wall geometry is the area where vendors diverge most.** D2 uses walkability bitmasks per tile cell; D3/D4 use collision-mesh per scene; PoE uses tile-prefab wall geometry; Grim Dawn similar to D3 but more accessible.
6. **Door / entry / exit positions are *always* explicit** — every game emits door + portal positions as named anchors in the spatial data. The community refers to these as "spawn anchors" (monster) or "waypoints" (player).

### Mode A precursor commission — flagged but optional

The Legolas existing knowledge base covers spatial-architecture design philosophy adequately for this schema lock. **What it does NOT cover** with precision:

- Exact byte-level layout of D2 .ds1 / .dt1 file formats (modder-community-documented; reference inspection would benefit a `spatial_format_spec.md` companion if Reincarnated ever ships modder tooling)
- PoE's internal tile-composition algorithm parameters (e.g., tile-prefab connection rules; spawn-density per tile-type)
- D4 chunk-streaming sub-chunk sizes (proprietary; not relevant for Reincarnated's encounter-scale scope)
- Last Epoch / Grim Dawn modder-tool data-format specifics

**Gandalf judgment:** the Mode A precursor commission is **OPTIONAL, not required for the schema lock.** The schema below is grounded in the design-philosophy-level pattern (continuous-coordinate combatants + tile-grid walkability + explicit spawn/door anchors) that is genre-convergent across all six vendors. The Mode A precursor would *validate implementation-detail nuance* but not *change the schema shape*. Filing the commission is gandalf's recommendation if Reincarnated ever moves toward modder-tooling support; not blocking for VS2a + Stage A2 implementation.

**Commission shape (filed at end of doc, Section 9) for knight-rider's optional activation.**

---

## Section 2 — Reincarnated's current spatial state + gap analysis

### What the engine has internally (simulator-internal positional state)

Per `engine-balance-stewardship.md` Gate 3 + 2026-05-16 simulation-seam code search:

| Element | Where it lives | Type |
|---|---|---|
| `range_profile` | `combatant.py:106-111`; `combatant.py:257`; `combatant.py:354`; `combatant.py:447`; `combatant.py:497`; `combatant.py:515` | enum: "close" / "medium" / "long" |
| `at_melee_range` | `combatant.py:111` (default False); reset per encounter at `fight_engine.py:425` | bool |
| `CLOSE_TO_MELEE_TIME` | `fight_engine.py:74` | constant: 0.5s |
| Teleport range-closure | `fight_engine.py:224-226` | mechanic: teleport geometry sets at_melee_range immediately |
| Encounter-level positional spread | None — PackProxy collapses pack into unified opponent | absent |

This is **partial positional state** — binary engagement (at_melee_range true/false) + a closing-cost (CLOSE_TO_MELEE_TIME). NOT movement-speed-aware; NOT a distance-spectrum (binary, not graduated); NOT kiting-modeled.

### What the engine emits in JSON packets today (the load-bearing gap)

Per knight-rider's 2026-05-16 cross-seam survey + `season_exporter.py` inspection: **NONE.** The engine emits NO spatial fields in any JSON packet at any level (season / act / encounter / room / combatant). The simulator-internal state above is **internal to fight_engine.py** and never written to disk.

The downstream consequence: the demo invents its own spatial container (`arena.ts` ellipse with semi-axes 784×336 at 1800×944 canvas) and movement-speed values (`movement.ts` 220/180/150 px/s by range_profile). Neither traces to engine intent; both are hand-tuned playtest artifacts. The current calibration epoch + cipher-width metrics + V2 compression numbers are all grounded in a **simulator that doesn't know what space combatants are moving through.**

### The gap, named explicitly

| Gap | Current state | Required state | Cost-of-close |
|---|---|---|---|
| **Combatant position state in JSON** | Absent | `spawn: {x, y}` per combatant per encounter | LOW — derive from encounter dimensions at generation time |
| **Movement_speed in JSON** | Absent | `movement_speed_base: float (m/s)` per combatant | LOW — `movement-speed-baseline.md` defines values; rocket adds field |
| **Movement_profile in JSON** | Absent | `movement_profile: enum` per combatant | LOW initial values; FINAL list with form-bias Stage 4 |
| **Floor dimensions in JSON** | Absent | `floor: {width_m, height_m, shape}` per encounter | LOW — engine picks per-encounter dimensions from a small library |
| **Wall geometry in JSON** | Absent | `walls: [{shape, geometry}]` per encounter | MEDIUM — bounded shapes vs polygon walls is a design call |
| **Obstacle positions in JSON** | Absent | `obstacles: [{position, shape}]` per encounter | MEDIUM — initial scope can be empty list (Stage A2 doesn't need obstacles) |
| **Entry / exit positions in JSON** | Absent | `entry: {x, y}` + `exit: {x, y}` per encounter | LOW — derived from floor dimensions |
| **Distance-spectrum in simulator** | Binary (at_melee_range) | 4-band (melee / near / mid / far) | MEDIUM — gamora Stage A2 (Lock 3b) |
| **Kiting AI in simulator** | None | Range-class retreat logic + close-class chase | MEDIUM — gamora Stage A2 (Lock 3b) |

### What's cheap to lift vs what needs new generation work

- **Cheap lift (schema-additive only):** spawn / movement_speed_base / movement_profile / floor dimensions / entry / exit. These are all *derivable from existing generation logic + per-encounter dimension picks*. No new generation algorithm needed.
- **Medium lift (new generation choices):** wall geometry shape (bounded ellipse vs rectangle vs polygon); obstacle positions (none for VS2a; future B-series).
- **Higher lift (consumer-side):** simulator's distance-spectrum + kiting AI (gamora Stage A2 / Lock 3b).

The **schema lock itself is cheap.** The *consumer-side implementation cascade* is where the load-bearing-for-balance work happens.

---

## Section 3 — Recommended JSON packet schema extension (EXACT per Matt's directive)

### Architectural decision: hybrid (continuous-coordinate at combatant + storage-mode "shape" at floor + tile-grid OPTIONAL for future obstacles)

**Why hybrid, not pure tile-grid:**

- Genre-convergence at the combatant layer is universal continuous-coordinate (per Section 1 finding 1). Reincarnated's combatants will operate continuous-coordinate in both simulator (gamora Stage A2 movement-speed-aware) and demo (drax PixiJS) — *no Tier-1 ARPG uses tile-step combat.*
- Tile-grid at the map-composition layer is dominant (PoE/D2/D3/Last Epoch) but not universal (D4 is chunk-streamed). For Reincarnated's encounter-scale scope (per-encounter bounded arenas; not open-world streaming), tile-grid at composition would *over-engineer* the floor-shape representation. A simple "shape + dimensions" descriptor (ellipse / rect / polygon) captures everything the gauntlet needs.
- The schema is **forward-compatible with tile-grid expansion** — adding a `tile_grid` field per encounter later (for procedural-obstacle composition or modder-tooling support) does not break the continuous-coordinate combatant layer.

**Why continuous m/s as the unit:**

- `movement-speed-baseline.md` already locks meters / m/s as the engine + sim unit. Demo derives px/s via `PIXELS_PER_METER = 48`. This schema preserves that lock — all spatial dimensions are in **meters**; all combatant speeds are in **m/s**; all positions are in **meter-coordinates from a per-encounter origin**.
- Yards / "abstract units" / tiles were considered and rejected: meters is the only Tier-1-honest, unambiguous, real-world unit. Yards is a Blizzard-internal convention (still preserved in D3/D4 but never user-facing); abstract units defer the conversion problem; tiles couple position-state to walkability-state inappropriately.

**Why per-encounter origin (not per-act or per-season global):**

- Each encounter is a self-contained arena (per `engine-balance-stewardship.md` Gate 1's content-distribution framing). Per-encounter origin = (0, 0) at floor-center keeps positions simple, supports per-encounter rotation / mirroring without rewriting coordinates, and avoids global-coordinate accumulation drift.

### The schema fragment — concrete-enough-to-implement

```json
{
  "schema_version": "spatial-1.0",
  "encounter_id": "season_001003_act_001_encounter_003",
  "spatial": {
    "floor": {
      "shape": "ellipse",
      "width_m": 32.7,
      "height_m": 14.0,
      "origin_convention": "center",
      "rotation_deg": 0.0
    },
    "walls": [
      {
        "type": "perimeter",
        "geometry_ref": "floor"
      }
    ],
    "obstacles": [],
    "entry": {"x_m": -13.6, "y_m": 0.0},
    "exit": {"x_m": 13.6, "y_m": 0.0},
    "encounter_meta": {
      "encounter_kind": "trash" ,
      "intended_combat_range_band": "mid",
      "spatial_complexity_tier": "open_arena"
    }
  },
  "combatants": [
    {
      "id": "player",
      "kind": "player",
      "spawn": {"x_m": -10.0, "y_m": 0.0},
      "movement_speed_base": 5.75,
      "movement_speed_effective_at_stage": {
        "early": 6.0,
        "mid": 7.5,
        "late": 8.0
      },
      "movement_profile": "walking",
      "terrain_interaction": {
        "respects_walls": true,
        "respects_obstacles": true,
        "wall_clip": false
      }
    },
    {
      "id": "monster_001",
      "kind": "monster_trash",
      "spawn": {"x_m": 10.0, "y_m": 0.0},
      "movement_speed_base": 5.75,
      "movement_speed_effective_at_stage": {
        "early": 5.75,
        "mid": 5.75,
        "late": 5.75
      },
      "movement_profile": "walking",
      "terrain_interaction": {
        "respects_walls": true,
        "respects_obstacles": true,
        "wall_clip": false
      }
    }
  ]
}
```

### Field-by-field rationale + value ranges

**`schema_version`** — `"spatial-1.0"` string at the spatial-block level (NOT the season-manifest-version; this is a sub-schema). Bumped independently when spatial-block shape changes. Pattern matches `season_manifest_version` evolution per `decisions-log.md` `1aa99b5` entry's approach.

**`encounter_id`** — string; already-canonical encounter identifier; passes through unchanged.

**`spatial.floor.shape`** — enum: `"ellipse" | "rect" | "polygon"`. Initial scope: **ellipse** (matches current demo arena.ts) for trash/elite encounters; **rect** as alternate for corridor-style boss encounters; **polygon** reserved for future irregular-arena designs. Engine picks per-encounter from a small per-encounter-kind library.

**`spatial.floor.width_m` + `height_m`** — float in meters, 1-decimal precision. Initial library values:
- Trash encounters: 32.7m × 14.0m (matches current demo arena = 1568px × 672px ÷ 48 px/m)
- Elite encounters: 28.0m × 28.0m (more compact, square-ish, denser combat)
- Boss encounters: 40.0m × 24.0m (larger, more room for boss telegraphs + player kiting)
- Act-boss encounters: 50.0m × 30.0m (cinematic scale)

These are **starting values**; gamora + drax + Matt refine post-VS2a-playtest. The library exists so generation is deterministic + per-encounter-kind appropriate.

**`spatial.floor.origin_convention`** — enum: `"center" | "corner"`. **Lock: `"center"`**. All positions are relative to floor-center; (0, 0) = arena center; positive x = "east"; positive y = "south" (matches typical 2D-game convention; PixiJS-friendly).

**`spatial.floor.rotation_deg`** — float in degrees, 0-359. Initial scope: always `0.0`. Reserved for future per-encounter rotation (e.g., act-boss arenas with intentional asymmetry).

**`spatial.walls`** — array of wall objects. Initial scope: a single `{"type": "perimeter", "geometry_ref": "floor"}` entry meaning "the floor's shape boundary is the only wall." Future expansion (polygon walls; interior walls) is additive: append additional wall objects with explicit geometry.

**`spatial.obstacles`** — array. **Initial scope: empty list `[]`.** Obstacles are deferred to a future B-series item (post-VS2a; possibly Stage A3 or A7 territory). The field exists in the schema so consumers know it's intentional-empty, not missing.

**`spatial.entry` + `spatial.exit`** — point objects with `x_m` / `y_m`. Initial values: entry at floor's western-major-axis point inset 10% from edge; exit at eastern-major-axis point inset 10%. For ellipse-shape floors, derived from semi-axes. Player spawns near entry; act-boss exit is reserved for future per-act narrative-transition rendering.

**`spatial.encounter_meta.encounter_kind`** — enum: `"trash" | "elite" | "mini-boss" | "boss" | "act-boss" | "mirror"`. Matches existing engine encounter classification.

**`spatial.encounter_meta.intended_combat_range_band`** — enum: `"melee" | "near" | "mid" | "far"`. The gamora-Stage-A2 4-band distance spectrum applied to encounter-design hint. E.g., a "boss" encounter with `intended_combat_range_band: "mid"` tells the simulator + AI that the combat is *designed* for mid-range engagement; informs kiting AI tuning.

**`spatial.encounter_meta.spatial_complexity_tier`** — enum: `"open_arena" | "obstacle_arena" | "corridor"`. Currently always `"open_arena"`. Reserved for future obstacle-design expansion.

**`combatants[].id`** — string; combatant identifier. Player is always `"player"`; monsters get encounter-unique IDs.

**`combatants[].kind`** — enum: `"player" | "monster_trash" | "monster_elite" | "monster_mini_boss" | "monster_boss" | "monster_act_boss" | "monster_swarm" | "mirror_self"`. Drives AI + simulator behavior.

**`combatants[].spawn`** — point object with `x_m` / `y_m`. **Player spawn**: derived from `entry` minus small inset (e.g., 1.5m). **Monster spawn**: derived from encounter-design — trash spawn near exit; elites spawn at floor-center; bosses spawn at exit; swarms spawn in cluster patterns near exit.

**`combatants[].movement_speed_base`** — float in m/s, 2-decimal precision. Per `movement-speed-baseline.md`: player = 5.75; trash monster = 5.75 (parity); fast-archetype monster = 6.6-7.5; bosses = gamora design-call.

**`combatants[].movement_speed_effective_at_stage`** — object with `early` / `mid` / `late` float values in m/s. Per `movement-speed-baseline.md` curve: player 6.0 / 7.5 / 8.0; monster trash 5.75 / 5.75 / 5.75 (no monster scaling per genre convention). Lets the simulator pick the right speed per intended-stage-of-content.

**`combatants[].movement_profile`** — enum (initial-scope values):
- `"walking"` — humanoid bipedal default; most player classes + most monsters
- `"running"` — sprinting variant; reserved for fast-archetype monsters (D2 fetish-style)
- `"crawling"` — low-to-ground variant; slimes, lizards, larvae
- `"floating"` — hover-above-ground variant; spirits, wisps, eyeball-monsters
- `"flying"` — true-aerial variant; reserved for future flying enemies + flying-form embodiments
- `"teleporting"` — discrete-jump variant; reserved for boss-tier teleport mechanics

These are **initial values for schema scaffolding;** the FINAL per-embodiment list lands with form-bias Stage 4 narrative-skin work (drax + gandalf future Stage 4 decision). The schema is forward-compatible: adding `"slithering"` / `"hopping"` / `"rolling"` / etc. is enum-additive.

**`combatants[].terrain_interaction.respects_walls`** — bool. Initial scope: always `true` (no wall-clipping abilities in VS2a). Reserved for future blink / phase / wraith mechanics that ignore walls.

**`combatants[].terrain_interaction.respects_obstacles`** — bool. Initial scope: always `true` (no obstacles in VS2a).

**`combatants[].terrain_interaction.wall_clip`** — bool. Initial scope: always `false`. Reserved for future ghost / phase mechanics.

### What the schema does NOT include (intentional exclusions)

- **Pathfinding metadata** — pathing is consumer-derived from spawn + walls + obstacles + movement_speed; not stored in the JSON. (Tile-grid ARPGs store pathing-friendly cell-walkability; Reincarnated's hybrid approach defers pathing to consumer.)
- **Per-tick combatant position state** — the JSON describes the *initial* spatial container; runtime positions are simulator-state (gamora) and renderer-state (drax), not engine-emitted-JSON-state.
- **Visual effects positions** — VFX positions are derived from combatant positions + skill geometry; not stored in this schema.
- **Camera positions** — drax demo concern; not engine concern.
- **Per-frame collision events** — telemetry concern (star-lord), not spatial-schema concern.

---

## Section 4 — Cross-seam wiring map

| Seam | Role | Implementation surface | Estimated lift |
|---|---|---|---|
| **rocket** | EMITS — generation writes the spatial block per encounter | `season_exporter.py` adds spatial-block emission; per-encounter-kind dimension library; spawn-position derivation; populates `combatants[]` from existing class + monster generation with `movement_speed_base` + `movement_profile` (initial defaults) | ~4-6 hours (small new code + schema additions; matches form-bias Stage 1 embodiment-axis additive pattern) |
| **gamora** | CONSUMES — simulator reads spatial block + drives 4-band distance + kiting AI per Lock 3b | `combatant.py` adds spatial fields to combatant init; `fight_engine.py` replaces binary at_melee_range with 4-band distance state; per-tick distance updates driven by movement_speed; kiting AI for ranged classes; encounter-level positional initialization from spawn | ~1.5-2 weeks (the load-bearing-for-balance work; **the critical path step**) |
| **star-lord** | PERSISTS — telemetry captures per-fight spatial-resolution outcomes (e.g., final distance at fight-end; time-in-each-distance-band; kiting frequency); also persists the spatial block itself in season DB for offline analysis | New telemetry fields under existing fight-result schema; season DB column for spatial-block JSON | ~2-3 hours |
| **drax** | RENDERS — PixiJS demo reads spatial block; constructs arena per `floor.shape` + dimensions; positions player + monster at spawns; consumes movement_speed via `PIXELS_PER_METER = 48` per `movement-speed-baseline.md` | `arena.ts` derives ellipse semi-axes from `floor.width_m` × 48 / 2 etc.; `movement.ts` reads `movement_speed_base` per combatant; existing hand-tuned px/s values removed | ~1-2 days (the demo-rebase work already commissioned per movement-speed-baseline; spatial-block consumption is additive — minor lift on top) |
| **legolas** | OPTIONAL — Mode A precursor research if Reincarnated ever moves to modder-tooling territory | New research/knowledge/ entry on Tier-1 spatial-data-format byte-level specs (D2 .ds1/.dt1; PoE tile prefab algorithm) | ~1 session if commissioned; NOT required for current schema lock |
| **elrond** | NONE — no catalogue impact | n/a | 0 |
| **knight-rider** | SEQUENCES — drafts decisions-log entry from this recommendation; authors rocket + gamora + star-lord + drax dispatches per cascade Section 6; routes legolas commission if needed | n/a (coordination) | ~2 hours |
| **jack-ryan** | REVIEWS — Gate 1 decisions-log entry review; Gate 2 review of cross-seam discipline (schema-emit-with-consumer pairing) | n/a (review) | ~1 hour |

### Cross-seam contract per ADR-002

The schema lock becomes the **cross-seam contract** that all four implementing seams reference. The contract evolves via `season_manifest_version` bumps following the established `1aa99b5` pattern; the spatial-block's independent `schema_version` (`"spatial-1.0"`) allows incremental spatial-schema evolution without season-manifest-version churn for unrelated changes.

`MIGRATION.md` per seam captures the consumer-side adaptation per dispatch.

---

## Section 5 — Strategic-axis-lock compatibility

Per the form-bias 5-entry batch's Entry 1 strategic-axis lock (committed `5d51b5a`):

### Sub-lock (a) — ARPG-canon-primary at substrate-mechanical layer ✓ SATISFIED

The schema is **substrate-mechanical** (continuous-coordinate combatants; tile-grid-forward-compatible map composition; meters-as-unit; explicit spawn/entry/exit/walls). This is Tier-1 ARPG-canon at every layer:

- Continuous-coordinate combatants → universal across PoE / D2 / D3 / D4 / Last Epoch / Grim Dawn
- Hybrid storage (continuous + shape-descriptors) → matches PoE's design-philosophy + Grim Dawn's modder-tooling
- Meters-as-unit → equivalent to Blizzard's yards (D2/D3/D4) with metric clarity
- Explicit spawn / entry / exit → universal pattern
- Per-encounter bounded arena → matches D2/D3/Last Epoch encounter-scale (NOT D4 open-world; per Section 1 rationale)

A Western ARPG-audience player reads this schema's *consequences in-game* (clear arena boundaries; m/s movement; positional combat) as instantly genre-canonical. **Sub-lock (a) preserved.**

### Sub-lock (b) — Isekai-canon-primary at narrative-skin layer ✓ COMPATIBLE

The `combatants[].movement_profile` enum is the **per-embodiment narrative-skin hook.** The substrate-mechanical movement_speed (5.75 m/s) manifests differently per embodiment at the display + UX layer:

- A humanoid hero's 5.75 m/s reads as confident walking
- A slime's 5.75 m/s reads as deceptive-fast-blob-crawling
- A dragon-hatchling's 5.75 m/s reads as awkward-fluttering-glide
- A spirit-wisp's 5.75 m/s reads as ethereal-floating

The substrate (m/s + spawn + walls) is ARPG-canon; the surface (movement_profile + drax's per-embodiment animation choices) is isekai-canon. **Sub-lock (b) preserved** — and the schema actively enables it by exposing `movement_profile` as a separate field from `movement_speed_base`.

### Sub-locks (c) + (d) — convergence at content + ritual layers ✓ COMPATIBLE

The schema operates at the substrate layer; the convergence layers (per-season content + ritual moments) consume spatial data through downstream seams (drax for ritual rendering; rocket for per-season encounter generation). No conflict.

### Entry 2 three-layer model compatibility ✓ PRESERVED

Per `engine-generic-meta-structure.md` three-layer model:

| Layer | What's spatial-schema-related |
|---|---|
| **L1 — Engine substrate** | The spatial schema itself; floor shapes; spawn derivation; movement_speed unit; movement_profile enum framework |
| **L2 — Project cosmology** | Reincarnated-specific per-encounter-kind dimensions (32.7×14.0 for trash; etc.); Court-flavored act-boss arena cinematics (future); Mirror-Trial arena structure (per `naming-triad.md`) |
| **L3 — Per-season content** | Per-season floor-flavor (LLM-generated: "lava-cracked floor" / "fungal-mossed floor" / "starlit-tiled floor" — future Stage 4 work); per-season wall-texture flavor; per-season movement_profile vocabulary modulation |

**The schema preserves the L1/L2/L3 separation cleanly.** The substrate-mechanical fields (dimensions, spawn, walls, movement_speed) are L1; the per-encounter-kind library values + per-act narrative-arena choices are L2; per-season floor-flavor + wall-texture + per-embodiment movement-profile naming is L3.

A licensee (per `engine-generic-meta-structure.md` B2B middleware framing) gets the L1 spatial-schema architecture and brings their own L2 + L3. **The schema is licensable-ready.**

---

## Section 6 — Implementation cascade recommendation (LOAD-BEARING per Matt's follow-on directive)

**Critical context — repeated for emphasis per Matt's directive:** *"the movement speed must be added into the core of the engine once we come to a decision so that the gauntlet simulation will be balanced."* This makes the gamora Stage A2 movement-speed-aware sim extension **load-bearing for gauntlet-balance correctness — not optional Stage A2 polish.** Any gauntlet-balance metric established between now and the gamora Stage A2 integration is provisional and will likely re-shift when integration lands (analogous magnitude to B10 V2's 61% compression of mean |mod-1.0| from 0.82 → 0.3175).

### Recommended sequence

**Step 1 — Knight-rider: decisions-log entry drafting (≤1 day)**
Knight-rider drafts a decisions-log entry from this recommendation. Jack-ryan Gate-1 review. Matt approval. Entry lands at `reincarnated-engine/design/decisions/decisions-log.md`. This becomes the cross-seam contract referenced by all downstream dispatches.

**Step 2 — Rocket: schema-additive engine generation (≤1 week, parallel-compatible)**
Rocket adds the `spatial` block emission to `season_exporter.py`. Per-encounter-kind dimension library; spawn-position derivation; combatant-side `movement_speed_base` + `movement_speed_effective_at_stage` + `movement_profile` defaults. Schema-additive (analogous to form-bias Stage 1 embodiment-axis additive pattern); existing consumers unaffected until they opt-in. **Can ship before or in parallel with Step 3.**

**Step 3 — Gamora: simulator consumption + Stage A2 movement-speed-aware sim extension (≤2 weeks — THE LOAD-BEARING STEP)**
Per `engine-balance-stewardship.md` § Gate 3 Recommendation 3b in full. Extend `combatant.py` with 4-band distance state. Extend `fight_engine.py` with per-tick movement-speed-driven distance updates + kiting AI for ranged classes + range-band-aware skill resolution. Initialize encounter positional state from rocket-emitted spawn data. Re-run convergence on baseline seasons; capture the delta from movement-blind sim.

**This is the trigger for the next calibration epoch.** Until this step completes, all gauntlet-balance claims are provisional.

**Step 4 — Star-lord: telemetry persistence (≤3 hours; can ship parallel with Step 3)**
Add spatial-block persistence to season DB. Add per-fight spatial-resolution telemetry (final distance, time-per-distance-band, kiting frequency). Enables post-hoc validation of design baseline.

**Step 5 — Drax: PixiJS demo consumption (≤2 days; can ship parallel with Step 3 OR post-Step-3)**
Replace `arena.ts` invented dimensions with engine-emitted floor dimensions × 48 px/m. Replace `movement.ts` invented px/s with engine-emitted m/s × 48. Consume spawn positions for combatant placement. Consume movement_profile for per-embodiment animation selection (initial scope: walking-only; richer profiles with form-bias Stage 4).

**Step 6 — Knight-rider: post-integration calibration-epoch decisions-log entry + roadmap amendments**
Draft new calibration-epoch decisions-log entry capturing the post-movement-speed-integration metric shifts (new modifier-range mean; new cipher-width verdict; new doppelganger-gate verdicts). Per Matt's load-bearing directive, this entry supersedes the current calibration epoch (`c000d7d`) once the integration completes. Update `decisions-log.md`. Update `canonical/16-project-roadmap.md` if B12 / B13 sequencing implications crystallize per below.

### Cascade trigger conditions

- **VS2a-ship gating:** Steps 1 + 2 + 5 must complete pre-VS2a-ship per `movement-speed-baseline.md` VS2a-gate. (Drax can hardcode spatial-block constants pending rocket Step 2 if rocket slips; not preferred.)
- **"Next balanced gauntlet" gating:** Step 3 must complete before the next gauntlet-balance claim is treated as authoritative-not-provisional. Per Matt's load-bearing directive.
- **Calibration-epoch boundary:** Step 6 lands post-Step-3-completion and post-fresh-regen-with-movement-speed-integrated. Until then, current calibration-epoch metrics are explicitly provisional.

### B12 / B13 roadmap sequencing implications

**B12 (movement speed / boots / gear slot audit) — partial-promotion-in-progress; recommendation: surface a Stage A2 acceleration check**

The `movement-speed-baseline.md` work already promoted B12's *baseline-anchor subset* to VS2a scope. The *full B12 audit* (boots / gloves / belt gear slots + +% MS affixes + hard-cap design) remains Stage A2 per current roadmap. **My recommendation:** the full B12 work should **land alongside or immediately following gamora Stage A2** (this doc's Step 3) — because:

- Boots primary affix = +% movement_speed; the gear-side affix mechanic is the natural extension of the core movement_speed handling
- Implementing boots' +% MS modifier in a separate cycle after gamora Stage A2 means two integration cycles touching the same code path; tighter to integrate together
- The full B12 hard-cap design (25% per movement-speed-baseline.md analogy with D3) lives in the same conceptual space as the AI_SPEED_MULTIPLIER work

**Surface to knight-rider:** consider B12-full as a Stage-A2-co-shipping item (not deferred-to-later-A2). Knight-rider drafts the roadmap amendment if Matt agrees.

**B13 (active mobility + telegraphs + i-frames) — recommendation: keep deferred**

B13's active mobility (5 new defensive mobility geometries: roll / defensive_dash / strafe_mode / blink / dodge_stance) + telegraphs + i-frame windows is **richer-than-core movement;** not load-bearing for basic gauntlet balance. The core gauntlet's load-bearing-for-balance need is the 4-band distance + kiting AI (Step 3 above); B13's active-mobility layer is a *feel-enrichment* layer on top.

**Recommendation:** B13 stays deferred to its current Stage A2 slot per roadmap. Re-evaluate post-VS2a + post-gamora-Stage-A2 + post-full-B12 — at that point B13 may be ready to ship if Reincarnated wants the D4-tier active-mobility feel. Not load-bearing for balance correctness.

### What this cascade does NOT cover

- The schema lock itself does not require physical room generation (procedural vs fixed); per-encounter dimensions come from a small library. Procedural room generation is a future B-series item; the schema is forward-compatible.
- Multiplayer / co-op spatial considerations (per-player perspectives; pet positions); Reincarnated is currently single-player-only per `project_design_intent` memory; not in scope.
- VFX positions; camera tracking; UI overlays — drax concerns; not engine concerns.

---

## Section 7 — Open questions surfaced by the recommendation

These do not block the schema lock. They surface during implementation OR are explicit Matt-decision items.

### Q1 — Per-encounter-kind dimension library — final values

The initial library values I proposed (32.7×14.0 trash; 28×28 elite; 40×24 boss; 50×30 act-boss) are starting values matching current demo arena dimensions for trash. Refinement comes from drax + gamora + Matt post-VS2a-playtest. **Decision-dependency:** playtest feedback on whether boss arenas feel cinematic-enough vs trash arenas feel claustrophobic.

### Q2 — Wall geometry representation — perimeter-only vs polygon

Initial scope: walls are only the floor perimeter (`{"type": "perimeter", "geometry_ref": "floor"}`). Future scope: interior walls (corridors; pillars; obstacle-arena designs). **Decision-dependency:** when Reincarnated's design moves beyond open-arena encounters toward corridor / obstacle-arena designs. Not blocking VS2a or Stage A2.

### Q3 — Obstacle scope and timing

Initial scope: `obstacles: []`. Future scope: per-encounter obstacle placement (boulders, pits, hazards). **Decision-dependency:** when Reincarnated adds positional gameplay beyond open-arena combat. Likely Stage A3 or A7 territory. Not blocking VS2a or Stage A2.

### Q4 — Per-embodiment movement_profile enum — final list

Initial values: walking / running / crawling / floating / flying / teleporting (6 values). Final list lands with form-bias Stage 4 narrative-skin work (drax + gandalf future). **Decision-dependency:** form-bias Stage 4 per-embodiment narrative-skin scope definition.

### Q5 — Spatial-block storage in season DB vs file-only

Star-lord persistence choice: store the spatial block in the season DB (queryable for offline analysis) vs file-only in the season JSON. **My recommendation:** both — file for the canonical JSON; DB for offline query. **Decision-dependency:** star-lord telemetry-architecture preference. Not blocking the schema lock.

### Q6 — Tile-grid forward-compatibility for modder tooling

The schema is forward-compatible with a future `tile_grid` field per encounter (for D2-style modder-tooling support per Section 1 Grim Dawn lesson). **Decision-dependency:** whether Reincarnated ever moves to modder-tooling territory. If yes, Legolas Mode A precursor commission becomes activated; new `spatial-2.0` schema version adds `tile_grid` field. Not blocking current scope.

### Q7 — 🔴 **Calibration-epoch implication (LOAD-BEARING per Matt's follow-on directive)**

The current calibration epoch (committed `c000d7d`; mean |mod-1.0| ≈ 0.82) + the in-pending cipher-width entry (just-committed-this-turn) + gamora's V2 smoke compression (0.3175) + the in-flight post-B6+V2 full regen are ALL grounded in a **movement-speed-blind, spatial-data-blind sim.** Adding movement_speed + spatial-data integration per Step 3 above WILL likely re-shift modifier-range metrics. **A new calibration-epoch decisions-log entry will land post-integration** per Step 6 of the cascade.

**Until that lands, ALL current gauntlet-balance claims are explicitly provisional.** Surface this implication explicitly so downstream agents (gamora B6 main; future balance-loop work; the in-flight post-B6+V2 full regen interpretation) know not to over-anchor on current calibration-epoch numerics.

**Expected direction of shift (gandalf hypothesis; gamora confirms empirically):**
- Single-target class modifiers move toward 1.0 (kiting-aware sim closes the gap; less compensation needed)
- AOE class modifiers may slightly increase (less free pack-clear advantage when single-target kiting closes the gap)
- Pack-fight win rates may decrease modestly (kiting reduces AOE-class effective pack DPS as monsters spread positionally)
- Mean |mod-1.0| may compress further OR stay similar (the cipher-width entry's Outcome 2 framing already accounts for substantial modifier-range; movement integration may not shift this metric as dramatically as B10 V2 did)

**Risk:** treating current calibration-epoch numerics as authoritative when they will likely shift creates downstream design-decision waste. Surface explicitly in the decisions-log entry knight-rider drafts.

### Q8 — VS2b interaction

VS2b (Substrate Realignment) ships in parallel with VS2a per `canonical/16-project-roadmap.md`. Does the spatial-data schema interact with VS2b cipher migration / embodiment-axis / Pimen full integration? **My read:** orthogonal. Spatial schema operates at substrate-mechanical layer (L1); cipher migration operates at vocabulary-cipher layer (L3-related); embodiment-axis operates at narrative-skin layer (L2/L3). The schema's `movement_profile` field is the *narrow surface* of interaction — and that interaction is "embodiment vocabulary informs movement_profile naming," which lands with form-bias Stage 4 (already coordinated). **No blocking conflict.**

---

## Section 8 — Cross-references

- **Required reading consumed:**
  - `agentic_orchestration/dispatches/2026-05-16-gandalf-spatial-data-jsonschema-recommendation.md` — this dispatch (all 7 sections)
  - `canonical/story/movement-speed-baseline.md` — the value-locking sibling doc
  - `canonical/story/engine-balance-stewardship.md` § Gate 3 + Recommendation 3b — the abstraction-naming + sim-extension framing
  - `canonical/story/engine-generic-meta-structure.md` — three-layer model
  - `canonical/story/form-bias-cadence-strategy.md` — strategic-axis lock four sub-locks
  - `canonical/16-project-roadmap.md` § VS2a + § VS2b + § Stage A2 — scope context + B12/B13 deferral framing
  - `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 batch — engine-balance-stewardship entry, calibration-epoch (c000d7d), form-bias 5-entry batch (5d51b5a), ailment-deferral (680a3f1), cipher-width (just-committed)
- **Engine code referenced:**
  - `reincarnated-engine/src/reincarnated/simulation/fight_engine.py` (CLOSE_TO_MELEE_TIME, at_melee_range, teleport-close)
  - `reincarnated-engine/src/reincarnated/simulation/combatant.py` (range_profile + at_melee_range state)
  - `reincarnated-engine/src/reincarnated/export/season_exporter.py` (current spatial-emission: none)
  - `reincarnated-demo/src/world/arena.ts` (current invented arena: 1568×672 px ellipse; semi-axes 784×336)
  - `reincarnated-demo/src/world/movement.ts` (current invented px/s + AI multiplier)
- **Drift-audit instances addressed:**
  - Drift-9 (Q2 movement empirically unknown) — partial-close via this schema (full close requires Step 3 gamora completion)
  - Implicit-pillar Drift on spatial-container blindness — closed by this schema lock

---

## Section 9 — Legolas Mode A precursor commission (OPTIONAL — knight-rider routes if needed)

**Status:** drafted-as-optional; gandalf judgment is **not required for current schema lock.** File only if Reincarnated moves toward modder-tooling territory OR if Matt wants implementation-detail validation prior to gamora Stage A2.

**Title:** *Mode A precursor — Tier-1 ARPG spatial-data-format technical inventory*

**Purpose:** Augment existing design-philosophy-level Legolas knowledge base with technical-format-level specifics for Tier-1 ARPG spatial-data architectures. Inputs to a future `spatial_format_spec.md` companion if Reincarnated supports modder tooling, OR validation-grounding for gamora's Stage A2 implementation choices.

**Vendors + research targets:**

1. **Diablo II — .ds1 / .dt1 file format** (community-modder-documented at Phrozen Keep; the gold-standard reference)
   - Byte-level layout of .ds1 stamp files (tile composition; monster spawn anchors; door positions)
   - .dt1 tile bitmap format (walkability bitmasks; per-cell metadata)
   - Yards-per-tile conversion canonical reference
   - Modding-community-documented vs Blizzard-internal-only distinction

2. **Path of Exile — tile prefab system + composition algorithm**
   - GGP file content extraction (community .ggpk tools)
   - Tile prefab structure (wall geometry, spawn anchors, door connection points)
   - Map composition algorithm parameters (tile-connection rules, spawn-density per tile-type)
   - Whether GGG has published any developer-talk content on the algorithm (GDC, ExileCon)

3. **Last Epoch + Grim Dawn modder-tool data-formats**
   - Official ModTools (Grim Dawn) — what spatial-format access is exposed
   - Last Epoch community-modder tools — current state of spatial-format access

4. **D4 chunk-streaming sub-chunk specifics** (low-priority; not relevant for Reincarnated's encounter-scale scope)

**Acceptance:** a research document at `agentic_orchestration/research/knowledge/arpg-spatial-formats/` covering each vendor's technical spatial-data-format specifics. Estimated ~1 session Legolas Mode A.

**Activation trigger:** Matt approval + knight-rider routing. Not blocking current schema lock; gandalf recommends activation **only if** modder-tooling support is on the Reincarnated roadmap OR Matt wants implementation-detail validation prior to gamora Stage A2.

---

## Maintenance protocol

When knight-rider drafts the decisions-log entry from this doc:

1. Reference this doc as authoritative
2. Capture the schema lock as the cross-seam contract
3. Capture the load-bearing-for-balance cascade per Section 6
4. Capture the calibration-epoch implication per Section 7 Q7
5. Note B12 sequencing recommendation (Stage A2 acceleration check) + B13 sequencing recommendation (keep deferred)
6. Jack-ryan Gate 1; Matt approval; commit

When gamora Stage A2 sim consumption ships (Step 3 of cascade):

1. Re-converge baseline seasons against new spatial-aware + movement-speed-aware sim
2. Capture the modifier-range delta vs current calibration epoch
3. Knight-rider drafts new calibration-epoch decisions-log entry (Step 6 of cascade)
4. Update this doc's Section 7 Q7 with empirical findings

When form-bias Stage 4 narrative-skin work surfaces per-embodiment movement_profile final list:

1. Update `movement_profile` enum in the spatial-block schema
2. Bump spatial schema_version (`spatial-1.0` → `spatial-1.1` if additive; `spatial-2.0` if breaking)
3. Coordinate with drax for per-embodiment animation selection update

When VS2a + VS2b ship + first family-playtest cycle returns:

1. Check Q1 dimension library values against playtest feedback (arena feel)
2. Check Q4 movement_profile values against player-embodiment-perception feedback
3. Surface drift instances if any spatial-design-intent drift is observed
4. Author additional spatial-design canonical-story docs as Reincarnated's spatial scope expands beyond open-arena encounters

— gandalf, 2026-05-16 (Day 4)
