# KIT-REPLICA LAP-1 — interim note 1: M1 ceiling + R1 complete

**Date:** 2026-07-24 · **Agent:** drax (presentation seam) · **Conductor:** gandalf
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-24-kit-replica-lap1-run-charter.md`
**Status:** M1 attempt CLOSED (ceiling mapped) · R1 SHIPPED · R2/R3 pending
**Captures:** `~/Games/reincarnated-godot/harness_logs/kit_replica_2026-07-24/`

Filed mid-run per context-budget discipline so R1 and the M1 ceiling survive independently of
the rest of the lap.

---

## 1. M1 — MCP wire (`satelliteoflove/godot-mcp` 4.1.0), assigned R1

**Prediction: FAILS EARLY. Verdict: CONFIRMED — but for a different reason than predicted, and
the real reason is more useful.**

The charter predicted M1 would fail because the room is runtime-built, so the editor tree is
empty (KF-6b). That reason is real and was reconfirmed. But it is **not the binding
constraint**. The binding constraint is simpler and more absolute:

> **godot-mcp 4.1.0 has no node-creation primitive at all.**

Empirically probed over the wire, every one of these returns `UNKNOWN_COMMAND`:
`create_node` · `add_node` · `instantiate_scene` · `create_scene` · `add_child` ·
`delete_node` · `set_property` · `godot_gridmap_edit` · `gridmap_set_cell`

The entire node surface is `node_commands.gd` = `{get_node_properties, find_nodes,
update_node, reparent_node}`. `update_node` sets properties on an **existing** node;
`reparent_node` moves an **existing** node. Nothing creates one. So M1 cannot author geometry
under any circumstance — not "cannot author *this* room."

### What M1 *can* do (verified working, not assumed)

- **Introspection on already-persisted content is solid.** `open_scene` →
  `res://scenes/crypt_vault_node_baked.tscn`, then `get_scene_bounds` → `node_count 724`,
  `combined_aabb size (80, 80, 80)`. `get_scene_tree`, `find_nodes`, `get_spatial_info`,
  `get_node_properties` all function.
- Reconfirmed KF-6b on the live room: `get_scene_tree` on the open editor scene returns just
  the root `Node3D` ("KT3Arena") because the arena is built at runtime.

### What M1 cannot do

| Need | Result |
|---|---|
| Create any node | **ABSENT** — no command exists |
| Measure an un-instantiated asset | **ABSENT** — `get_resource_info` on an FBX returns only `{resource_path, resource_type: "PackedScene"}`. No AABB, no mesh dims, no surface count. And you cannot instantiate it to measure it, because creation is absent. |
| GridMap authoring | **GATED, not absent.** `set_gridmap_cell` / `set_gridmap_cells_batch` DO exist — but they need a pre-existing GridMap node **and** a pre-existing MeshLibrary. `list_gridmaps` → `[]`. No command creates either. So the GridMap path is only reachable *after* another method has authored the GridMap + MeshLibrary. |
| `exec_run` as a back door | **Wrong target.** It relays to the RUNNING GAME via the debugger bridge, not the editor, and nothing it does persists to a scene file. |

### Setup friction worth recording (M1 cost, not R1 cost)

The installed addon was **gutted** — 3 `.gd` files on disk against 36 in the package, and
`plugin.cfg` pointed at a `plugin.gd` that did not exist. The official repair path does not
repair it: `npx @satelliteoflove/godot-mcp@4.1.0 --install-addon` reads the version out of
`plugin.cfg`, sees `4.1.0`, prints **"Addon is already up to date (version 4.1.0)"** and exits
without checking file integrity. A gutted addon therefore never self-heals. Restored manually
from the npm tarball, then re-applied the standing one-line patch (commenting the dead
`class_name MCPGameBridge`, which still collides with the autoload in 4.1.0 —
`// TODO(drax)` carried forward).

MCP tools are **not** in the sub-agent tool surface, so as in KF-6b the wire was driven
directly: `ws://127.0.0.1:6550`, Node 24 native WebSocket, client rebuilt at
`/tmp/mcp_call.mjs`. Protocol `{id, command, params}` → `{id, status, result|error}`.

### Which of the four load-bearing surfaces bit

- **import** — clean. All four packs fully imported (dark-fantasy 674/674, dungeon-realms
  1221/1221, dwarven-dungeon 434/434, ancient-egypt 884/884 `.fbx.import` sidecars). The FBX
  resolves over the wire as a `PackedScene`.
- **introspection** — **partially bit.** Works on persisted scene content; returns nothing
  dimensional for an un-instantiated asset, which is precisely what a kit swap needs.
- **persistence** — not reached. `save_scene` exists, but there is never anything new to save.
- **skeleton-and-material remap** — not reached.

**Finding for the conductor:** the four-surface taxonomy inherited from the bake-off has a
gap. It assumes a creation primitive exists and asks which surface fails downstream of it. For
M1 the answer is upstream of all four: **there is no authoring primitive to begin with.**
Suggest a fifth surface — *authoring/creation* — in the lap-2 register.

**Honorable fallback engaged:** R1 finished with M3, per the pre-registered protocol.

---

## 2. The measurement instrument (one-time pipeline cost)

`~/Games/reincarnated-godot/scripts/kit_measure.gd` + `scenes/kit_measure.tscn`. Loads a
kit's candidate FBX headless and prints local-space AABBs, accumulating parent-chain
transforms explicitly (`global_transform` reads zero before the headless transform-
notification pass — the same technique `check_crypt_vault_gate1.gd` uses).

**Calibrated against the reference before being trusted.** Run on `polygon-dark-fantasy` it
reproduces every constant hard-coded in `walltop_level.gd` exactly:

| Reading | Probe | `walltop_level.gd` |
|---|---|---|
| floor quarter | 1.249996 × 1.250000 | `FLOOR_Q 1.25` |
| wall | 2.499991 × **3.005743** × 0.225000 | `WALL_LEN 2.5` · `WALL_H 3.005743` · `WALL_THICK 0.225` |
| pillar | 1.082276 × 6.000000 | `PILLAR_NATIVE_W 1.082276` · `PILLAR_NATIVE_H 6.0` |
| topper | 0.582074 × 0.885200, base y 0.011793 | `TOPPER_NATIVE_W/H/BASE_Y` |

An instrument that reproduces the reference constants to six decimals is trustworthy on a new
pack. This is the "measure" half of the skill the run is testing.

---

## 3. R1 — `polygon-dungeon-realms` (built with M3 after the M1 ceiling)

### The wall-run ceiling: FOUND, then CLEARED without touching room geometry

dungeon-realms shares **no** module family with the reference — its own `SM_Env_Dwarf_*` /
`SM_Bld_Ruin_*` vocabulary, on a 5 m grid.

- Primary wall `SM_Env_Dwarf_Wall_01` measures **5.000000 m** long.
  **17.5 / 5.0 = 3.5 segments** — a broken half-segment. This is exactly the failure class
  `walltop_level.gd` documents in its "WHY 14 and NOT 13" comment, hit for real.
- Primary floor `SM_Env_Dwarf_Floor_01..06` measure **5.000 × 5.000 m** → 17.5 / 5.0 = 3.5
  tiles. Same failure.

Per charter §3 I did **not** re-scale the room. Searched the pack for sub-modules instead:

- `SM_Env_Dwarf_Wall_Half_02` = **2.500001** m → **17.5 / 2.5 = 7 whole segments**, matching
  the reference's `WALL_SEGS = 7` exactly.
- `SM_Env_Dwarf_Floor_Half_01` = **2.500000** m → **7 × 7 = 49 tiles = 17.5 m** exactly.

**Ceiling cleared. Room geometry untouched. No HALT required.**

### Re-derived constants (all measured, none assumed)

| Slot | Module | Native | Derived scale → reference value |
|---|---|---|---|
| floor | `SM_Env_Dwarf_Floor_Half_01` | 2.5 sq, top face +0.037299 | 7×7 tiles; Y offset −0.029209 to seat the top face at the reference +0.008090 |
| wall | `SM_Env_Dwarf_Wall_Half_02` | 2.500001 × 5.0 × 0.563997 | **(1.0000, 0.6011, 0.3989)** → 2.5 × 3.005743 × 0.225 |
| pillar | `SM_Env_Dwarf_Pillar_04` | 1.074 × 5.0 | (0.6248, 0.6132, 0.6248) → world foot 0.671011, height 3.065858 |
| topper | `SM_Env_Dwarf_Pillar_Cap_02` | 1.241856 w, base y 0.0 | 0.5511 uniform → world 0.6844 wide |

**Recorded replica cost, visible in the frame:** the DR wall is natively 5 m tall, so meeting
`WALL_H` squashes it 0.601 in Y — the dwarven brick course reads ~40% squatter than the pack's
authored proportion. Horizontal bay (2.5 m) and thickness (0.225) land exactly. The
alternative (`Wall_Short_*`, 5.0 × 2.5) would have needed a 0.5 horizontal squash instead;
vertical compression is the less legible of the two at this camera pitch.

### Three defects caught by looking at the picture

Each was invisible in the build log and only surfaced by cropping the render — the reason the
charter's exit predicate is a frame.

1. **Module origin convention, not just module size.** The reference wall is symmetric about
   its own origin in thickness (z ∈ [−0.1125, +0.1125]). The DR wall is **not**: z ∈
   [−0.142392, +0.421605], origin 0.1396 off centre. Placed with the reference's math both
   leaves sat **5.6 cm proud** — a gap at the inner face, and the outer leaf's top edge
   protruding past the wall-top void cap. Fixed by cancelling the module's own thickness-axis
   origin offset **in its local frame** (local +Z faces outward on N/S but inward on E/W, so
   the correction cannot be applied along `outward`). *Generalised into the builder — every
   later kit inherits the fix.*

2. **The wall-top void cap does not survive a naive kit swap.** Its material samples through
   **world-space UV tiling** (`use_world_uv`, `world_uv_period 1.125`), which is correct for
   the reference kit because dark-fantasy ships a small **separate tiling** stone texture
   (`Textures/Misc/Brick_Small_01.png`). dungeon-realms ships **no tiling stone at all** —
   only 4096×4096 atlases — and world-UV tiling across an atlas walks over its palette-swatch
   strip, rendering a rainbow chunk on the cap once per world period. Fixed with a per-kit
   `cap_tex`: a kit that *has* tiling stone gets the reference material verbatim; an
   atlas-only kit falls back to a solid texture at the reference brick's **measured** mean
   (0.4076, 0.4137, 0.4218), so the cap band lands at the same value under the same
   `stone_tint` and photographic identity holds.

3. **`aura_tint` was a silent no-op for every pilot.** `pilot_rig._tint_aura()` drives aura
   colour via `set_instance_shader_parameter("tint", …)`. The ruled Binbun variants expose
   **no `tint` uniform** — `aura_clip.gdshader` exposes `primary_color` / `secondary_color` /
   `tertiary_color`. Proven by rendering with `--aura=#FF0000` and getting an unchanged white
   aura. The aura light is separately invisible (energy 0.55 against the 5.0/6.0 hero fill
   rig). Applied the hex host-side to the uniforms that actually exist, at the same point the
   harness already swaps the shader for the interior clip. **The rig seam was not modified** —
   logged here for the KT-2/KT-3 rig owner.

### Aura re-pick (drax reasoning-boundary call, charter §7)

Matt ruled "all kits need a selected aura to match them". The KT-2 hexes were chosen with no
room around them.

| Room | KT-2 inheritance | Re-pick | Reason |
|---|---|---|---|
| REF | `#9AA0A6` | *unchanged* | kept as a true control |
| **R1** dungeon-realms | `#9AA0A6` | **`#5AB4E0`** | R1 is a pale sandstone room; the desaturated pale grey rendered white-on-white and stopped reading as an aura at all. Steel-cyan keeps the cyclone's wind/steel identity and separates from warm sand. |
| R2 dwarven-dungeon | `#FF6A1A` | `#FF5A0F` | already separates against cool stone; nudged hotter for the darker room |
| R3 ancient-egypt | `#FF7A24` | `#FF3D1A` | orange sits on top of Egypt's sand+gold palette and would merge; hotter and redder to separate while staying a flame |

R2/R3 picks are provisional until their rooms render.

---

## 4. The I7 tension — reported, not silently resolved

The reference frame Matt has been judging is
`harness_logs/walltop_void_test_v8_2026-06-21/walltop_00_player_cam.png`: the whole box in
view — floor, four walls, void caps, four corner columns — on black void. **That frame was
shot when `FLOOR_TILES` was 6, i.e. a 7.5 m room.** Matt grew the room to 17.5 m on
2026-07-07 for the zoom-register ladder.

At 17.5 m the bit-identical `CAM_DIST 16.5` telephoto (FOV 20, pitch −50, yaw 47) frames
**floor only** — no wall enters the shot. Verified. A frame with no wall in it cannot be
judged for a wall-kit swap, which is this run's entire subject.

So every room ships **both** framings, derived identically across all four rooms:

- **`__cam`** — `CAM_DIST 16.5`. Literally I7, the bit-identical gameplay camera.
- **`__box`** — same pitch / yaw / FOV / aim derivation, dollied back along the same view axis
  to 50 m, reproducing the v8 composition. Eye-picked from a dolly ladder (30 / 34 / 38.5 / 44
  / 50); the naive room-growth ratio 16.5 × 17.5/7.5 = 38.5 still crops the corner columns,
  because the aim point is the occupant stance rather than room centre and the wall height plus
  column crowns add vertical extent the ratio does not model.

Only the dolly distance differs, and it differs identically for every room, so the cross-room
comparison the contact sheet exists for is exact. **Conductor: I7 as written is not satisfiable
against the current room; this is the substitute I chose and why.**

Related: charter **I4 conflates two different numbers**. `interior_half = 8.30` is the
occupant **movement clamp**; the reference clips `king_clip`/`aura_clip` at the wall **inner
face**, `floor_edge * 0.5 = 8.75` (what `playshell.gd` actually passes). Implemented the
reference behaviour and will exercise the box at 8.30 in the `--mode=clip` G2 frames.

---

## 5. Cost ledger so far (KRL-2 split)

| | one-time pipeline cost | R1 method cost |
|---|---|---|
| **M1 attempt** | — | **4 min 11 s** (20:45:06 → 20:49:17), incl. addon repair from tarball, patch re-apply, editor launch, WS client rebuild, 15 wire probes |
| measurement instrument | `kit_measure.gd` authored + calibrated | 1 s to run on DR |
| generator | `kit_replica_level.gd` authored (kit-parameterised fork of `walltop_level.gd`) | — |
| capture harness | `shoot_kit_replica.gd` + contact-sheet compositor authored | — |
| framing decision | dolly ladder shot + eye-picked | — |
| **build → capture → inspect → fix** | 3 fixes generalised into the pipeline (origin re-centring · cap `cap_tex` · aura colour uniforms) | 20:59:27 → 21:08:04 = **8 min 37 s**, of which the large majority is the 3 pipeline fixes that R2/R3 inherit free |

**R1's true marginal cost is not 8m37s.** With the pipeline established, a re-render of R1 is
**~3 seconds** of Godot wall-clock. R2/R3 will show the honest per-room number.

## 6. Artefacts

- `~/Games/reincarnated-godot/scripts/kit_measure.gd` · `scenes/kit_measure.tscn`
- `~/Games/reincarnated-godot/scripts/kit_replica_level.gd` · `scripts/shoot_kit_replica.gd` ·
  `scenes/shoot_kit_replica.tscn` · `scripts/kit_contact_sheet.py`
- `~/Games/reincarnated-godot/harness_logs/kit_replica_2026-07-24/REF_dark-fantasy__{box,cam}.png`
- `~/Games/reincarnated-godot/harness_logs/kit_replica_2026-07-24/R1_dungeon-realms__{box,cam}.png`
- `/tmp/mcp_call.mjs` (WS client, rebuilt)
