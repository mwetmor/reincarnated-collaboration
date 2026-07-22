# REPLICA-1 — Frame-Schema Contract (`replica-frame/v1`)

**Gate:** G1 of the REPLICA-1 run (charter:
`2026-07-22-replica-1-godot-sim-window-run.md`). **Author:** gandalf `SPEC-AUTHOR`,
named sub-agent, 2026-07-22. **Status:** DRAFT for gamora (G2 emitter) + drax (G3 playback)
to build against; conductor (gandalf `RUN-CONDUCTOR`) ratifies. **Engine grounding-head:**
`2f430457461509378c1bd0c20425e6ac7b06a077` (`2f43045`, the ablation-gate frozen head — the
substrate this spec was READ against; every file:line below is at this commit).

---

## §0 The one law this spec obeys — SUBSTRATE-LED

Every field below is something the Python battle sim **already computes and holds in memory
during `SpatialFightEngine.run()`**. Nothing here requires new sim capability. Where a viewer
would expect something the sim does NOT model (continuous projectile flight, per-hit damage
retention, facing-as-aim, collision volumes), it is a **registered honest gap (§9)** — Matt
seeing sim reality in the window is the product, not a defect. `replica-frame/v1` is a
**faithful serialization of the sim's own state**, not an idealized combat feed.

The architectural consequence (charter §1): because Godot renders these frames and derives
NOTHING, exactness is **by construction**. There is no second combat implementation to diverge.
The schema is the whole contract surface between sim-truth and pixels.

---

## §1 Fight header block (one per fight, first record)

Emitted ONCE at fight start, before any tick. All spatial fields in **sim meters**; the frame
convention is pinned here and inherited by every downstream reader (the `TelegraphSpec` already
carries this exact contract in-band — `spatial_telemetry.py:119-123`, :166-170).

```
record_type:        "header"
schema_version:     "replica-frame/v1"
engine_git_hash:    "2f430457..."           # full 40-char; the emitter reads `git rev-parse HEAD`
fight_id:           str                      # SpatialFightResult.make_fight_id() (UUID)
kit_id:             str                      # e.g. "d2-bowazon" (reference-set cell kit)
cell:               str                      # cell-slot "IV|high|poe1-kinetic-fusillade" (era|side|kit)
scenario_id:        str                      # sim scenario_id, e.g. "t3w3p_swarm_44x44"
formation_class:    str                      # "swarm" | "volley-fan" | "lane" | "emplacement"
composition:        str                      # "encounter" | "matched_baseline"
policy_arm:         str                      # "blind" | "aware"   (charter: BOTH arms)
seed:               int                      # 20260722..25 (gate seeds)
tick_size_s:        0.1                       # TICK_SIZE (spatial_engine.py:107). 100 ms/tick.
max_duration_s:     float                     # scenario.max_duration_s (120.0 for the ref set)

# --- coordinate frame (PINNED — the whole point of 1 sim m = 1 Godot m) ---
frame:
  spatial_unit:     "m"                       # sim-world meters == Godot meters (charter §1 / G3)
  origin:           "bottom_left"             # Arena docstring arena.py:128 — (0,0) bottom-left
  x_axis:           "east(+)"                 # +x → east
  y_axis:           "north(+)"                # +y → north; ALL positions non-negative (clamped)
  angle_unit:       "rad"                     # heading_rad; atan2 convention, 0=east, π/2=north
  arena_width_m:    44.0                       # _ARENA_W (four-family ref set); read from Arena.width_m
  arena_height_m:   44.0                       # _ARENA_H;                        read from Arena.height_m
  choke_zones:      [ {y_min, y_max, x_min, x_max}, ... ]   # arena.choke_zones (empty for ref set)

# --- entity roster (id, side, kit ref, element, spawn, radius, max_hp) ---
entities: [
  {
    entity_id:      str,                       # SpatialEntity.entity_id (stable string key)
    side:           "player" | "mob" | "ally", # from SpatialEntity.allegiance ("player"/"enemy"/"ally")
    is_player:      bool,
    kit_ref:        str,                       # player: kit_id; mob: threat_tier+archetype_tag
    element:        str | null,                # kit/mob element (roster-time; may be null)
    threat_tier:    str | null,                # "swarm"|"magic"|"elite"|"mini_boss"|"boss" (mobs)
    is_boss:        bool,
    spawn_x_m:      float,                      # SpatialEntity.spawn_x
    spawn_y_m:      float,                      # SpatialEntity.spawn_y
    entity_radius_m: float,                     # 0.5 mob / 1.5 boss (SpawnSpec defaults)
    max_hp:         float,                      # SpatialEntity.max_hp
    skills: [ {skill_idx, name, geometry, range_m, element}, ... ]  # roster of castable skills
  }, ...
]
win_condition:      str                        # "all_mobs_killed" (ref set) | "boss_killed" | ...
boss_focus_entity_id: str | null               # self._boss_focus_entity.entity_id if set, else null
```

**Emission note — mid-fight spawns:** the four-family ref-set scenarios build `self.mobs` ONCE
and do NOT stream reinforcements (`continuous_spawn`/`timed_add_waves` are None for the ref set —
arena.py:342/345). So the roster is COMPLETE at the header for REPLICA-1. The schema still carries
a `spawn` **event** (§3) for forward-compat with escape-lane / add-wave scenarios; on the ref set
it never fires.

---

## §2 Per-tick frame (one record per simulation tick)

The engine loop (`SpatialFightEngine.run()`, spatial_engine.py:3653 `while elapsed < max_duration`)
holds every field below in memory at the bottom of each tick. `_tick_counter` (:3563, incremented
:4817) is the frame index; `elapsed` (:3510, advanced :4816 by `tick_size`) is the sim clock.

```
record_type:        "tick"
tick:               int                        # _tick_counter (0-based; 1200 ticks / 120 s fight)
t_s:                float                       # elapsed at this tick = tick * tick_size_s
entities: [
  {
    entity_id:      str,
    alive:          bool,                       # SpatialEntity.is_alive
    x_m:            float,                       # SpatialEntity.x  (continuous; += step each tick)
    y_m:            float,                       # SpatialEntity.y  (post arena.clamp_entity)
    heading_rad:    float,                       # SpatialEntity.heading_rad (faces nav/attack target)
    hp:             float,                        # SpatialEntity.hp (current)
    # --- action state (what this entity is doing THIS tick; sim-computed) ---
    commit_state:   "idle" | "committing" | "channeling",   # SpatialEntity.commit_state (E4)
    commit_skill_idx: int,                        # skill in flight (-1 = none); SpatialEntity.commit_skill_idx
    is_leashing:    bool,                          # SpatialEntity.is_leashing (returning to spawn)
    is_activated:   bool,                          # SpatialEntity.is_activated (serial-engagement latch)
    # --- optional per-tick derived flags (READ-ONLY of existing state; see §2-note) ---
    energy:         float | null,                 # SpatialEntity.energy (player; null-omit for mobs if quiet)
    ailments:       [ {name, remaining_s, element}, ... ]   # combatant_state.active_effects (see §3/§9)
  }, ...
]
```

**§2-note — full-frame vs delta.** `v1` emits a **FULL entity list every tick** (positions +
hp + state for all live entities). Rationale: (a) it is the sim's literal state, zero derivation;
(b) it makes each tick self-contained → the renderer's scrubber can seek to any tick without
replaying history (charter §2 wants pause/step/0.25–4× scrub — random-access needs self-contained
frames); (c) at ref-set scale (≤41 entities × ~9 floats × ≤1200 ticks) the cost is trivial (§4).
**Dead entities:** once `alive=false`, an entity MAY be dropped from subsequent tick frames (the
renderer holds its last position for a death-pose/corpse); the emitter SHOULD keep emitting it for
~5 ticks post-death then drop, so the renderer can play a death transition. This is a size
optimization, not a truth change — the death **event** (§3) is the authoritative death moment.

**Ailments caveat (honest gap HG-4):** `active_effects` lives on `combatant_state`, which is
populated only for the resolver-backed (commit-grade) path. For a projected/flat-path entity
`combatant_state is None` → `ailments: []`. The schema represents this honestly: absent state =
empty list, NOT a fabricated ailment.

---

## §3 Event stream (discrete gameplay events, tick-stamped)

Events are the **authoritative record of every discrete gameplay moment** — the renderer sources
100% of gameplay from these (never re-derives). Each event carries its `tick` so it composes with
the tick frames. Emitted interleaved (NDJSON) as they resolve within a tick.

The sim's event vocabulary is ALREADY enumerated in two substrate structures I map onto directly:
- `FightEvent.VALID_EVENT_TYPES` = `{damage_dealt, damage_received, resource_spent,
  resource_recovered}` (spatial_telemetry.py:85) — the BC-telemetry event enum.
- `TelegraphSpec` (spatial_telemetry.py:104) — the wind-up danger-zone contract, ALREADY declared
  "Godot renders" (:110), field-for-field.

```
record_type:  "event"
tick:         int
t_s:          float
event:        <one of the types below>
```

### 3.1 `damage` — a resolved hit (source → target, one per per-hit landing)
```
event:        "damage"
source_id:    str            # attacker SpatialEntity.entity_id
target_id:    str            # defender SpatialEntity.entity_id
amount:       float          # realized post-mitigation damage this hit (the `dmg` at _apply_skill_damage:2297/2321)
delivered:    float          # overkill-clamped min(dmg, hp_before) — the _delivered_this_hit (:2296/2320)
element:      str | null     # resolver source_element (typed path) / null (flat path)
skill_idx:    int            # attacker's skill index that fired
geometry:     "circle"|"cone"|"line"|"point"|"self"|"none"   # skill_geometries[skill_idx]
target_hp_after: float       # target.hp after this hit (for HP-bar sync without re-derivation)
lethal:       bool           # did this hit set target.is_alive=False (drives death-pose trigger)
```
**Mass-AOE burst (charter §3 requirement):** the loop `for target in targets_hit:`
(`_apply_skill_damage` :2278/:2316) resolves EACH target's damage + death in one tick. The
emitter emits **one `damage` event per target in that loop** — so a burst that kills 25 mobs in
one tick becomes 25 `damage` events (25 `lethal=true`) at the same tick, and the renderer shows
it as exactly what it is: a single cast, 25 simultaneous floaters + deaths. This is the honest
rendering of the sim's instantaneous-AOE model (see HG-1).

### 3.2 `death`
```
event:        "death"
entity_id:    str            # the entity whose is_alive flipped False (any of 7 death sites, e.g. :2303, :3848, :4779)
killer_id:    str | null     # attacker of the lethal hit if known (player death → mob; else null)
death_element: str | null    # self._player_death_element on player death; null otherwise
```
Note: `death` is emitted the tick `is_alive` flips. A `damage` event with `lethal=true` and the
`death` event will co-occur at the same tick for hit-kills; environmental/DoT deaths emit `death`
without a paired `damage` (see HG-3).

### 3.3 `telegraph` — wind-up danger zone (OPTIONAL; gated on `emit_telegraphs`)
Serialize `TelegraphSpec` **field-for-field** (spatial_telemetry.py:144-170). This is the ONE
"projectile-ish" thing the sim models: a danger-zone footprint with a `wind_up_s` lead time
before a boss/mob AREA attack resolves. The sim does NOT branch on avoidance (HG-2), but the
window `[fire_time_s - wind_up_s, fire_time_s]` is real and renderable as a growing/pulsing
telegraph that snaps to a hit at `fire_time_s`.
```
event:        "telegraph"
attack_id:    str            # "{attacker_id}:{skill_idx}" round-trip key
attacker_id:  str
skill_idx:    int
fire_tick:    int            # tick the hit resolves
fire_t_s:     float
wind_up_s:    float
shape:        "circle"|"cone"|"line"|"point"
origin_x_m:   float
origin_y_m:   float
orientation_rad: float | null   # cone/line; null for circle/point
radius_m:     float | null       # circle
range_m:      float | null        # cone range / line length
half_angle_rad: float | null    # cone
width_m:      float | null        # line full width
damage_amount: float            # what the hit WILL deal (metadata; sim always applies it)
```
**Ref-set default:** telegraphs are emitted only when the engine runs with `emit_telegraphs=True`.
For the first REPLICA-1 watch, telegraphs are OPTIONAL (the ref-set kits are player-offense-led;
mob area-attacks are sparse). G2 SHOULD wire the flag so drax can toggle telegraph rendering, but
the mismatch-autopsy (bowazon clear-vs-brick) does not depend on it. Recommend: **emit if cheap,
default-on** — it costs nothing when no area-attack resolves.

### 3.4 `spawn` — mid-fight entity introduction (forward-compat; INERT on ref set)
```
event:        "spawn"
entity: { ...same shape as header roster entry... }
```
Fires only for `continuous_spawn`/`timed_add_waves` scenarios (escape-lane, add-waves). The ref
set never triggers it (roster is complete at header). Included so `v1` needs no schema bump when
those scenarios enter the window.

### 3.5 `resource` — (OPTIONAL, low-priority) energy spend/recover
Maps `FightEvent{resource_spent, resource_recovered}`. Player energy is already in the tick frame
(`entities[].energy`), so a discrete resource event is redundant for rendering a mana bar.
**Recommend OMIT from v1** (the tick-frame `energy` field covers the visual). Listed for
completeness; a resource-cost floater is a launch-scope nicety, not a sim-window need.

---

## §4 File format + size

**Choice: NDJSON** (newline-delimited JSON — one JSON object per line), one file per fight.

Rationale:
- **Self-delimiting frames** → the file is stream-ready (charter §9 non-goal R5 note: schema must
  be stream-ready even though v1 replays from file). A future socket upgrade (charter R5 → v2)
  reuses the identical per-line records over a socket with zero schema rework — each line is one
  frame/event, already framed.
- **Append-emittable** → the emitter writes each tick/event as the sim produces it, no
  hold-whole-fight-in-RAM-then-serialize step; robust to a crash mid-fight (partial file still
  replays up to the crash tick).
- **GDScript-consumable** → Godot 4.6 `FileAccess.get_line()` + `JSON.parse_string()` per line is
  the idiomatic reader; no streaming-JSON parser needed. All values are JSON primitives (float,
  int, string, bool, array, object) — NO Python-isms (no tuples, no NaN; the emitter must coerce
  the decision-trace tuple `(tick, id, intent)` and any tuple-shaped state into JSON arrays/objects,
  and clamp any non-finite float to a sentinel — see §6).

Record order within a fight: `header` first, then per tick: the `tick` frame, then that tick's
`event` records (damage/death/telegraph) in resolution order. A reader can process purely
sequentially OR index by `tick` for random-access scrub.

**Size estimate (40-mob full fight, worst-case full-clear):**
- Header: ~40 entity roster entries × ~250 B ≈ 10 KB.
- Tick frames: ≤1200 ticks (120 s / 0.1 s). Per tick, ≤41 entities × ~9 numeric fields. As
  compact NDJSON (short keys, entities dropping as they die → mean ~20 live) ≈ 20 entities ×
  ~110 B + envelope ≈ ~2.3 KB/tick. Most ref-set fights end well before 1200 ticks (bowazon-class
  clears in seconds-to-low-tens of seconds; ~100–400 ticks typical). Worst case 1200 ticks ×
  2.3 KB ≈ **2.8 MB/fight**; typical full-clear ~300 ticks ≈ **0.7 MB/fight**.
- Events: full-clear of 40 mobs = 40 `damage` (min) to a few hundred (multi-hit) + 40 `death` +
  sparse telegraphs. ≈ 40–400 events × ~180 B ≈ **7–72 KB/fight**.

**Total per fight: ~0.7 MB typical, ~2.9 MB worst-case.** The full reference set =
5 kits × 2 arms × 2 compositions × 6 seeds = **120 fights ≈ 85 MB–350 MB** total. Trivial for
file replay; well within a single directory. (The charter's §2 target is BLIND-vs-AWARE on the 5
mismatch kits; if compositions collapse to `encounter`-only per the autopsy focus, halve it.)

**Naming convention** (one file per fight, sortable, self-describing):
```
replica-<kit_id>__<arm>__<composition>__seed<seed>.ndjson
e.g.  replica-d2-bowazon__aware__encounter__seed20260722.ndjson
      replica-d2-bowazon__blind__encounter__seed20260722.ndjson
```
Directory: `agentic_orchestration/gamora/notes/replica1-frames/` (untracked; regenerable from the
frozen engine + seed — Discipline #3). A `manifest.json` (kit×arm×comp×seed grid + engine hash +
schema_version) sits alongside so drax's playback scene can enumerate the set.

---

## §5 Emission-point map (the gamora G2 build guide)

Every schema field, mapped to where it is available in `SpatialFightEngine.run()` at `2f43045`.
Two emitter shapes are viable; my lean is stated at the end.

| Schema field | Source (file:line at 2f43045) | Notes |
|---|---|---|
| `tick`, `t_s` | `_tick_counter` (:3563, ++ :4817); `elapsed` (:3510, += :4816) | Frame index + clock. Snapshot at loop BOTTOM (after all mutation, before ++). |
| entity `x/y/heading` | `SpatialEntity.x/.y/.heading_rad` (:914-916); player move :4010-4011; nav :1671-1811 | Continuous per-tick; post `arena.clamp_entity` (:4012). |
| entity `hp`, `alive`, `max_hp` | `.hp/.is_alive/.max_hp` (:920-921, :1135) | HP mutated in `_apply_skill_damage` (:2297/2321). |
| `commit_state`, `commit_skill_idx` | `.commit_state/.commit_skill_idx` (:1205-1206) | E4 cast-state machine. |
| `is_leashing`, `is_activated` | `.is_leashing/.is_activated` (:1136, :1144) | |
| `energy` | `.energy` (:938); decremented :4182 | Player pool; mob quiet. |
| `ailments` | `.combatant_state.active_effects` (combatant.py:109 `ActiveEffect{name,params,duration_remaining,source_element}`) | Null-safe: `combatant_state is None` → `[]` (HG-4). |
| **`damage` event** | `_apply_skill_damage` per-target loop (:2278-2304 resolver / :2316-2328 flat). `dmg`, `_delivered_this_hit`, `target.hp`, `is_alive` flip all live INSIDE the loop. | **KEY GAP: not currently retained.** Only the aggregate `total_damage_dealt` delta is captured (:4199). Per-hit source→target→amount requires capturing inside this loop — see emitter shape B. |
| `damage.element` | resolver `source_element` via `resolve_spatial_hit` (spatial_resolver_adapter.py) | Flat path → null. |
| `damage.geometry`, `skill_idx` | `geo`, `skill_idx` at the cast site (:4106, :4135) | |
| **`death` event** | 7 `is_alive = False` sites (:2303, :2327, :2897, :3470, :3848, :4396, :4779) | Player death also sets `_player_death_element` (:2566). |
| **`telegraph` event** | `self.telegraph_buffer` (:2479), minted by `_mint_telegraph_spec` (:1418) when `emit_telegraphs=True` (:2478) | ALREADY a render contract. Field-for-field serialize. |
| header `entities` roster | built in `run_spatial_fight` wrapper (:5624+) from `class_dict`/`mob_dicts`; entities exist as `self.player`, `self.mobs`, `self._positioned_allies` (:3538-3539) | Roster = snapshot at fight start (post-construction, pre-loop). |
| header `arena`/frame | `self.scenario.arena` (`Arena.width_m/.height_m/.choke_zones`, arena.py:134-136) | The pinned frame constants. |
| `winner`, `elapsed_s` (footer) | post-loop resolution (:4819-4906); `SpatialFightResult` (:4940) | Optional trailer record mirroring the result. |
| decision-trace (optional) | `self._decision_trace` (:2416), appended :4000 when `_trace_decisions=True` | `(tick, chosen_target_id, intent∈{advance,hold})`. Coerce tuple→`{tick,target_id,intent}` (no Python tuple in JSON). Useful to render an aim-line / "who is the player pathing to" overlay. |

**Emitter shape A — non-perturbing monkeypatch wrapper (the diagnostic's precedent).**
Exactly the pattern in `2026-07-22-aware-fighter-ablation-trace-diagnostic.py`: wrap
`_get_player_primary_target` (and, for full frames, snapshot the entity lists once per tick via a
wrapped tick hook) from the collab-notes file, engine `*.py` UNTOUCHED (HEAD stays 2f43045, zero
tracked diff). PRO: zero engine change, zero determinism risk (side-effect-free reads), matches
the frozen-head discipline the whole ablation run is under. CON: **cannot cleanly capture per-hit
`damage` events** — `_apply_skill_damage` is a module function whose per-target loop is internal;
a wrapper only sees before/after aggregate. It can capture tick frames (position/hp/state, read
after each tick) and `death` (diff `is_alive` across ticks) and `telegraph` (read
`telegraph_buffer`), but per-hit source→amount is lost to a pure wrapper. Mass-AOE would render as
"these N mobs died this tick" (from `alive` diffs) with a single aggregate damage number, not N
per-hit floaters.

**Emitter shape B — in-engine emitter (a proper observability hook).** Add an OPTIONAL
`frame_sink` callback to `SpatialFightEngine` (default None = byte-identical; same brownfield
pattern as `telemetry_writer`, `_trace_decisions`, `emit_telegraphs` — the engine is FULL of
default-off observability seams). `_apply_skill_damage` gains an optional `on_hit` callback
invoked per resolved target with `(attacker_id, target_id, dmg, delivered, element, target.hp,
lethal)`; `run()` calls `frame_sink.tick(...)` at loop bottom and `frame_sink.event(...)` at death
sites. This is **observability-only, ZERO combat-logic change** (charter G2: "ZERO combat-logic
changes in the same commits") — the callback reads state and mutates nothing. PRO: full per-hit
`damage` events → the mass-AOE burst renders as N floaters + N deaths (the charter §3
requirement). CON: touches engine `*.py`, so it un-freezes 2f43045 → must land as its own gamora
commit under Gate-2, and the ablation gate's frozen-head attestation must be re-pinned to the
new head (or the emitter kept on a branch the ablation re-run doesn't use).

**gandalf lean → Shape B (in-engine emitter), gated properly.** The charter's headline
requirement — "the mass-AOE burst that kills 25 mobs in one tick MUST be renderable as what it
is" (charter §3 event stream) — is ONLY satisfiable with per-hit capture, which Shape A cannot
give. Shape A is a legitimate FALLBACK (position/hp/death frames, aggregate damage) if the in-
engine hook stalls Gate-2, but it under-delivers the burst autopsy. Shape B fits the engine's own
default-off observability-seam convention exactly (`telemetry_writer`/`telegraph`/`trace_decisions`
are all precedent), so it is idiomatic, not invasive. **Sequencing note for the conductor:** the
emitter re-pins the frozen head — coordinate with gamora so the ablation-gate re-run (if any)
attests the NEW head, OR the emitter rides a branch. This is a run-sequencing call, flagged to the
`RUN-CONDUCTOR`, not a schema question.

---

## §6 Determinism + versioning rules

- **Determinism (charter §1 / G2 check):** same seed ⇒ **byte-identical trace**. The sim is
  fully seeded (`self._rng = random.Random(seed)` :2507; two numpy streams :2515-2516 seed-derived
  from the fight seed). The emitter is side-effect-free w.r.t. engine state (reads only), so it
  does not perturb the RNG sequence — a re-run of a seed reproduces the exact fight AND the exact
  frame file. G2's determinism gate: emit seed 20260722 twice → `diff` the two NDJSON files → must
  be identical (modulo the header's `created_at` if any wall-clock field is included — **recommend
  NO wall-clock field in the frame file**; keep it byte-pure. The `SpatialFightResult.created_at`
  timestamp stays in the DB result, NOT in the replica frame).
- **Float determinism:** the sim's floats are IEEE-754 deterministic under a fixed seed + fixed
  code. The emitter MUST serialize floats at **full precision** (`repr`-round-trippable, e.g.
  Python `repr(float)` / `json.dumps` default) — NOT truncated — so byte-identity holds and the
  renderer sees the exact sim position. Non-finite guard: the sim should never produce NaN/Inf in
  position/hp, but the emitter MUST assert-or-sentinel any non-finite value (fail loud rather than
  emit `NaN`, which is not valid JSON and breaks GDScript `JSON.parse_string`).
- **`schema_version` field** is in the header (`"replica-frame/v1"`). Every reader checks it and
  refuses an unknown MAJOR version.
- **Forward-compat stance:** additive-only within `v1` (a reader ignores unknown fields; an
  emitter may add fields without a version bump — the `spawn`/`resource` events and the optional
  `energy`/`ailments`/decision-trace fields are all additive). A BREAKING change (renaming/removing
  a field, changing the frame origin, changing units) bumps to `replica-frame/v2`. The socket-
  stream upgrade (charter R5) is NOT breaking — same records, different transport → stays `v1`.

---

## §7 Zero-derivation renderer contract (the drax G3 law)

Godot **MAY** (presentation-only, no gameplay consequence):
- **Interpolate POSE between ticks** — smooth an entity from its tick-N `(x,y)` to tick-N+1
  `(x,y)` for fluid motion at display framerate (the sim is 10 Hz; the display is 60+ Hz). This is
  the ONLY derivation permitted, and it derives PRESENTATION (in-between pixels), never gameplay.
- **Ease/animate** HP-bar drains, damage floaters, death dissolves, telegraph pulses.
- **Map the frame** — sim 2D `(x_m, y_m)` → Godot 3D ground plane. Godot 4.6 is Y-up, so the
  render transform is `Vector3(x_m, floor_y, y_m)` (sim-Y → Godot-Z; a fixed floor Y). Heading
  `heading_rad` (atan2, 0=east) → a Y-axis yaw. **1 sim m = 1 Godot m** (charter §1 / G3 — flat
  arena at sim coords, NOT the ravine level whose geometry would falsify positions). This mapping
  is a fixed render-side transform, not a sim change.
- **Camera** — isometric-ARPG framing, follow/scrub, free-look. Purely viewer.
- Choose proxy meshes / colors / VFX (the placeholder legibility kit, charter R2): element-colored
  primitives keyed by `geometry`/`element`. Grammar is launch-scope; the placeholder is disposable.

Godot **MUST NOT** (any of these forks the truth — forbidden by construction):
- Compute or roll **damage** (read `damage.amount`/`.delivered`; never recompute).
- Choose **targets** (read `damage.source_id/.target_id` and the decision-trace; never re-select).
- Run **cooldowns / energy / cadence** logic (read `commit_state`, `energy`; never simulate).
- Decide **deaths** (read the `death` event / `lethal` flag; never kill from HP it computed).
- Resolve **hit/miss, collision, dodge, or telegraph avoidance** — the sim has NO avoidance branch
  (HG-2); a telegraph is a drawn danger-zone, and the paired hit ALWAYS lands per the trace.
- Move an entity anywhere the trace didn't put it (interpolation stays ON the tick-N → tick-N+1
  segment; no physics, no steering, no pathfinding).

If the renderer ever needs a value not in the trace to show a gameplay outcome, that is a **schema
gap to fix in v1 (add the field, re-emit)** — NOT a value for Godot to compute.

---

## §8 (reserved — see §9 honest-gap register)

---

## §9 Honest-gap register (what the sim does NOT model — stated plainly for Matt)

These are NOT defects. They are the sim's actual combat model, which the window shows faithfully.
Matt seeing them is the point (charter §0/§1 — improvements land sim-side after he sees reality).

- **HG-1 — No continuous projectile flight. AOE resolves INSTANTANEOUSLY at cast.** A circle/cone/
  line/point skill hit-tests target positions at the fire instant and applies damage in the SAME
  tick (`_compute_aoe_hits` :1343 → `_apply_skill_damage` :2210, both synchronous within the cast
  block :4116-4138). There is no arrow/bolt/orb travelling across the arena over multiple ticks.
  **Renderer disposition:** a bowazon "volley" is N simultaneous hits at cast-tick, not N arrows in
  flight. The window shows a flash + N floaters, honestly. If Matt wants visible projectile travel,
  that is a SIM change (add projectile-flight ticks) pushed back through the loop — exactly the
  iteration the run enables. Do NOT fake travel in Godot (that would derive gameplay-timing the sim
  doesn't have → forks the truth).
- **HG-2 — Telegraphs are INERT in sim (no dodge/avoidance).** `TelegraphSpec` carries a `wind_up_s`
  danger window, but the sim ALWAYS applies the damage at `fire_time_s` with no avoidance branch
  (spatial_telemetry.py:116-118 §7.2). The telegraph is real geometry to DRAW; the hit is
  guaranteed. The renderer must not let a player "dodge" a telegraph — there is no such mechanic in
  the sim.
- **HG-3 — DoT / coverage-pressure damage bypasses the per-hit `damage` channel.** DoT ticks
  subtract from `e.hp` WITHOUT routing through `_apply_skill_damage` (SpatialEntity comment
  :1160-1168 — "the F1 tick site subtracts realized DoT from e.hp WITHOUT routing through
  `_apply_skill_damage`"). Coverage-pressure HP bleed is similar (:2467). **Consequence:** for
  `poe1-caustic-arrow` / `d2-poison-javazon` (the DoT-ailment ref-set cells — the "aware-cleared-
  MORE" mismatch), HP will visibly drain on mobs BETWEEN discrete `damage` events. The renderer
  syncs HP bars from the **tick-frame `hp` field** (always authoritative), so the drain shows
  correctly even where no per-hit `damage` event fires. G2 SHOULD additionally emit a lightweight
  `damage` event for DoT ticks IF cheaply capturable (the DoT tick site is known), tagged
  `element`+`source_id`, so the floater story is complete — but the **tick-frame `hp` is the
  fallback that guarantees HP-bar honesty** regardless. Flag: the DoT autopsy is exactly a case
  Matt will want to SEE (why does aware clear MORE on the DoT kits?), so completing the DoT
  `damage` event is worth G2's effort.
- **HG-4 — Ailment state only exists on the resolver path.** `active_effects` is populated only
  when `combatant_state` is present (commit-grade path). Flat/projected entities show `ailments:
  []`. Honest: absent state → empty, never fabricated.
- **HG-5 — "Facing" is travel/aim heading, not a separate look direction.** `heading_rad` is set to
  face the nav/attack target (:3961, :1671, :1771...). There is no independent head/aim vs
  movement-facing split. The renderer orients the mesh by `heading_rad`; it is aim AND facing.
- **HG-6 — No collision VOLUMES; only soft-push separation + arena/choke clamp.** Entities carry an
  `entity_radius` used for a soft-collision nudge (`_apply_soft_collision` :4023, :1872) and arena/
  choke boundary clamp (:4012) — but there is no rigid-body collision, no blocking, no
  line-of-sight occlusion. Two entities can overlap transiently; walls are position clamps, not
  meshes to collide with. The renderer draws the flat arena + soft-separated proxies; it must not
  add collision that the sim doesn't have (that would move entities off-trace).
- **HG-7 — Player skill "self/none" geometry = a HEAL, not a spatial effect.** A self/none cast
  heals the caster (`self.player.hp += heal` :4111-4112) with no external footprint. The renderer
  shows a self-buff/heal pulse, not an attack. (Same for mob self-casts :4261.)
- **HG-8 — Mid-fight spawns are INERT on the ref set.** The four-family ref-set scenarios never
  stream reinforcements (§1). The `spawn` event exists for forward-compat only; on REPLICA-1 the
  roster is complete at the header and no `spawn` fires.

---

## §10 Non-goals (explicitly OUT of `replica-frame/v1`)

- **VFX grammar fields** (charter R2 DEFER). No particle/shader/asset-binding fields. The renderer
  uses a placeholder legibility kit (element-colored primitives keyed by `geometry`/`element`).
  The VFX grammar remains the launch-scope system; not in this schema.
- **Bundle refs** (charter R1 REMOVE-from-path). No drax bundle-loader / generated-content asset
  keys. The trace carries every render-needed datum inline (archetype/element/skill ids in the
  roster); the loader serves generated-content presentation, not sim-windowing.
- **Live socket streaming** (charter R5 SEQUENCE-to-v2). `v1` is FILE replay. BUT the schema is
  **stream-ready by construction** — every record is a self-delimiting NDJSON line (a frame or an
  event), so the v2 socket upgrade reuses the identical records over a socket with zero schema
  rework. That stream-readiness is a §4 format property, deliberately preserved even though
  streaming is a non-goal for v1.
- **Golden-trace parity battery** (charter R3 DEFER). There is no second combat implementation to
  verify — playback derives nothing. The battery becomes load-bearing only if a Godot-native combat
  port is ever chartered (R4, out of this path entirely).
- **Resource-cost floaters** (§3.5) — the tick-frame `energy` field covers the mana-bar visual; a
  discrete resource event is a launch-scope nicety, recommended OMIT from v1.

---

## §11 Summary handoff (for gamora G2 + drax G3 + conductor)

- **G2 (gamora):** build the emitter per §5. Lean = in-engine `frame_sink` + per-hit `on_hit`
  callback (Shape B), observability-only, default-off, ZERO combat-logic change, its own Gate-2
  commit; determinism gate = emit a seed twice, `diff` byte-identical. Fallback = non-perturbing
  wrapper (Shape A) if the hook stalls, accepting the mass-AOE gap. Emit NDJSON per §4; naming per
  §4. Complete the DoT `damage` event if cheap (HG-3 is an autopsy Matt wants to see).
- **G3 (drax):** consume per §2/§3, obey §7 (interpolate pose ONLY; derive no gameplay). Flat arena
  at sim coords, 1 m = 1 m, sim-XY → Godot-XZ, `heading_rad` → Y-yaw. HP bars sync from tick-frame
  `hp` (authoritative even for DoT). Mass-AOE = N floaters + N deaths at one tick.
- **Conductor (gandalf `RUN-CONDUCTOR`):** the Shape-B emitter re-pins the ablation-gate frozen
  head — sequence gamora's emitter commit vs any ablation re-run (attest new head, or branch the
  emitter). This is the one cross-gate sequencing flag from G1.
```
