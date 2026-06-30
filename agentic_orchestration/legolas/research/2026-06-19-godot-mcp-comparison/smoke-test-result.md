# MCP Smoke-Test Result — satelliteoflove/godot-mcp v4.0.1 → ADOPTED

**Companion to:** `findings.md` (legolas research, same dir)
**Smoke-tested by:** drax (hands-on, reincarnated-godot, 2026-06-19)
**Captured by:** gandalf (commissioner) as part of the MCP-selection decision record
**Verdict:** ALL FOUR acceptance checks PASS. Viable for the vignette PoC. No fallback needed.

---

## Decision-driving fact

reincarnated-godot is on **Godot 4.6.3.stable** — above the 4.5+ hard requirement for Rank 1. The Rank-1-vs-Rank-2 fork is moot; no Godot upgrade, no fall to the runtime-GridMap backup (tugcantopaloglu).

## Checks (all agent-driven over stdio MCP → cli.js → WS:6550 → editor addon; zero editor clicks)

| Check | Result | Evidence |
|---|---|---|
| 1 — scene-tree + transforms | PASS | `godot_node_read get_scene_tree` returned full typed hierarchy; `get_properties` returned real transforms matching authored values |
| 2 — AABB / overlap detection | PASS | `godot_scene3d get_spatial_info` returned engine-computed `global_aabb`; interval-intersection flagged the deliberate overlap, passed the separate control. **Direct fix for the overlapping-crypt failure.** |
| 3 — GridMap (critical) | PASS | `set_cell` item=2 orient=10 round-tripped; `set_cells_batch` of 60 cells → count 0→60; `get_cells_by_item` correct. **Source-confirmed** `addons/godot_mcp/commands/tilemap_commands.gd:568,:662` calls `gridmap.set_cell_item(Vector3i, int item, int orientation 0-23)` — index-based, not string-based, exactly as required. |
| 4 — agent-driven | PASS | initialize handshake + 21-tool list + all calls over stdio; editor log corroborates client connect/disconnect; GUI untouched |

## Setup friction the vignette PoC MUST account for

1. **Spawn `dist/cli.js`, not `dist/index.js`** (`index.js` only exports `main()`). The `npx @satelliteoflove/godot-mcp` config resolves correctly; only bites a hand-wired path.
2. **Lazy background connection** — server returns `tools/list` immediately but connects to the bridge with backoff; gate the first real call (a cheap `godot_project get_info` poll). Self-resolves for an interactive session with the MCP in `.mcp.json`.
3. **Godot editor must be open with the plugin enabled** (it hosts the WS listener; server is the client). Install: `npx @satelliteoflove/godot-mcp --install-addon <project>` → Project Settings > Plugins > enable "Godot MCP".
4. **Enabling the plugin rewrites `project.godot`** — adds `MCPGameBridge` autoload + `[godot_mcp]` block, and in this run **dropped an unrelated `[addons]` sidekick_creator block** (editor normalization). DISCIPLINE: enable in a deliberate, diff-reviewed commit; verify the project.godot diff; don't let the editor silently mutate config.
5. **GridMap orientation is an index 0-23** (24 orthogonal rotations), not Euler. Use `GridMap.get_orthogonal_index_from_basis()` semantics; tool passes the int straight to `set_cell_item`.
6. **`get_scene_tree` is unbounded by default** — on a real scene it dumps the whole tree (180k lines once here). Always pass `max_depth`/`max_children`; for spatial work prefer `godot_scene3d get_spatial_info` with `type_filter`/`within_aabb`/`max_results` (compact AABB text — also the galadriel-judge-friendly channel).
7. **Port 6550 is a hard singleton, one client at a time** (2nd client rejected, WS close 4001, 45s stale-takeover). Fine for one drax session; **if galadriel wants the visual-debug channel concurrently, that is a contention point** — sequence them, or use the sub-agent pattern (sub-agent inherits parent's MCP connection rather than opening a 2nd).
8. **Scene creation is file-first; GridMap cells are base64 in the `.tscn` and CANNOT be hand-edited** — they MUST go through `godot_gridmap_edit`. This *enforces* the structure-first discipline: author the GridMap node + MeshLibrary in `.tscn`, then drive ALL cell placement over the MCP.

## Footprint

Smoke-test-only, fully reverted. project.godot restored byte-identical to HEAD; throwaway `_mcp_smoketest/` + installed `addons/godot_mcp/` removed; only gitignored `.godot/` cache holds transient self-pruning refs. No production scenes touched. The only run failures were two self-inflicted driver issues (wrong entry file; racing the lazy connection) — neither a tool defect.
