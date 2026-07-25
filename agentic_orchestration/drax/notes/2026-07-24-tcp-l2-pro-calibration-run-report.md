# TCP-L2 — PRO CALIBRATION — run report

**Date:** 2026-07-24/25 · **Agent:** drax (presentation seam) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Charter:** `agentic_orchestration/gandalf/notes/2026-07-24-tcp-l2-pro-calibration-charter.md`
**Program:** `2026-07-24-tool-capability-program-charter.md` — lap **L2**, class **T1 REPLICA** × mode **(i)**
**Status:** COMPLETE — all five exit predicates met. Four predictions resolved; **two resolved against
the charter's expectation**, and one of those (P-D) against it by a factor of three in the *favourable*
direction for Pro, which changes how the rest of the program should read latency.

---

## 0. The exit predicate — the picture

**`~/Games/reincarnated-godot/harness_logs/tcp_l2_2026-07-24/CONTACT_SHEET_tcp_l2.png`**
— PRO | M3 CONTROL | `|PRO − M3| ×4`, one pack, one camera, one lighting rig. **This is the frame to judge.**

Also:
- `PRO_dark-fortress__box.png` · `M3_dark-fortress__box.png` — the two frames at full resolution
- `DIFF_pro_vs_m3__box.png` · `..._x4.png` — raw and amplified difference
- `DIFF_pro_vs_m3.json` — whole-frame mean + six named patch samples
- `silhouette_iou.txt` — geometry registration, isolated from material
- `LATENCY_LEDGER.txt` — per-leg and per-tool wire timings
- `PRO_dark-fortress__cam.png` · `M3_dark-fortress__cam.png` — the literal I7 telephoto framing
  (still floor-only at 17.5 m; see L1 §4, the defect is unchanged)

---

## 1. The verdict, in one line

> **Godot MCP Pro 1.15.1 is an EXECUTOR.** It builds a correct node graph from constants somebody
> else derived, and it cannot derive them. Its only path to a measurement is `execute_editor_script`
> — GDScript over a wire — which makes it **transport for the method that already won, not a rival
> to it.** Every later Pro result in this program must be read as *"given the right numbers, can it
> build."*

---

## 2. The four predictions, each resolved to a fact

### P-A — Pro creates the node graph. **CONFIRMED.**

**1307 of 1307 calls succeeded. Zero failures.** `create_scene` → `open_scene` → `add_node` ×3 →
(`add_scene_instance` + 3 × `update_property` + `set_material_3d`) × 260 → `save_scene`, producing a
776-node `.tscn` (260 `Node3D` instance roots, 260 `MeshInstance3D`, 252 `AnimationPlayer`, 199 KB).
Evidence: `wire_room.jsonl`, `scenes/tcp_l2_pro_room.tscn`.

### P-B — DECISIVE. Pro cannot measure an un-instantiated FBX. **CONFIRMED — and the trap is worse than the plain NO.**

The test the charter specified was run exactly as written: instantiate the pack's wall mesh into a
scratch scene, call `get_node_properties`. **No AABB comes back.** What comes back is:

```
"custom_aabb": "[P: (0.0, 0.0, 0.0), S: (0.0, 0.0, 0.0)]",
"mesh": { "path": "…/SM_Bld_Base_Wall_01.fbx::ArrayMesh_8ce4r", "type": "ArrayMesh" }
```

**`custom_aabb` is shaped exactly like the answer and is not the answer.** It is `GeometryInstance3D`'s
*override* field — position-and-size formatted, identically zero, and unrelated to the mesh's bounds.
An agent that asked "does `get_node_properties` return an AABB?" would find a field with `aabb` in its
name, in `[P: …, S: …]` form, and could take it. The wall it measured would be zero-sized; 280
instances would land at zero scale; **every call would return `ok=true`.** That is the L1 transpose
class verbatim — a silently wrong answer that survives structural inspection.

The rest of the measurement-adjacent surface was probed too, and closes:

| probe | result |
|---|---|
| `get_node_properties` on the instanced `MeshInstance3D` | 19 properties, none dimensional; only `custom_aabb` = zero |
| `read_resource` on the FBX | `{type: "PackedScene", properties: {}}` |
| `get_resource_preview` on the FBX | refuses — *"PackedScene does not have an image preview"* |
| `get_scene_dependencies` on the FBX | `count: 0` |
| `get_collision_info` | empty — no derived extents |
| `analyze_scene_complexity` | node census only, no geometry |
| source grep for `aabb\|bounds\|extents\|bounding` across all 175 tools | **zero matches** |

Evidence: `wire_pb.jsonl`, `wire_pb2.jsonl`, `pb2.err`.

### P-C — the escape-hatch trap. **HATCH WAS NEEDED, AND IT WORKED FIRST TRY.**

```
execute_editor_script → "AABB size=(2.499991, 3.005743, 0.225) pos=(0.0, 0.0, -0.1125)"   [10.01 ms]
```

Six decimals identical to `kit_measure.gd`'s headless reading of the same FBX. So the measurement is
available — by writing GDScript and having Pro relay it. **Verdict class: transport, not rival.**
Recorded per the charter's instruction that this changes the verdict class.

### P-D — ≥32 s of pure wire latency. **NOT CONFIRMED. Measured 10.886 s, and the prediction's premise was the wrong number.**

| leg | calls | wire time | mean | median | max | failed |
|---|---|---|---|---|---|---|
| P-B probe A | 12 | 0.500 s | 41.63 ms | 6.88 ms | 418.19 ms | 2 |
| P-B probe B + P-C hatch | 15 | 0.110 s | 7.34 ms | 4.58 ms | 34.40 ms | 4 |
| **ROOM BUILD (pass 1)** | **1307** | **10.886 s** | **8.33 ms** | **6.99 ms** | 1138.42 ms | **0** |
| post-build inspect | 3 | 0.063 s | 20.86 ms | 13.91 ms | 39.45 ms | 0 |
| surface-1 delta (pass 2) | 255 | 1.826 s | 7.16 ms | 6.71 ms | 91.86 ms | 0 |
| **TOTAL** | **1592** | **13.384 s** | | | | |

Room build by tool: `update_property` 780 calls / 6.466 s · `set_material_3d` 260 / 1.957 s ·
`add_scene_instance` 260 / 1.862 s · `open_scene` 1 / 0.505 s · `save_scene` 1 / 0.065 s.

**Think time is excluded** — these are wire round-trips executed from a call plan. Editor handshake
(2–3 s, the addon's 3 s reconnect timer finding a freshly-spawned server port) is logged separately
and excluded; it is a property of the connection model, not of a call.

**Why the prediction missed.** It was built on the bake-off's measured **114–180 ms/call**. On this
path — stdio to the server, loopback WebSocket to a headless editor on the same machine — the mean is
**8.33 ms**, roughly **14× faster**. `add_scene_instance` on a cold FBX is 8.26 ms, not seconds; the
1138 ms max is a single `update_property` outlier, not the norm (median 7.08 ms).

**Latency is therefore NOT Pro's binding constraint, and the program should stop treating it as one.**
That matters for L5: the T4-UI case for the wire (≈150 ms/nudge vs 15–30 s per script→relaunch cycle)
is *stronger* than charted, not weaker.

**The number that actually decides this lap** is not the wire at all:

> Pro: **10.886 s of wire** to place 260 modules, geometry only, with a Godot editor already running.
> M3: **1.09 s total wall-clock** — process boot, project load, kit derivation, the same 260 modules
> **plus** 28 wall-top void caps, the occlusion-split shader materials, environment, lighting, and a
> JSON dump — measured with `/usr/bin/time`.

**M3 is ~10× faster and does strictly more.** Pro loses this room on throughput even after its per-call
latency came in 14× better than predicted, because the wire needs **5 calls per module** where the
builder needs one expression.

---

## 3. The frames, and what the pixels say

Both rooms are `polygon-dark-fortress`, both driven from the **same transform dump**
(`m3_transform_dump.json`, produced by an actual M3 build), both lit by the **same environment and
lighting rig**, both shot at the **same camera**. One variable: the executor (program law L-H).

### Geometry — Pro placed it correctly

| measure | result |
|---|---|
| silhouette bounding box | PRO `x[134,1807] y[0,1079]` · M3 `x[137,1807] y[0,1079]` — **≤3 px of 1673 px width (0.18%)** |
| `VOID_bg` control patch | `(0,0,0)` in both — the comparison itself is sound |
| amplified diff at the wall faces and corner columns | **black** — those pixels are identical |

Wall runs land on the same pixels; the thin bright lines in the `×4` diff are antialiasing on
high-contrast silhouette edges, not doubled bands. **Silhouette IoU reads 0.879**, but that number is
depressed by bloom, not displacement — the Pro room is blown out (below) and its glow bleeds into the
void, which is why the bbox and the void patch are the honest registration metrics.

### Material — Pro got it wrong, and the failure is silent

| patch | PRO | M3 | \|diff\| |
|---|---|---|---|
| whole frame | `107.07, 105.97, 103.64` | `37.24, 36.25, 34.13` | `69.83, 69.71, 69.51` |
| `FLOOR_CENTER` | `244.5, 243.8, 242.0` | `146.9, 159.3, 155.9` | `97.6, 84.5, 86.1` |
| `FLOOR_NEAR` | `252.5, 248.4, 239.2` | `93.8, 89.2, 81.0` | `158.7, 159.2, 158.2` |
| `WALL_N_far` | `55.1, 55.0, 54.9` | `12.6, 11.7, 11.1` | `42.6, 43.3, 43.8` |
| `WALL_E_right` | `110.3, 106.9, 98.7` | `83.8, 80.7, 73.3` | `26.4, 26.2, 25.4` |
| `COLUMN_W_left` | `57.7, 54.7, 50.8` | `23.5, 20.8, 17.5` | `34.4, 34.0, 33.4` |
| `VOID_bg` | `0.0, 0.0, 0.0` | `0.0, 0.0, 0.0` | `0.0, 0.0, 0.0` |

The Pro room reads **~2.9× brighter over the whole frame** and its floor is blown to near-white. The
diffs are near-uniform across R/G/B — a luminance offset, the signature of a wrong *material*, not a
wrong *position*.

**Root cause, diagnosed and confirmed by measurement.** `SM_Bld_Base_Floor_Quarter_Combined_01` and
`SM_Bld_Base_Wall_01` each carry **two surfaces**. Pro's `set_material_3d` is **single-surface** —
`surface_index`, default `0`. Surface 1 kept the pack's own `A_Wall29` / `A_Wall34` material:
`albedo (0.906, 0.906, 0.906, 0.8)` with **`emission_enabled = true`**. That emissive second surface is
the white floor. The M3 builder's `_apply_single_tex` walks `mesh.get_surface_count()` and overrides
**every** surface.

**This is P-B's consequence one level down.** To dress a module correctly over the wire you must know
its *surface count*, and Pro has no tool that reports one — the same missing introspection that stopped
it measuring dimensions stops it dressing meshes. It is not enough to hand an executor the room's
dimensions; you must hand it the mesh topology too.

---

## 4. The second Pro pass — and a silent no-op worse than the first failure

Having diagnosed the surface gap, I re-swapped to Pro and fired a delta: 252 × `set_material_3d` with
`surface_index: 1`, on node paths **Pro itself had reported in pass 1**.

**255/255 calls returned `ok=true`. Zero `surface_material_override/1` entries were written. The
rendered frame did not change by one pixel.**

Cause: Pro's `add_scene_instance` calls `NodeUtils.set_owner_recursive`, promoting every internal node
of the instanced FBX to scene-owned. On save that writes the subtree out explicitly *and* keeps the
`instance=ExtResource(...)` line. On reload Godot re-instances the PackedScene **and** loads the saved
duplicates, which collide and are renamed — `SM_Bld_Base_Floor_Quarter_Combined_01` becomes
`…_02`, `AnimationPlayer` becomes `AnimationPlayer2`. So every node path Pro emitted in pass 1 resolves
in pass 2 to the *re-instanced* node, which is not scene-owned and is therefore **not serialized**. The
call mutates a node that will never be saved and reports success.

Stated plainly:

> **A scene Pro authors does not round-trip through Pro.** Its own reported node paths are invalid on
> the next session, and the tools that target them fail silently with `ok=true`.

For a program whose T2 EXPANSION lap (L4) is *"open an existing scene and modify it in place"*, this is
the single most consequential finding in the run after P-B. **L4 must not assume a Pro-authored scene
is re-addressable by Pro.**

The frames shipped are therefore the **pass-1** room; pass 2 changed nothing.

---

## 5. Three more Pro behaviours found in execution, all silent

**(a) `create_scene` does not open the scene it creates.** The documented assembly loop —
`create_scene → add_node → add_scene_instance → update_property → save_scene` — omits `open_scene`.
Following it verbatim, my first P-B probe created `_tcp_l2_pb_probe.tscn`, then instanced the wall FBX
into **`crypt_vault_node_baked.tscn`**, a 1943-node scene the editor had restored from its previous
layout. Every call returned `ok=true`. The only tell was the `scene_path` field echoed back by
`get_scene_tree`. Had the plan reached its `save_scene`, it would have written the pollution to disk.
It did not — the run was cut short by an unrelated pipe close — and the file is verified unmodified.

This is a genuine blast-radius hazard for autonomous use: **the target of every Pro authoring call is
implicit editor state, not an argument.** All subsequent plans in this lap open the scene explicitly
and verify the echoed `scene_path` before writing.

**(b) Enabling the Pro addon rewrites `project.godot`.** It injects three autoloads — `MCPScreenshot`,
`MCPInputService`, `MCPGameInspector` — into the `[autoload]` section, replacing what was there. After
restore those point at files that no longer exist. **Swap residue is not confined to `addons/`.**
Caught and restored from a pre-swap snapshot (§7).

**(c) Removing an addon silently empties the global class-name cache.** After restore, the incumbent's
files were byte-identical yet the project threw `Could not find type "MCPFrameProfiler"` on every run —
because `.godot/global_script_class_cache.cfg` had been rewritten without the incumbent's `class_name`
registrations while Pro was installed. A file-level restore does not restore it; an editor rescan does.
**Add "rescan and re-verify the class cache" to the L-J restore procedure** — a byte-perfect addon
restore is necessary but not sufficient.

---

## 6. LOUD — an L-B event: the Pro manifest disagrees with `docs/tools-reference.md`

The charter names this a HALT-and-surface condition worth more than the lap. Surfacing it.

**`docs/tools-reference.md` documents 77 tools. The server registers and exposes 175.** Confirmed at
the source (`server/src/tools/*.ts`, 175 `server.tool(` registrations), in `package.json`
(*"Premium MCP server … with 175 tools"*), and **over the wire** (`tools/list` → 175;
`pro_tools_list.json`). The addon logs `Registered 174 commands`.

The audit that set this lap's expectations read the docs file. Three of its conclusions do not survive
the source:

| audit §3 claim | actual |
|---|---|
| Pro has **no GridMap** — *"tilemap is 2D only"* | **`add_gridmap` exists** (`scene-3d-tools.ts`) |
| — | **`batch_add_nodes` exists** — a batching primitive the latency arithmetic never modelled |
| escape hatch is `execute_editor_script` → editor | **plus `execute_game_script`** → the running game, a *second* hatch |

Undocumented families found in source, several bearing directly on later laps:

- **3D:** `add_mesh_instance` · `setup_lighting` · `setup_environment` · `setup_camera_3d` ·
  `set_material_3d` · `add_gridmap`
- **VFX (→ L7):** `create_particles` · `set_particle_material` · `set_particle_color_gradient` ·
  `apply_particle_preset` · `get_particle_info`
- **Motion capture (→ TCP-8's blocker):** `record_frames` · `start_recording` · `stop_recording` ·
  `replay_recording` · `compare_screenshots`
- **Also:** physics (6), navigation (5), audio (6), animation-tree (8), input-map (2), test/assert (5),
  android (3), analysis (6), `get_editor_camera` / `set_editor_camera`, `batch_get_properties`,
  `cross_scene_set_property`, `find_nearby_nodes`, `search_in_files`, `validate_script`

**Three documented schemas also disagree with the wire** — `batch_get_properties` (docs: `type` +
`property`; wire: `nodes[]` of objects), `setup_collision` (docs: `shape_type`; wire: `shape`),
`find_nearby_nodes` (docs: `node_path`; wire: requires `position`). All three failed validation on
docs-shaped arguments. **Read the manifest from source, and confirm each schema at the wire before
building a plan on it.**

**What this does NOT change:** there is still **no bounds/AABB tool** in the 175. P-B stands, now on
the full surface rather than the documented subset.

**What it does change:** `add_gridmap` means the L4 GridMap prediction is **not W-MUR-exclusive** — if
GridMap authoring really is transpose-proof by construction, Pro can be scored on it too, and L4 can
be a genuine three-way instead of two-plus-a-control.

---

## 7. The instrument swap, and the restore predicate

Recorded **before touching anything**, per §4.1 — inventory, not version string:

```
addons/godot_mcp   74 files · 36 .gd · 327,576 bytes
manifest sha256    2f0f0e3a50aa5f34a6c0faa426bacb4e9ff1378d6b559848da08484b3a2f7257
project.godot      a76d666a4a3ece81d508d0a0a183d6674bf6d8ad9509cdb55b01233f81ae2680
```
(`harness_logs/tcp_l2_2026-07-24/incumbent_inventory.sha256`, `project.godot.pre-swap`)

Swapped **twice** (pass 1, then the pass-2 surface delta). Incumbent moved aside, never deleted; Pro
installed from `~/Games/vendor/godot-mcp-pro-v1/addons/godot_mcp` (44 files, 35 `.gd`, v1.15.1).

**RESTORE VERIFIED — three times, against the inventory:**

- after swap 1: **74 files / 36 `.gd`, byte-identical** — `diff` clean
- after swap 2: **74 files / 36 `.gd`, byte-identical** — `diff` clean
- final, post-rescan: **74 files / 36 `.gd`, byte-identical** — `diff` clean
- `project.godot` sha256 `a76d666a…` — **matches the pre-swap record exactly**
- class-name cache re-registered (48 `MCP*` entries); `kit_measure.gd` on the reference pack
  reproduces every calibration constant to six decimals (`WALL_H 3.005743`, `FLOOR_Q 1.249996`,
  `PILLAR 1.082276 × 6.0`, topper base `0.011793`) — **the probe is still sound**

`project.godot` shows as modified in git, unchanged from how the session found it (a pre-existing
`[rendering] mesh_lod` removal). Nothing of mine is in that diff.

**No HALT was required.** Pro's addon copies are parked at `~/Games/vendor/_tcp_l2_pro_addon_USED{,2}`
and the incumbent backup at `~/Games/vendor/_tcp_l2_incumbent_godot_mcp_backup`; all three are outside
the Godot project and safe to delete.

---

## 8. The pack pick was a measurement — and it inverted the shortlist again

Ran `kit_measure.gd` across five candidates plus the reference before choosing (law L-D). Full log:
`harness_logs/tcp_l2_2026-07-24/pack_measure.log`.

| pack | FBX count | wall module | 17.5 m ÷ wall | verdict |
|---|---|---|---|---|
| **polygon-dark-fortress** | 1399 | `2.499991 × 3.005743 × 0.225`, origin z −0.1125 | **7.0000** | **PICKED** |
| polygon-samurai-empire | 1254 | identical | 7.0000 | viable, runner-up |
| polygon-ancient-empire | 804 | identical | 7.0000 | no quarter floor, no wall trim, no roof cap |
| polygon-elven-realm | 828 | identical | 7.0000 | no quarter floor, no wall trim |
| polygon-dungeon | **830** | `SM_Env_Wall_01` = **0.052 × 0.052 × 0.004** | — | **unusable** — centimetre-scale, no `SM_Bld_Base_*` family at all |

`polygon-dungeon` has more FBX assets than `ancient-empire` or `elven-realm` and is the only one of the
five that cannot build the room at all. **L-D holds for a second lap running:** catalogue count and
module compatibility are uncorrelated.

**dark-fortress won on four measured properties, not on taste:**
1. wall `2.499991 × 3.005743 × 0.225` with origin z `−0.1125` — **byte-identical to the reference**, so
   the derived wall scale is `(1, 1, 1)` exactly and the L1 origin-convention defect cannot recur;
2. quarter floor `1.249996`, top face `+0.008090` — 14 tiles/side, **no y-fix needed**;
3. it is the only shortlisted pack shipping **both** a genuine tiling stone (`Brick_Small_Texture_01`)
   **and** a tiling floor (`FloorTiles_Texture_01`), so L1's void-cap defect #2 — world-UV tiling
   walking across an atlas — does not recur and **no `cap_tex` substitution is needed**;
4. its pillar (`3.015154` native against the reference post's `6.0`) is the one module that forces a
   real re-derivation, keeping the lap from being a trivial copy.

**Contamination guard satisfied** (charter §2 / TCP-10): grepped both repos before picking — no
architecture constant for any candidate existed on disk, and `kit_measure.gd`'s `KITS` table held only
the four burned packs. dark-fortress's constants were first written in **this** lap's commit, after the
Pro attempt. Pro could not have read the answer.

**Bonus, not a criterion:** dark-fortress renders genuinely dark. All three L1 rooms read pale tan
against a dark reference, which is the open H1 register question. This one does not. That is one data
point toward H1 and is offered as such, not as an answer.

---

## 9. What the Pro build's scope was, declared

Pro was given the geometry and the constants; it was **not** asked to build:

- the **28 wall-top void caps** (procedural `BoxMesh` + `ShaderMaterial`, ~10 parameters each)
- the **occlusion-split / south-dissolve ShaderMaterials** on walls and the three occluding columns
- **environment and lighting** — supplied identically to both rooms by the harness
  (`KitReplicaLevel.build_env_only()`), so the diff measures the executor and not the exposure

Excluded deliberately and stated here rather than dropped quietly. They are why the M3 frame carries
detail the Pro frame does not; they are **not** why the Pro floor is white (§3).

Also declared: the Pro plan was **generated from an M3 transform dump**, not hand-aimed. That is not a
concession — it *is* what "executor" means, and it is the only way to hold the variable at one. If I
had hand-typed 1307 calls, a typo would be indistinguishable from a wire defect.

---

## 10. Charter defects and things that could not be satisfied

The conductor asked for this explicitly. Three items.

**(1) P-D's premise was stale, not its arithmetic.** `~280 instances × 114–180 ms` is sound arithmetic
on a wrong constant. The bake-off's figure did not survive re-measurement on this path (8.33 ms mean,
14× faster). Nothing was worked around — the prediction is simply recorded as not confirmed, with the
measurement that replaced it. **Recommendation: re-measure per-call latency at every lap that predicts
on it (L-C already says verdicts expire; this shows the *numbers* expire too).**

**(2) The charter's decisive test is necessary but not sufficient, and the lap found the sufficient
one by accident.** §3's P-B is *"instantiate → `get_node_properties` → does an AABB come back?"* It came
back NO, correctly. But the same missing introspection failed a second time, one level down and in a
place the charter did not anticipate: **you cannot dress a mesh over the wire without knowing its
surface count**, and Pro has no tool that reports one. The white floor is that second failure, and a
lap that had stopped at the charter's literal predicate would have shipped a frame it could not explain.
**Suggest the author/executor test generalise to: can the tool discover the properties of an asset it
has never seen — dimensions, surface count, node structure — or must all three be supplied?** For Pro
the answer is all three.

**(3) I7 remains unsatisfiable, unchanged from L1, and I did not re-litigate it.** The reference frame
predates Matt growing the room 7.5 m → 17.5 m; at 17.5 m the bit-identical `CAM_DIST 16.5` telephoto
frames floor only. Both `__cam` frames were captured and are shipped for completeness; both are
wall-free and neither is judgeable for a wall swap. The `__box` framing (identical pitch/yaw/FOV/aim,
dollied to 50 m) is the deliverable, applied identically to both rooms. **This is now the second
consecutive lap blocked on the same defect — it wants a ruling, not a workaround.**

---

## 11. What this changes for the rest of the program

1. **Every later Pro lap reads as *"given the right numbers, can it build."*** Pro can build. It cannot
   find out what to build. Where a lap needs asset discovery, Pro needs a supplier — and today the only
   supplier is M3.
2. **L4 (T2 EXPANSION) has a new precondition.** A Pro-authored scene does not round-trip through Pro
   (§4). Before L4 assumes "open an existing scene and modify it", verify Pro can re-address nodes in a
   scene *it* wrote. On this evidence it cannot.
3. **L4 can be a real three-way.** `add_gridmap` exists (§6). The transpose-proof-by-construction
   prediction should be scored on Pro as well as W-MUR.
4. **L5 (T4-UI) is a stronger case for the wire than charted.** 8.33 ms/call, not 150 ms. Pro also has
   `get_editor_camera` / `set_editor_camera` and `compare_screenshots`, undocumented.
5. **TCP-8's motion-harness blocker needs re-scoping.** Pro ships `record_frames` / `start_recording` /
   `stop_recording` / `replay_recording`. TCP-8 says the harness must be ours or the laps score capture
   rigs — that ruling still stands, but it should be made knowing Pro has a rig, not assuming it doesn't.
6. **L-J needs a fourth clause.** Restore-by-inventory is necessary and insufficient: swap residue also
   lands in `project.godot` (§5b) and in `.godot/global_script_class_cache.cfg` (§5c). Proposed addition:
   *snapshot `project.godot` with the inventory; after restore, rescan the project and re-verify the
   class cache and a smoke run.*
7. **Autonomous Pro use carries an implicit-target hazard.** `create_scene` does not open; every
   authoring call targets whatever scene is open; wrong-target calls return `ok=true` (§5a). Any Pro
   lap must open explicitly and verify the echoed `scene_path` before writing.

---

## 12. Cost ledger

| phase | cost |
|---|---|
| manifest re-read from source + wire `tools/list` (L-C) | ~6 min |
| pack measurement across 6 kits + pick | ~5 min |
| incumbent inventory + hash + verified backup | ~3 min |
| swap 1 + headless editor + `pro_mcp_client.mjs` authored | ~12 min |
| P-B / P-C probes (2 plans, 27 calls) | ~4 min |
| M3 kit entry + transform dump + plan generator | ~8 min |
| **Pro room build over the wire** | **10.9 s wire / ~1 min wall** |
| swap 2 + surface-1 delta + swap back | ~9 min |
| restore ×2 + rescan + verification + smoke | ~6 min |
| capture ×2 + contact sheet + pixel diff + IoU | ~9 min |
| **M3 control build (the comparison number)** | **1.09 s** |

**Total ~65 min.** The two numbers that matter are the last two: **10.9 s of wire against 1.09 s of
process**, for a room the wire built less of.

---

## 13. Artefacts

Code (`~/Games/reincarnated-godot/`), commit `c53b954`:
- `scripts/pro_mcp_client.mjs` — stdio MCP client + per-call latency ledger (`--list` / `--call` /
  `--plan` / `--wait`). Claude Code loads `.mcp.json` at session start, so a mid-session server cannot
  become agent tools; this is the same wire, driven from a client that can also timestamp it.
- `scripts/tcp_l2_dump_plan.gd` + `scenes/tcp_l2_dump_plan.tscn` — M3 transform dump (260 modules)
- `scripts/tcp_l2_gen_pro_plan.py` — dump → 1307-call Pro plan
- `scripts/tcp_l2_diff.py` — contact sheet + whole-frame mean + six named patch samples
- `scripts/_tcp_l2_surf_probe.gd` — the surface-count/material probe that diagnosed the white floor
- `scripts/kit_measure.gd` — +5 candidate kits (paths only, no dimensions)
- `scripts/kit_replica_level.gd` — `dark-fortress` kit entry (measured) + `build_env_only()`
- `scripts/shoot_kit_replica.gd` — `mode=tcpl2`, `env_kit` for wire-authored rooms
- `scenes/tcp_l2_pro_room.tscn` — **the room Pro authored** (776 nodes, 199 KB)

Captures + evidence: `~/Games/reincarnated-godot/harness_logs/tcp_l2_2026-07-24/`
— frames, diffs, `DIFF_pro_vs_m3.json`, `silhouette_iou.txt`, `LATENCY_LEDGER.txt`,
`pro_tools_list.json` (175), all five `wire_*.jsonl` ledgers, all call plans,
`incumbent_inventory.sha256`, `project.godot.pre-swap`, editor/capture/rescan logs.

Commit: `c53b954` (local, **not pushed** — Matt-gated).
