# drax BRIEF — parametric `ArenaRoom`: one spec-driven room renders all 6 battle scenarios (WS2)

**Type:** direct gandalf → drax design brief. **Hand-delivered to drax's current session — NOT a KR dispatch.** (Matt directive 2026-06-15: *"author the drax brief for all of it … hand it to Drax in his current session."*)
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized 2026-06-15 (Pattern-B). Matt's own architectural instinct: *"we'd be wasting time recreating all of the rooms as scenes — what's the next best step to move the original room to a pattern that eventually leads to playability and to add and test all the other rooms in that conceptual space?"* This brief is the answer.
**Parent:**
- Build #1 PASS — `agentic_orchestration/galadriel/...boss-arena register-2 scorecard` (`SCENARIO_BOSS_WITH_ADDS` 30×30 @ composite 4.00 + fight-readability PASS; collab HEAD `a27c6df`).
- The proven scripts you already wrote: `reincarnated-godot/scripts/render_boss_arena.gd` (Build #1), `render_lift.gd` + `render_cathedral.gd` (the register-2 lift recipe).
- Engine source-of-truth: `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` (`ALL_SCENARIOS`).
**Supersedes:** my own battle-room routing note § 6, which nominated bespoke Build #2 (chokepoint) + Build #3 (magic_pack) as hand-built scenes. That was the wrong architecture. Matt's parametric instinct is correct; substrate-led discipline says the better architecture wins even when it overturns my prior call. **Do not build bespoke scenes 2–6. Build one parametric room.**

---

## 0. One line

Refactor your proven Build #1 (`render_boss_arena.gd`) from a hardcoded 30×30 boss scene into **one** parametric `ArenaRoom` that reads an engine scenario spec (footprint + spawn list) as **data** and procedurally builds + dresses + populates it. The lift rig stays constant; only footprint + spawns + dressing + camera vary off the spec. This one scene renders **all six** battle rooms as a loop — and is the spine the playable battle-sim replica grows on.

## 1. Why this is the architecture (not just a time-saver)

**Engine-first orientation (CLAUDE.md).** The sim's `arena.py :: ALL_SCENARIOS` is the architectural authority for room geometry. The Godot room is a **consumer / manifestation** of that spec — never a parallel authority. Six bespoke `.tscn` scenes would be six parallel authorities that can silently drift from the sim's geometry (a spawn moved 2 m "for a prettier shot," a footprint rounded). One parametric room that reads the same spec the `SpatialFightEngine` runs **cannot drift**: the engagement geometry is sacrosanct *by construction*. That parity is the whole point — it's the property that lets the visual room and the balance sim stay the same fight forever, for free, instead of being policed by hand.

arena.py says it outright (magic_pack / elite_pack comments): *"Substrate-AGNOSTIC: arena shape and AI are identical for all substrate manifestations."* The Godot `ArenaRoom` is just one more substrate manifestation of that data.

## 2. You're 90% there already — this is a generalization of YOUR working script

`render_boss_arena.gd` is a near-parametric room with the scenario hardcoded. The refactor is: lift the hardcoded values out to the spec. Concretely, these become spec-driven:

| Hardcoded today (`render_boss_arena.gd`) | Becomes (read from spec) |
|---|---|
| `ARENA_W := 30.0`, `ARENA_H := 30.0` (`:54-55`) | `scenario.arena.width_m` / `height_m` |
| `PLAYER_POS`, `BOSS_POS`, `ADD1_POS`, `ADD2_POS` (`:56-59`) | iterate `scenario.player_spawn` + `scenario.mob_spawns[]` → `(x, 0, z=y)` |
| `CHR_PLAYER / CHR_BOSS / CHR_ADD` prefab picks (`:48-50`) | a **tier→prefab map** keyed off `SpawnSpec.threat_tier` (+ `archetype_tag`) |
| figure scale `2.2 / 1.45 / 1.6` (`:214-221`) | keyed off `SpawnSpec.entity_radius` (boss 1.5 → big, swarm 0.5 → small) |
| `_frame_camera()` fixed frame (`:352-363`) | a **camera rule** keyed off footprint aspect ratio (§ 5) |
| boss-summon sigil anchored under boss (`:291-327`) | a **hero-VFX anchor rule** for rooms that have no boss (§ 7) |
| floor/wall tiling already computes `n = round(W/TILE)` (`:112,132`) | already parametric in dims — just feed it the spec dims (+ fix the non-square bug, § 6) |

The lift rig (filmic env + warm-key/cold-rim/low-fill + braziers + the GPUParticles3D hero lifecycle + ground fog/dust/smoke) is **unchanged and constant across all rooms.** This is the a-holds finding: the controllable fidelity layer (lighting + VFX) is content-portable. It rode graybox → cathedral → Build #1 at no recipe cost; it rides across footprints the same way.

## 3. The spec source — the 6 rooms as data

The data model in `arena.py` (read-only; gamora owns it):
- **`Arena`** = `width_m`, `height_m`, `choke_zones[]`, `name`
- **`SpawnSpec`** = `x`, `y`, `heading_rad`, `entity_radius`, `is_boss`, `threat_tier`, `archetype_tag`, `leash_distance_override_m`, `suppress_leash_hp_reset`
- **`ChokeZone`** = `y_min`, `y_max`, `x_min`, `x_max` (interior bottleneck; x-clamp in the y-band)
- **`ArenaScenario`** = `scenario_id`, `description`, `arena`, `player_spawn`, `mob_spawns[]`, `max_duration_s`, `win_condition`, `boss_index`, `mini_boss_index`, `soft_timeout_s`

**The 6 scenarios (verbatim from `ALL_SCENARIOS`; 2D `(x,y)` → world `(x, 0, z=y)`):**

| scenario_id | arena W×H | choke | player | mob_spawns (x,y · tier/archetype · radius) | win |
|---|---|---|---|---|---|
| `open_arena` | 50×50 | — | (25,40) | 8× swarm/swarmer r0.5 @ (20,12)(25,10)(30,12)(18,18)(32,18)(23,8)(27,8)(29,15) | all_mobs_killed |
| `chokepoint_corridor` | 10×50 | y[23,27] x[2.5,7.5] | (5,40) | 8× swarm/swarmer r0.5 @ (2,10)(5,10)(8,10)(3,15)(7,15)(4,5)(6,5)(5,20) | all_mobs_killed |
| `boss_with_adds` ← Build #1 | 30×30 | — | (15,25) | boss/boss r1.5 @ (15,8); 2× elite/brute r0.5 @ (3,26)(27,26) | boss_killed (idx 0) |
| `magic_pack` | 32.7×14 | — | (16.35,10) | magic/caster r0.5 @ (16.35,3); 3× swarm/swarmer r0.5 @ (10,4.5)(22.7,4.5)(16.35,1.5) | all_mobs_killed |
| `elite_pack` | 28×28 | — | (14,20) | elite/brute r0.5 @ (14,6); 2× magic/caster r0.5 @ (5,12)(23,12) | all_mobs_killed |
| `mini_boss` | 30×30 | — | (15,22) | mini-boss/boss r1.0 @ (15,6); 2× elite/brute r0.5 @ (4,14)(26,14) | mini_boss_killed (idx 0) |

**The bridge + the parity discipline (read this carefully — it's the load-bearing part):**
- The room must read these specs from a JSON file `data/arena_scenarios.json` (a serialization of `ALL_SCENARIOS`), **not** from values typed into GDScript. Hardcoding the values back into the loader would re-introduce exactly the drift the architecture exists to prevent.
- **The authoritative `arena_scenarios.json` is GENERATED from `arena.py` by a tiny engine-side emitter** (a ~20-line `json.dump` of the dataclass fields). That emitter is a small engine-seam task (rocket / star-lord) — I'm naming it as a **parity-hardening follow-up, NOT a blocker on you.** Matt will route it to the engine seam.
- **To start NOW without waiting:** bootstrap `data/arena_scenarios.json` from the table above. Mark it `// BOOTSTRAP — regenerated from engine arena.py by the emitter; do NOT hand-edit` at the top. When the emitter lands, the file regenerates and the hand-copy is retired. Build your loader against the JSON **shape** so the swap is a no-op.

## 4. The parametric room contract

`ArenaRoom.tscn` + a loader script that, given one scenario spec, produces a register-2 room identical in *kind* to Build #1:

1. **Shell** — tile the floor to `width_m × height_m` with the 2.5 m Base module; enclose with walls (fix § 6); corner pillars.
2. **Choke zones** — when `arena.choke_zones` is non-empty (only `chokepoint_corridor`), build interior bottleneck wall geometry matching the `ChokeZone` band. (Build #1 never needed this; it's new. The corridor's 5 m-wide gap at y[23,27] reads as two wall stubs narrowing the 10 m corridor.)
3. **Lift rig — constant.** Instance the unchanged env + 3-point rig + perimeter braziers + ground fog/dust/smoke exactly as `render_boss_arena.gd`. Do not re-tune per room.
4. **Dressing — procedural, footprint-scaled.** Skull piles / ritual circle / props placed by rule relative to the footprint and the spawns (never *on* a spawn point), as you already do.
5. **Combatants — placeholder figures at the EXACT spawn positions.** Tier→prefab map; scale off `entity_radius`; face per heading / toward the marquee target. Spawn **positions are sacrosanct**; figure **scale** is a presentation lever (your existing rule — keep it).
6. **Camera** — the rule in § 5.
7. **Hero VFX** — the anchor rule in § 7.

Spawn-position fidelity is the acceptance bar: a re-render of `boss_with_adds` through `ArenaRoom` must reproduce the passed Build #1 (same four figures in the same places, same frame). That's the parity proof for step one.

## 5. Camera rule — this is the structural answer to the CHOKEPOINT question

galadriel flagged the 10×50 corridor and 32.7×14 trash room as "harder shape-generalization tests." In a bespoke world each is a hand-tuned camera. In the parametric world it's **one rule keyed off `aspect = width_m / height_m`:**

- **Near-square (≈0.7–1.4)** — `boss_with_adds`, `elite_pack`, `mini_boss`, `open_arena`: keep your Build #1 fixed elevated 2.5D frame (behind player at high-z, looking toward the marquee), FOV/height scaled so the footprint + front row fit. The locked register frame.
- **Long corridor (aspect ≪ 0.5)** — `chokepoint_corridor` (10×50 = 0.2): the fixed square frame cannot contain a 50 m-long axis at readable scale. Rule: pull the camera back along the long axis (or raise + tilt) to frame the *engagement band* — the player + the chokepoint + the approaching mobs — not the whole 50 m at once. This is where a **follow-camera** becomes correct (and prefigures the playable on-ramp: a follow-cam is what a moving player needs anyway).
- **Wide-shallow (aspect ≫ 1.5)** — `magic_pack` (32.7×14 = 2.3): widen FOV / step back along z so the full 32.7 m width reads; the 14 m depth is shallow so height stays modest.

The complexity lives in **one legible rule the spec's own dimensions select** — not in six hand-tuned scenes. That's the win.

## 6. Bug to fix in the refactor — non-square walls

`_build_walls()` (`:128-142`) uses a single `n = round(ARENA_W/TILE)` for **all four** sides. That's correct only because Build #1 is square (30×30). For non-square footprints (10×50, 32.7×14, 28×28) you need **two** counts: `n = round(width_m/TILE)` for the N/S walls (run along X) and `m = round(height_m/TILE)` for the E/W walls (run along Z). Same for the floor double-loop (`:112-113` already has `n` and `m` — good; just feed real dims). 32.7 m isn't a clean multiple of 2.5 — round tile count and let the last tile slightly overrun under the wall, or inset; your call (presentation lever, not a parity issue — the *collision/spawn* truth is the spec meters, not the tile grid).

## 7. Hero-VFX anchor rule for non-boss rooms

Build #1 anchors the summon sigil + fire column under the **boss** — the marquee read. Four of the six rooms have no boss. The hero VFX (highest-leverage register axis — don't drop it) needs an anchor rule:
- **Boss / mini-boss rooms** (`boss_with_adds`, `mini_boss`): under the boss/mini-boss entity, as today.
- **No-boss rooms** (`open_arena`, `chokepoint_corridor`, `magic_pack`, `elite_pack`): anchor on the **highest-tier mob** (magic > elite > swarm) — the `magic`/`elite` "leader" is the natural channel-source (the champion casting, the elite enraging). For `open_arena` (pure swarm), a **room-center ritual bloom** (the arena itself is the event) reads better than picking an arbitrary mob. Pick per the marquee read; the rule is "anchor on the most-threatening present entity, else room-center."

This is a genuine small design call — make it, capture which you chose, and galadriel scores whether the VFX still carries register-2 without a boss to hang on. If swarm rooms read flat, that's a finding, not a failure.

## 8. "Add and test all rooms" = a loop, and it unblocks galadriel

Iterate `ALL_SCENARIOS` (the 6 keys) through the one `ArenaRoom`. Each room is a data row; rendering it is a render call + a capture run. No new scenes. This also **unblocks galadriel's readability rubric** — she deferred the formal readability axis until 3+ rooms exist. The loop produces all six cheaply, which *delivers* the corpus that lets her formalize the axis. The two workstreams feed each other.

## 9. Scope honesty — what this delivers and what it does NOT

**Delivers:** the *spatial* replica (all six rooms, register-2 dressed, spawns spec-faithful) + the *playability on-ramp*. The on-ramp: swap the `player_spawn` placeholder for an input-driven character controller; sequence the rooms in scenario order with transitions between them — and you can walk the battle-sim gauntlet in Godot.

**Does NOT deliver (unchanged, separately-gated):**
- **The live combat loop.** Placeholder figures standing where the sim spawns them ≠ them fighting. Input-driven multi-form combat integration is the separately-gated milestone it always was (an original a-holds exclusion). This brief builds the *stage*; wiring combat onto it is the next milestone, made approachable by having a stable, parity-guaranteed stage.
- **The real combatant.** Figures stay placeholder Synty kitbashes (as in Build #1). The generative-self / character-creator combatant is a separate track.
- **UI / HUD.** Not in scope; not evidenced.

Keep these lines explicit in your capture notes so galadriel scores the *room*, and we don't over-claim a playable build off a spatial replica.

## 10. Roles / acceptance (unchanged from Build #1 discipline)

- **drax:** builds `ArenaRoom` + the loader + the bootstrap JSON; renders + captures all 6; **does NOT self-score.**
- **galadriel:** lifecycle-scores each room register-2 parity + fight-readability against the rubric (the 6-room corpus also formalizes the readability axis).
- **gandalf:** interprets the scorecards for the canon call (does the parametric room hold register-2 across all six footprints? — that's the next A-holds-class question).
- **engine seam (rocket / star-lord):** the `arena_scenarios.json` emitter — parity-hardening follow-up, **non-blocking**, Matt-routed.

## 11. Suggested sequence

1. **Parity step first.** Refactor `render_boss_arena.gd` → `ArenaRoom` reading `boss_with_adds` from the bootstrap JSON. Re-render the 30×30. **Acceptance: it reproduces the passed Build #1** (same figures, same places, same frame). This proves the parametric path is loss-less before you touch new rooms.
2. **Loop the other five.** Render `elite_pack`, `mini_boss`, `magic_pack`, `open_arena`, then `chokepoint_corridor` (the hardest — choke geometry + long-axis camera) last.
3. **Camera rule** (§ 5) + **non-square walls** (§ 6) + **hero-VFX anchor** (§ 7) fall out as you hit the non-square / no-boss rooms.
4. **On-ramp** (separate increment, once the six render clean): player controller + inter-room transitions = the playable battle-sim spine.

Build to the rubric + the proven lift recipe — not to pixel-matching any marketing frame (the standing a-holds discipline). The reference is composition/mood; the rubric is the gate.

---

**Signed:** gandalf, 2026-06-15
**For:** the parametric `ArenaRoom` refactor — generalize the proven Build #1 into one spec-driven room that reads the engine's `ALL_SCENARIOS` and renders all six battle scenarios as a loop (parity-by-construction; combat geometry sacrosanct because the room reads the same spec the sim runs), with a footprint-aspect camera rule that structurally answers the CHOKEPOINT shape-generalization question, a non-boss hero-VFX anchor rule, the non-square wall fix, and an honest scope line (spatial replica + playability on-ramp delivered; live combat loop + real combatant + UI still separately gated). Bootstrap from the JSON in § 3; the engine emitter that regenerates it from arena.py is a non-blocking parity-hardening follow-up.
