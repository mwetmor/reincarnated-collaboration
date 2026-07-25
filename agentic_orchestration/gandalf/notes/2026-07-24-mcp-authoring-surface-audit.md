# MCP authoring-surface audit — the two servers are near-complementary, and neither can do the job alone

**Date:** 2026-07-24 · **Author:** gandalf (`ARCHITECT`) · **Method:** source-manifest read, no run
**Trigger:** Matt, after KIT-REPLICA LAP-1: *"Which MCP-type-tool was used for each set of images? I'm confused."*
**Cost:** minutes. **What it corrects:** a canon-level claim I made from one server's behaviour.

---

## 0. What prompted it

LAP-1's M1 leg failed and I reported the ceiling as a property of *the wire*. Matt's question exposed
that lap 1 tested **one** MCP server against **two non-MCP methods** — while his ruling had asked to
*"see how the agent does when working with the different MCP-like tools."* He chose the audit over
another run. Correct call: **the audit answered most of it without spending a lap.**

## 1. THE CORRECTION

> **I wrote:** *"the wire inspects, it does not build."*
> **True of:** `@satelliteoflove/godot-mcp` 4.1.0 (the incumbent).
> **False of:** MCP as a category. **Godot MCP Pro 1.15.1 has a complete authoring surface.**

`create_scene` → `add_node` → `add_scene_instance` → `update_property` → `save_scene`. That is a
full assembly loop, documented, in a server we already own and have shelved.

Generalising one implementation's limit to a category is the same error class TRUE-SOURCES exists to
prevent. It went into a tracker entry and a message to Matt within an hour of the run closing.

## 2. Evidence — read from source, not from docs or recollection

**Incumbent 4.1.0** (`~/.npm/_npx/…/@satelliteoflove/godot-mcp/dist/tools/`). Tools are *namespaced
verb-dispatchers*, not one-tool-per-verb — so drax's over-the-wire probes of `create_node`/`add_node`
were probing names this server never exposes. **His verdict survives anyway**, now confirmed at the
source: the dispatcher's own operation set is

- `godot_node_edit` → `find` · `get_properties` · `get_scene_tree` · `reparent` · `update`
- `godot_scene` → `open` · `reload` · `save`
- `godot_resource` → `get_info` (one operation — confirming no AABB from an un-instantiated FBX)
- `godot_scene3d` → `get_bounds` · `get_spatial_info`
- `godot_game_time` → `freeze` · `thaw` · `status` · `step` · `step_until`
- module list: animation, docs, editor, exec, game-time, input, node, profiler, project, resource,
  runtime-state, scene, scene3d, tilemap, validate-meshes — **there is no gridmap module.**

**No create. No add. No delete. No instantiate.** Read/update/reparent only.

**Pro 1.15.1** (`~/Games/vendor/godot-mcp-pro-v1/docs/tools-reference.md`, 77 documented tools):
`create_scene`, `add_node`, `add_scene_instance`, `delete_node`, `add_resource`, `rename_node`,
`update_property`, `batch_set_property`, `save_scene`, `execute_editor_script`,
`get_editor_screenshot`, `capture_frames`, full shader suite, theme suite, export suite, 2D tilemap
suite. **No gridmap. No AABB/bounds tool. No game-clock control.**

**IvanMurzak: not on disk.** Only NuGet HTTP-cache entries for `com.ivanmurzak.mcpplugin` 7.3.0
survive. A three-way needs a reinstall; the bake-off closed it (P3 no-batch FAIL, P4 FAIL).

## 3. The split — and it is almost comic

| What the assembly program needs | Incumbent 4.1.0 | Pro 1.15.1 |
|---|---|---|
| create scene / node / instance / resource | **✗ none** | **✓ all four** |
| set property | ✓ `update` | ✓ + `batch_set_property` |
| persist | ✓ `scene save` | ✓ `save_scene` |
| **3D bounds — measurement** | **✓ `scene3d get_bounds`** | **✗** |
| GridMap (Godot's native 3D modular primitive) | ✗ no module | ✗ tilemap is 2D only |
| **game-clock freeze/step** (KT-5 conductor-eye law) | **✓ freeze/thaw/step/step_until** | **✗** |
| shaders · screenshots · export | ✗ | ✓ |
| mesh validation | ✓ `validate_meshes` | ✗ |
| escape hatch | `godot_exec` → *running game* | `execute_editor_script` → *editor* |

- **The incumbent can measure and cannot create.**
- **Pro can create and cannot measure.**

LAP-1's core skill is *measure a new kit, re-derive the constants, build.* **Neither server can do
both halves.** And the 70 hardcoded `res://addons/godot_mcp/` refs still forbid them coexisting as
standing stacks — they can only be swapped for a lap.

## 4. The two unknowns worth a run — and the one that is already knowable

**UNKNOWN-1 (decisive).** Pro *can* instantiate. So it could instantiate an FBX into a scratch scene
and read `get_node_properties`. **Does that return an AABB?** If yes, Pro has a complete — if
roundabout — measure→build loop. If no, Pro is an **executor** of constants derived elsewhere, not an
author.

**UNKNOWN-2 (the trap).** Pro has `execute_editor_script`. That trivially yields an AABB. But then
you are writing GDScript over a wire — **which is M3 with added latency.** If the escape hatch is
required, the honest verdict is *MCP is a slow transport for the method that already won*, not a
rival to it.

**ALREADY KNOWABLE — throughput.** LAP-1's R2 room is ~280 instances. At the bake-off's measured
114–180 ms/call that is **32–50 seconds of pure wire latency** before a single measurement, decision
or capture. M3 built, dressed and captured an entire room in **1 min 37 s total.** So a
fully-capable Pro is at rough parity *at best* on one room — and loses by orders of magnitude at the
10³ nodes of a dungeon floor or the 10⁴ of a catalogue sweep.

**This does not make the run pointless.** *"It can, but 20× slower"* is a materially different
finding from *"it cannot"*, and Matt's standing intent is to find the end of each tool's capability,
not to pick a winner. But it does mean lap 2 should be **one room, not three.**

## 5. Recommendation (fork; Matt rules)

**Lap 2 = single room, single method, against a control.** One new pack; Pro authors the room; an M3
build of the *same* room is the control; diff the frames. That makes LAP-1's hardest lesson
operational — the M2 transpose was caught only by a rendered frame against a control, and structural
verification passed clean while every rotation was mirrored.

Pre-registered: **(P-A)** Pro creates the node graph — high confidence, tools documented ·
**(P-B)** Pro cannot measure an un-instantiated FBX; the instantiate→`get_node_properties` path is
the decisive test · **(P-C)** if measurement needs `execute_editor_script`, verdict is *transport,
not rival* · **(P-D)** wire latency ≥ 32 s for the instance placements alone.

**Standing alternative Matt should weigh against it:** H1 — the register question — decides whether
this asset library can carry act-grade variety at all. That is a *product* question; this is a
*tooling* one.

---

**Signed:** gandalf, 2026-07-24. The audit cost minutes and corrected a claim I had already committed
to a tracker. Read the manifest before generalising from behaviour.
