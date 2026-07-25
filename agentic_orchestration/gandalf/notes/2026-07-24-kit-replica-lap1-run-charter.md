# KIT-REPLICA LAP-1 run charter — "same room, different vocabulary"

**Date:** 2026-07-24 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Executes:** drax (presentation seam)
**Pattern:** desirable-run (`operating-procedures/desirable-run-pattern.md`)
**Status:** ✓ **RATIFIED + DISPATCHED 2026-07-24.** Matt ratified §4a as proposed (`polygon-dungeon-realms`
/ `polygon-dwarven-dungeon` / `polygon-ancient-egypt`; the `polygon-dark-fortress` substitute was NOT
taken). No open forks. Run is live in drax's seam.
**Predecessor:** MCP-BAKEOFF (`2026-07-23-mcp-bakeoff-run-charter.md`) — this run exists because that
one produced no judgeable artifact. Its correction is §6.

---

## §0 Intent (one sentence)

Rebuild the king room three times — **geometrically and photographically identical, dressed from three
different Synty packs, each built by a different authoring method** — to produce (a) frames Matt can
judge and (b) a map of where each authoring method stops.

**Matt's framing, verbatim (2026-07-24):** *"exact faithful replicas of the king scene properties just
with specifically chosen different assets"* · *"I want to continue testing production/development
skills, iteratively across a wide breadth of processes and then deep into increasing difficulties
until we find the end of the capability of each tool."*

**This is lap 1 of a standing program**, not a one-off. Deferred to lap 2+: animation (swing/shoot —
Fork A parked, no source ruled), room-geometry variation, tile-set-swap-in-one-builder, VFX bake-off.

## §1 Substrate (bounded, frozen at launch)

**The reference:** `scripts/walltop_level.gd` (`class_name WalltopLevel`, drax 2026-06-21) — a pure
builder whose own header declares it THE level-content seam. Both the play-shell and the PNG harness
call `build_level()`; neither re-implements geometry.

**Reference dressing — `polygon-dark-fantasy`:**

| Slot | Asset |
|---|---|
| floor | `FBX/Buildings/Base/SM_Bld_Base_Floor_Quarter_01.fbx` |
| wall | `FBX/Buildings/Base/SM_Bld_Base_Wall_01.fbx` |
| pillar | `FBX/Buildings/SM_Bld_Pillar_05.fbx` |
| topper | `FBX/Buildings/SM_Bld_Topper_Base_01.fbx` |
| textures | `Misc/Floor_Tiles_01.png` · `Misc/Brick_Small_01.png` · atlas `Alts/PolygonDarkFantasy_Texture_01_A.png` |

**Reference occupant:** king rig (`scripts/king_rig.gd`) — elven-realm `SK_Chr_King_Male_01`.
**Lap-1 occupants:** three existing KT-2 pilot rigs, weapon in hand, idle clip, matched aura:

| rig | mesh | prop | aura |
|---|---|---|---|
| `rig_poe1_cyclone` | `SK_Chr_DarkLord_Male_01` | `SF_Wep_GreatAxe_01` | `#9AA0A6` |
| `rig_d2_firewall_sorc` | `SK_Chr_Male_Sorcerer` | `SM_Prop_WizardStaff_01` | `#FF6A1A` |
| `rig_gd_flames_of_ignaffar_purifier` | `SK_Chr_Hunter_Male_01` | `SM_Wep_Crossbow_01_Rigged` | `#FF7A24` |

Aura hexes are KT-2 inheritances. **Per Matt's ruling ("all kits need a selected aura to match them"),
drax may re-pick each aura to match its kit — a reasoning-boundary call, logged, conductor-reviewed.**

## §2 Fit test (§3 of the pattern)

- **F1 enumerable:** YES — 3 rooms × 1 method each, fixed asset packs, fixed rig set.
- **F2 decidable:** YES — six pre-registered gates, PASS/FAIL per room; exit = artifacts + ledger + register.
- **F3 pre-drainable:** YES — animation OUT (Matt), geometry OUT (Matt), packs = the one open fork below.
- **F4 authority-resident:** YES — gandalf chartered and conducts; drax owns the executing seam.

→ gandalf conducts · drax executes · KR not engaged (single seam).

## §3 THE INVARIANTS — what "faithful replica" means, enumerated

Every one of these is held **identical** to the king room. Any deviation is a FAIL, not a variation.

| # | Invariant | Value |
|---|---|---|
| I1 | Floor footprint | `FLOOR_EDGE = 17.5 m` square (`FLOOR_Q 1.25 × FLOOR_TILES 14`) |
| I2 | Wall run | whole segments per side, no gaps, no overlap, no half-segment |
| I3 | Wall height | matches reference silhouette height (`WALL_H ≈ 3.005743`) within tolerance |
| I4 | Interior clip box | `interior_half = FLOOR_EDGE*0.5 − 0.45 = 8.30` — **`king_clip` + `aura_clip` must still scissor correctly** |
| I5 | Occlusion split | `OCCLUDE_BASE_Y = 1.33` · feather `0.08` · ghost alpha `0.18` — see-through-walls behaves identically |
| I6 | Wall collision | colliders on `WALL_COLLISION_LAYER = 2` so the camera→player raycast still drives occlusion |
| I7 | Camera | angle, zoom, position — bit-identical to the reference shot |
| I8 | Lighting / shading | key `DirectionalLight3D` + WorldEnvironment unchanged; aura energy `0.55`, `AURA_Y_LIFT 0.08` |
| I9 | Occupant scale | `TARGET_HEIGHT 1.85 m` |

**The real difficulty lives here.** `WALL_H = 3.005743` is a *measured* value from the dark-fantasy
wall FBX. Another pack's wall is a different length, height and thickness; its floor tile is a
different size; its atlas has a different UV layout. **The test is whether an agent can measure a new
modular kit and re-derive the constants so the room comes out identical.** The file already documents
this failure class: *"WHY 14 and NOT 13: `WALL_SEGS = FLOOR_TILES / 2` MUST stay a whole number."*
If a pack's wall segment doesn't divide 17.5 m into whole runs, that is a genuine ceiling — **record
it, do not silently re-scale the room.**

## §4 THE VARIABLES

### 4a — Dressing (one pack per room) — **OPEN FORK, Matt rules**

Conductor proposal, chosen for an easy/medium/hard spread **and** a register spread:

| Room | Pack | Walls/Floors | Why |
|---|---|---|---|
| **R1** | `polygon-dungeon-realms` | 81 / 47 | On-genre. Richest floor vocabulary → predicted **easiest** fit. |
| **R2** | `polygon-dwarven-dungeon` | 37 / 8 | On-genre, warm carved stone. **Sparsest** vocabulary → hardest fit. |
| **R3** | `polygon-ancient-egypt` | 137 / 10 | **Off-genre, maximum register separation** → range-finder: does the swap hold when the vocabulary is alien? |

*Alternative for R3 if Matt prefers on-genre only:* `polygon-dark-fortress` (308 walls / 39 floors —
cold black militaristic; the largest architecture vocabulary on disk).
**→ NOT TAKEN. Matt ratified the proposal as written 2026-07-24; R3 is `polygon-ancient-egypt`.**

**Design reasoning:** three similar stone dungeons would give the test no power. D2's act structure
worked because registers were maximally separated (Rogue camp → Lut Gholein → Kurast → Hell);
adjacent registers read as "the same place with a colour filter." The spread is the point.

### 4b — Authoring method (one per room) — the run's real subject

| Method | Definition | **Pre-registered prediction** |
|---|---|---|
| **M1 — MCP wire** | incumbent `satelliteoflove/godot-mcp`, live editor manipulation | **FAILS EARLY.** The room is runtime-built by `build_level()`; the editor tree is empty (KF-6b: *"get_scene_tree returns just the root Node3D"*). Expect the ceiling within minutes. |
| **M2 — direct text authoring** | write/bake the room as `.tscn` text; no wire round-trips | **PASSES, at authoring cost.** Node-count is free; the cost is deriving every transform without an editor. |
| **M3 — generator script** | fork `walltop_level.gd` constants, run headless, capture | **PASSES cheapest.** The repo's native pattern. |

**Predictions are pre-registered so the run is falsifiable.** If M1 surprises us, that is a real
finding. If M3 wins as predicted, the finding is the *margin* — how much cheaper, and where M1/M2 stop.

**Method assignment:** R1→M1, R2→M2, R3→M3 (assigned so the predicted-weakest method meets the
predicted-easiest pack — a fair shot).

**Honorable fallback (pre-registered):** if a method hits its ceiling, **record precisely where it
stopped, then finish that room with M3.** Every room ships a frame regardless. Matt gets three
pictures; we still get three ceilings.

### 4c — Execution order + ledger hygiene (added at dispatch, 2026-07-24)

**Order: R1 → R2 → R3. Strictly sequential, one agent.** Not for convenience — for validity:

- **M1 must go first, before the M3 pipeline exists.** If M3 runs first, the M1 attempt is contaminated:
  the agent already knows the answer and can shortcut to it. A pre-registered prediction only earns its
  keep if the weakest method gets a genuine first attempt against an unsolved problem.
- **No parallel rooms.** Three agents in one Godot working tree contend on a single shared import
  cache (`.godot/`), `project.godot`, and editor state. Concurrent FBX ingest would corrupt the very
  wall-clock numbers the ledger exists to measure.

**The ledger's one methodological trap:** whichever room establishes the measure→derive→build→capture
pipeline pays a one-time cost that later rooms inherit free. Under this ordering that cost most likely
lands on **R1's M3 fallback**. So the ledger MUST split every row:

| | one-time pipeline cost | per-room method cost |
|---|---|---|

A room that took 12 minutes on an established pipeline and a room that took 12 minutes while building
it are not the same number, and the content roadmap depends on not confusing them.

## §5 Pre-registered gates (PASS/FAIL per room)

| Gate | Criterion |
|---|---|
| **G1 geometry** | 17.5 × 17.5 m, whole wall segments, no gaps/overlaps/z-fight |
| **G2 clip** | `king_clip` + `aura_clip` scissor at `interior_half = 8.30`; **no body, weapon or aura fragment renders past a wall** |
| **G3 occlusion** | near walls ghost on approach at `OCCLUDE_BASE_Y 1.33`, ghost alpha `0.18`; raycast fires off layer 2 |
| **G4 collision** | occupant cannot leave the interior; no weapon poke-through at idle extents |
| **G5 photographic identity** | camera / zoom / lighting / shading bit-identical to the reference frame |
| **G6 register** | galadriel scores each room against the reference on the HSV+edge-density register axes — *does the swap change the register, and by how much* |

## §6 Deliverables — **the correction to the bake-off**

**No cell, JSON or prose substitutes for a picture. A presentation run that produces no judgeable
frame has not met its exit predicate.**

1. **Contact sheet** — reference + R1 + R2 + R3, same camera, labelled. Plus a 3×3 (room × occupant)
   if cheap. Harness template: `scripts/shoot_costume_variants.gd` (SubViewport + camera + queue +
   settle-frames + outdir — the loop Matt has eye-picked from before).
2. **Cost ledger** — wall-clock and step-count per room, per method. *This* is the production-skill
   map: if a dressing swap costs 10 minutes and another costs 3 hours, that is the content roadmap.
3. **Failure register** — where each method stopped, and which of the four untested surfaces bit:
   **import / introspection / persistence / skeleton-and-material remap.**

## §7 Matt interface

- **Ratify:** the §4a pack picks (or substitute).
- **In-run:** red-flag pings only. Ruling ledger KRL-1..n, veto open.
- **At end:** the contact sheet. Matt's eye is G-final; galadriel's G6 is advisory.

**HALT to Matt (commitment boundaries):** a pack requires purchase · a room cannot hit 17.5 m with
whole segments and the only fix is changing room size (that is a geometry change, which Matt ruled
OUT) · the occlusion/clip system needs a rewrite rather than a re-parameterisation.

**Reasoning boundaries drax owns in-run:** aura re-pick per kit · which specific wall/floor/pillar/
topper mesh within the chosen pack · texture/atlas selection · measurement method.

## §8 Status ledger (conductor)

- **2026-07-24 — CHARTERED**, awaiting Matt ratification of §4a.
- **2026-07-24 — RATIFIED.** Matt: *"ratify and dispatch."* §4a taken as proposed; dark-fortress
  substitute declined. Zero open forks at launch.
- **2026-07-24 — DISPATCHED** to the named `drax` sub-agent (per gandalf OP § 4.10 — substantial
  pieces route to the seam's named agent, never an unnamed spawn). §4c execution order added at
  dispatch. Run live.

### Ruling ledger (KRL-n) — conductor, veto open to Matt

| # | Ruling | Basis |
|---|---|---|
| KRL-1 | Execution order R1→R2→R3, strictly sequential, single agent | §4c — prediction validity + import-cache contention. *Reasoning* boundary; conductor's to make. |
| KRL-2 | Cost ledger splits one-time pipeline cost from per-room method cost | §4c — otherwise the content roadmap reads a contaminated number. *Reasoning* boundary. |

---

## Appendix — hygiene note (not blocking)

Duplicate packs on disk: `polygon-dark-fantasy` / `polygon-dark-fantasy-01` (64 walls / 6 floors
each) · `polygon-dungeon` / `polygon-dungeon-pack` (78 / 2) · `polygon-dwarven-dungeon` /
`-dwarven-dungeon-map` (37 / 8) · `PolygonDarkFantasy` (a third casing). Worth an elrond/drax pass;
the reference points at `polygon-dark-fantasy`, so the run is unaffected.

---

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-24. Same room, three vocabularies, three methods —
and this time the run ends in a picture.
