# Godot MCP Server Comparison — for agent-driven scene authoring

**Commissioned by:** gandalf (design steward), Pattern B dialogue 2026-06-19
**Researched by:** legolas (Mode A, analytical, read-only)
**Captured by:** gandalf on legolas's behalf (sub-agent file-write policy blocked direct write; capture is durable per OP § 2 Pattern A-deep file-write-constraint pattern)
**Status:** decision-ready research; hands-on download/install/smoke-test is drax's follow-on

---

## Context

reincarnated-godot authors ARPG scenes via an agent (drax) working largely "blind" — writing `.tscn`/`.gd`, rendering snapshots, scoring them, with no engine ground-truth in the loop. This open-loop authoring produced spatial-coherence failures the project owner rejected on sight:

1. ~50 identical large "crypt" assets placed overlapping around every room's perimeter
2. doors half-occluded by walls (socket/grid misalignment)
3. second-floor geometry at wrong heights, unpassable, clipping through everything (stairs / vertical-layer problem)

Root cause: free-placement instead of snap-to-grid structure discipline + no engine-truth spatial introspection. The fix is to have drax author **inside** a Godot MCP so he has engine ground-truth (real transforms, collision/AABB, scene tree) and can drive **GridMap-based** structure-first authoring. galadriel may also use the MCP's visual-debug path as a judge input channel.

## Two critical (disqualifying) requirements

- **#4 GridMap manipulation** — must READ cells and DRIVE `set_cell_item(Vector3i, item_index, orientation)`. Our structure-first discipline IS GridMap. No GridMap = wrong tool, regardless of other strengths.
- **#7 Agent-drivable** — usable by a coding agent via MCP protocol (stdio/HTTP), not human-in-editor only.

---

## DISQUALIFIED

| Candidate | Reason |
|---|---|
| **GDAI MCP** (3ddelano / gdaimcp.com) | **#4 FAIL.** No GridMap cell manipulation documented anywhere (product site, blog, README, aggregators). Covers scene/node creation, property control, screenshots, script-gen — GridMap entirely absent. Strong visual debugging + editor control, but cannot be the primary authoring MCP. *Could* be layered as a supplementary visual-debug-only channel if the team ever runs two MCPs. **(This was the owner's lead candidate — disqualified on the one capability that is load-bearing for our fix.)** |
| bradypp/godot-mcp | #4 FAIL — MeshLibrary export at best; no GridMap cell read/write |
| Coding-Solo/godot-mcp | #4 FAIL — same |
| FunplayAI/funplay-godot-mcp | #4 FAIL — same |

---

## Ranked shortlist

### Rank 1 — satelliteoflove/godot-mcp
`github.com/satelliteoflove/godot-mcp`

- **GridMap: CONFIRMED at EDITOR time.** `godot_gridmap_read` (list nodes, MeshLibrary info, read cells) + `godot_gridmap_edit` (set single cell w/ MeshLibrary item + orientation, batch-set, clear, clear-all). Exact API surface for structure-first authoring. Editor-time (not runtime) matters for scene authoring.
- **AABB/bounds: CONFIRMED** via `godot_scene3d` (engine-computed bounding boxes) — directly addresses the overlapping-crypt failure.
- **Scene-tree introspection: CONFIRMED** (`godot_node_read`, incl. instanced sub-scenes).
- **Visual debugging:** screenshots + structured JSON runtime state (token-cost-minimized; useful for galadriel).
- **Agent invocation:** stdio via `npx @satelliteoflove/godot-mcp`; WebSocket:6550 bridge to a Godot addon. CONFIRMED.
- **Godot version: 4.5+ HARD requirement** (uses 4.5 Logger class). **MUST be verified against the project — this is the gating fact.**
- **License:** MIT (clean for commercial).
- **Maturity:** 105 stars; v4.0.1 released 2026-06-14 (freshest in the field); actively maintained.

### Rank 2 — tugcantopaloglu/godot-mcp
`github.com/tugcantopaloglu/godot-mcp`

- **GridMap: CONFIRMED but at RUNTIME** (`game_gridmap` — set/get/clear, query used cells). Game must be PLAYING — adds friction vs Rank 1's editor-time authoring.
- Scene tree, transforms, physics queries (raycast, area intersections): CONFIRMED. 149 tools / 19 categories.
- **Agent invocation:** stdio via `node build/index.js`; TCP:9090 to a Godot autoload. CONFIRMED.
- **Godot version:** 4.x; 4.4+ for UID features. (Lower version bar than Rank 1.)
- **License:** MIT. **Maturity:** 282 stars; v2.0.0 2026-03-02; actively maintained.
- **Use case:** best backup if Rank 1's 4.5+ requirement blocks; or a runtime-layer complement.

### Rank 3 — Godot MCP Pro (youichi-uda) — CONDITIONAL
- **GridMap: UNVERIFIED.** `add_gridmap` creates a GridMap node; `tilemap_set_cell` / `tilemap_get_cell` exist — but TileMap and GridMap are DISTINCT node types. No confirmed `gridmap_set_cell`. If `tilemap_*` dispatches to GridMap → rises; if not → DISQUALIFIED on #4.
- Strong elsewhere: 444 stars; v1.14.0 2026-05; UndoRedo integration; editor + game screenshots + **screenshot comparison** (interesting for galadriel); `execute_editor_script` for arbitrary GDScript.
- Proprietary; **$15 one-time**; commercial use per standard Godot Asset Store terms. Godot 4.4+.

---

## Smoke-test priorities (drax — hands-on, on a throwaway scene)

1. **Does reincarnated-godot run Godot 4.5+?** (Gates Rank 1. THE decision-driving fact.)
2. Does satelliteoflove's `godot_gridmap_edit` correctly call `set_cell_item` with MeshLibrary item index + orientation (not just string-based)? Test batch-set with 50+ cells.
3. Does Godot MCP Pro's `tilemap_set_cell` work on GridMap nodes, or is it strictly TileMapLayer? (Only if Rank 1 + Rank 2 both have problems.)

Plus the agreed acceptance criterion: the MCP must demonstrably (a) read scene tree + real transforms, (b) detect a deliberately-overlapping mesh pair via AABB/collision, (c) place + read GridMap cells via `set_cell_item`, (d) all driven by the agent, not a human. Pass all four → viable for the vignette PoC.

## Next action

drax confirms the project's Godot version, then smoke-tests Rank 1 (satelliteoflove) against the four-part criterion + the three priority checks. Selection is made on drax's test results. If the project is below 4.5, the branch is: upgrade Godot to 4.5+ (to use Rank 1) **vs** adopt Rank 2 (runtime-GridMap, 4.4+) — an owner decision the version-check will surface.
