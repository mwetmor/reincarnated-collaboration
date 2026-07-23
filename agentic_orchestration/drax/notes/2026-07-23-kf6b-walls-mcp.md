# KF-6b — Walls (in-scene, MCP working mode) + MCP stack update + CaptureRig

Run KIT-FIDELITY · Lane KF-6b · ledger KFL-20 · conductor gandalf · 2026-07-23 · drax (presentation seam)

Repo: `~/Games/reincarnated-godot` (work) · report in `~/Games/reincarnated-collaboration`.
Godot: 4.6.3.stable.official STANDARD (no .NET/Mono). Commit local; conductor pushes.

---

## MATT FIELD REPORT — what this lane fixes
1. Characters perfect — TOUCH NEITHER (rigs + HUD untouched).
2. Walls not snapped to grid. → fixed by placement.
3. Walls not across full floor space. → fixed by placement.
4. Kit/monsters walk through walls. → fixed by placement (replica is playback; presentation cannot impose collision — §8).
5. DIRECTIVE: use MCP / work directly IN the godot scene, live editor, visual verification in loop.

---

## GROUND TRUTH (established before touching anything)

### Scene architecture
- `scenes/replica_playback.tscn` = single Node3D, `script=replica_playback.gd`. Everything (arena, camera, lights, entities, HUD, floaters, grid) built PROCEDURALLY in `_ready()`. So the walls live in CODE, not in the .tscn dressing nodes.
- Sim→world mapping (`replica_playback.gd` header + line ~724): sim `(x_m, y_m)` → Godot `Vector3(x_m, FLOOR_Y=0.0, y_m)`; heading→Y-yaw. Arena spans `[0,0]`→`[w,h]`.
- The dressed arena (`scenes/kt3_arena.tscn` → `render_kt3_arena.gd`) is instanced as child `DressedArena`; it brings the Synty dungeon floor + **perimeter walls** + pillars + arch + bone-deco + the KING lighting register. It is HARDCODED to a 30×30 footprint (`ARENA_W=ARENA_H=30`, `TILE=2.5`, 12 tiles/side).
- Load sequence: `_build_arena_and_camera()` (in `_ready`) instances the dressed arena ONCE at 30×30 BEFORE any fight loads. On fight-load `_load_fight_path()` → `_fit_arena_to_trace()` resizes the Ground plane + Grid overlay to the trace dims — but NEVER re-fits the dressed arena walls. That is the bug.

### Root cause of "walk through walls" + "not full floor" + "not snapped"
- `replica_trace.gd` defaults `arena_width_m = arena_height_m = 44.0` and reads them from the frame header via `frame.get("arena_width_m", 44.0)`.
- **DATA FINDING:** the emitted `replica-frame/v1` frames carry NO `arena_width_m` / `arena_height_m` field (header keys verified: record_type, schema_version, engine_git_hash, fight_key, kit_id, cell, scenario_id, formation_class, composition, policy_arm, seed, tick_size_s, max_duration_s, frame, entities, win_condition, boss_focus_entity_id). So the window falls back to **44×44**. Floor + Grid render at 44×44; the dressed-arena walls sit at 30×30. Entities roam the true recorded range, which exceeds 30 — so they cross the north/east walls, the walls don't span the 44 floor, and the 30-grid vs 44-floor never lines up.

### Recorded position scan (all 40 fights, all ticks; SCAN via python — read-only, frames untouched)
- Global entity CENTER bounds: **x ∈ [7.0, 37.5], y ∈ [1.471, 43.5]**. Entity radius = 0.5 (uniform). → entity EDGES reach **x ∈ [6.5, 38.0], y ∈ [0.97, 44.0]**.
- Per-fight: bowazon/frost-blades/kinetic sets x[7,37] y[5,38]; poison-javazon/caustic sets x[7.7,37.5] y[1.5,43.5].
- All recorded positions fit inside [0,44]×[0,44] (y edge max 44.0 exactly touches the boundary). So the 44×44 fallback IS a correct enclosing arena; the walls just need to be built to it, grid-snapped, full-perimeter, at the boundary.

---

## PART 1 — MCP STACK UPDATE + CONNECTION

### Version update: addon 4.0.1 → 4.1.0
- `npm view @satelliteoflove/godot-mcp version` = **4.1.0** (npx side floats via `-y`; in-project addon was pinned at 4.0.1).
- Pulled the 4.1.0 tarball (`npm pack`), diffed the whole addon tree vs in-project 4.0.1. Same file SET (no files added/removed). Content changed in 4 files only:
  - `plugin.cfg` — version bump 4.0.1→4.1.0.
  - `commands/scene_commands.gd` — NEW command **`reload_scene`** (reload an open scene from disk after a direct .tscn edit, without a heavyweight restart; disk wins over unsaved in-memory edits). Also refactors `save_scene` to a shared `_resolve_scene_path`. **Directly useful for this lane's in-scene edit→reload loop.**
  - `core/mcp_utils.gd` — resource-property resolver now accepts `uid://` refs (not just `res://`); prevents silent load failure when a uid string is handed to a resource-typed property (editor writes uid:// into .tscn since 4.4).
  - `game_bridge/mcp_game_bridge.gd` — upstream RE-ADDS `class_name MCPGameBridge`.
- **Preserved the pre-existing drax patch** in `mcp_game_bridge.gd`: the `class_name MCPGameBridge` collides with the autoload of the same name registered by plugin.gd (`GAME_BRIDGE_AUTOLOAD`) → "Class hides an autoload singleton" parse error whose cascade PRUNES the sidekick_creator block out of project.godot on editor relaunch. Re-verified against 4.1.0: plugin.gd still registers that autoload AND the class_name is still dead (grep: never used as a type). So I took 4.1.0's body (identical to 4.0.1's body) and kept the class_name commented, refreshing the TODO(drax) to cite 4.1.0. `// TODO(drax): remove when upstream drops the dead class_name`.
- Updated the TODO(drax) tracker entry in AGENT_STATE (see §AGENT_STATE below).

### Editor launch + websocket up
- Launched windowed: `/Applications/Godot.app/Contents/MacOS/Godot --path . -e` (background, PID 40964). Log: `harness_logs/_kf6b_editor_launch.log`.
- Plugin already enabled in project.godot editor_plugins (`res://addons/godot_mcp/plugin.cfg`); did NOT need to add it.
- Log confirms: `[godot-mcp] Plugin initialized` + `[godot-mcp] Server listening on 127.0.0.1:6550 [Localhost]`. Port 6550 verified LISTEN (lsof, Godot PID). My class_name patch held — MCP initialized cleanly (no fatal cascade).

### Connection ground-truth (PLUMBING HONESTY)
- **MCP tools are NOT in my (sub-agent) tool surface** — no `mcp__godot__*` functions loaded; this repo's `.mcp.json` is not wired into the sub-agent session.
- **The wire that worked: direct websocket** to `ws://127.0.0.1:6550` via Node 24's native `WebSocket` global (no `ws` npm module available; Node 24 built-in undici WebSocket speaks the client handshake). Protocol: send `{"id","command","params"}`, receive `{"id","status":"success"|"error","result"|"error"}` (one client at a time; server rejects a second with close 4001). Client script: `/tmp/mcp_call.mjs`.
- Handshake response proved the stack live + at the new version: `{"addon_version":"4.1.0","godot_version":"4.6.3-stable (official)","project_name":"reincarnated-godot-spike"}`.
- Editor-viewport capture via MCP works: `capture_editor_screenshot {viewport:"3d"}` → 1024×608 PNG. **BUT** the editor 3D viewport of `ReplicaPlayback` shows only the editor grid gizmo — the arena/walls/entities are built PROCEDURALLY at runtime (`_ready`), so they don't exist in the static editor scene tree (`get_scene_tree` returns just the root Node3D). Therefore meaningful wall verification is on the RUNNING scene, captured by the existing Metal `--capture` harness (a windowed run of the scene) — that is my before/after instrument, complemented by MCP editor captures where a static view helps.

### Isolated-node capture attempt (spec §6 falsification input) — RESULT: NOT SHIPPED
- Tried `capture_isolated_node`, `screenshot_isolated`, `capture_node` over the wire → all `UNKNOWN_COMMAND`. This GDScript server (satelliteoflove @4.1.0) ships only `capture_game_screenshot` (running-scene viewport, via MCPGameBridge debugger session) and `capture_editor_screenshot` (editor 2D/3D viewport). No isolated-node / no 2×2 composite.
- **Decision-shaped (fork):** isolated-node capture is the IvanMurzak/Godot-MCP feature (spec §5 Tier 1) — a **C# editor addon that wants the .NET/Mono Godot build**. We are on 4.6.3 STANDARD. Enabling isolated-node capture = a Godot build switch (STANDARD → Mono), which is a Matt decision (per lane law: ".NET/Mono switch is a Matt decision"). NOT actioned here. Godot MCP Pro ($15) does NOT add isolated-node either (viewport-only) — and NO purchases per law. So the CaptureRig.tscn (Part 3) — the server-agnostic harness that authors the locked rig ourselves — is the correct path on the STANDARD build regardless of the server ranking.

## PART 2 — THE WALLS (fixed by PLACEMENT; replica is playback, §8 — no collision to impose)

### The fix (in-scene, same-scene law — no fork)
Files touched (both my seam):
- `scripts/render_kt3_arena.gd` — `ARENA_W`/`ARENA_H` made RUNTIME (`var`, were `const 30`). New `rebuild(width, height)` re-dresses Floor/Walls/Pillars/BoneDeco to the given dims (env/camera built once in `_ready` are NOT touched). Tiles-per-axis now `ceil(dim/TILE)` (was `round`) so a non-multiple dim covers the FULL floor with no far-edge gap. Walls run the full length of each edge (per-axis tile counts) and sit AT the sim boundary (x=0/W, z=0/H). Arch centered on actual width; bone-deco anchored to the actual perimeter (Fork 3 edges-only preserved).
- `scripts/replica_playback.gd` — `_fit_arena_to_trace()` now calls `_dressed_arena.rebuild(w, h)` after resizing Ground+Grid, so the walls re-dress to the REAL trace dims on every fight-load (the arena is built once at its 30x30 default in `_ready`, then re-dressed here). Also updated `DEFAULT_FIGHT` to a fight that exists in the re-emitted set (see §concurrency below).

### Placement numbers (bounds vs wall line)
- The playback derives arena dims from the frame header; frames carry NO dims → trace fallback **44×44**. So the arena the walls enclose = **[0,44]×[0,44]**.
- Wall line: x=0, x=44, z=0, z=44. Grid-snapped to TILE=2.5 → **18 tiles/side** (`ceil(44/2.5)=18`), **72 wall pieces** (18×2 x-edges + 18×2 z-edges), 324 floor tiles (18×18). (Was: 12/side, 48 walls, 144 floor at the wrong 30×30.)
- Recorded entity CENTER range (scan, all 40 fights, all ticks — read-only): **x[7.000, 37.500], y[1.471, 43.500]**, radius 0.5. Every center is strictly inside [0,44]×[0,44]. Tightest margin: y_hi=43.5 vs wall at 44.0 → **0.5 m** clearance; x_hi=37.5 vs 44.0 → 6.5 m; both low edges ≥ 1.47 m off their walls.

### Wall-crossing scan (evidence) — VERDICT: PASS
- Scanned **126,051 recorded points** across all 40 fights. **VIOLATIONS (center outside the 44×44 wall line) = 0.** No recorded path crosses a wall. No data finding — nothing exceeds the arena bounds (re-verified identical on the re-emitted set: same x[7,37.5] y[1.471,43.5]).

### Visual verification (before/after, my eyes in the loop per the directive)
- BEFORE (`01_BEFORE_walls_30x30_poison-javazon_tick51.png`): walls at 30×30 inside the larger floor; mob skeletons stand ON/THROUGH the east wall; player is south of the south wall — the fight footprint spills past the walled area. Confirms Matt items 2/3/4 exactly.
- AFTER (`02_AFTER_walls_44x44_fire-sorc_tick51.png`): walls span the FULL floor edge-to-edge; the entire mob arc + player are INSIDE the walled perimeter; walls grid-snapped with corner pillars; bone-deco hard against the enlarged perimeter. Items 2/3/4 fixed.
- Captures: Metal windowed `--capture` harness (1920×972). Characters/HUD/floaters untouched (globes, hot-bar, aim-line all intact in the AFTER frame). Also an MCP editor-viewport capture (`04_…`) recorded to document that the editor viewport is empty because the arena is runtime-built.

### Instrument checks — all GREEN (post-edit, post-re-emission)
- Gated smoke (`--smoke`, quit-after 4000): `SMOKE COMPLETE … parse_errors=0`, walls rebuilt 44×44 (72 pcs), clean-exit, 0 errors.
- `check_picker_advance.gd`: PASS (7 distinct fights, scene ALIVE across 6 cycles).
- `check_floater_format.gd`: PASS. NOTE: I retargeted its real-frame sub-check (tick 51→19, and the assertion from "must be null `(—)`" to "well-formed `<amount> (<pct>%|—)`") because the re-emitted frames now CARRY gauge data — the current default renders `359 (94%)` (real pct!), whereas the old bowazon default was pre-gauge `… (—)`. Both are valid floater forms; the null-graceful path is still definitively proven by the SYNTH RECEIVED case (`◆ 3,400 (—)`). See §finding.

### CONCURRENCY — the re-emission landed mid-lane
- Per the guard, a gamora lane replaced `replica-*.ndjson` under me. It landed at ~06:04: the old roster (bowazon/poison-javazon/caustic-arrow/frost-blades/kinetic-fusillade) is GONE, replaced by **fire-sorc / firewall-sorc / flames-of-ignaffar-purifier / cyclone / bonestorm** (40 files, 5 kits × aware|blind × 4 seeds). A `--capture` run mid-swap hit `FileAccess.open err 7` (transient); I waited for writes to quiesce and reloaded. I staged/committed NONE of these frame files. Consequences I absorbed (all on MY files): `DEFAULT_FIGHT` pointed at a now-deleted file → updated to fire-sorc-blind; the floater check's tick-51 assumption → retargeted (above). Scenario geometry is unchanged across the re-emission (same arena bounds), so the wall fix + scan verdict hold verbatim.

### FINDING (surface to knight-rider → engine seam)
- The re-emitted `replica-frame/v1` frames now carry populated `pct` gauge fields on damage events (e.g. fire-sorc tick 19: floater renders `359 (94%)`). The prior set was pre-gauge (`(—)`). This is an engine-output improvement the demo now renders faithfully — no override needed. (Separately, still no `arena_width_m`/`arena_height_m` in the header — the window relies on the 44×44 default. If a fight ever used a non-44 arena, the walls would follow the wrong dims. Recommend the engine emit arena dims in the frame header; until then the 44×44 fallback is correct for the current boss_with_adds scenario. NOT patched — documented.)

## PART 3 — CaptureRig.tscn (spec §2 contract, server-agnostic)

### Authored
- `scenes/CaptureRig.tscn` + `scripts/capture_rig.gd` (procedural, repo one-script pattern). Spec §2.1 rig:
  - neutral turntable pivot at world origin; asset instanced as its child.
  - 4 fixed cameras at 0/90/180/270, framed to the asset AABB (locked framing = comparable reruns).
  - fixed key + fill DirectionalLights (no per-asset relighting).
  - environment PINNED: filmic tonemap, fixed exposure (1.0) + ambient (E0.9), glow at locked strength 0.8.
  - solid neutral background #2b2b2b; 1024 px per side.
  - each angle gets its OWN SubViewport sharing one `world_3d` (all render simultaneously — no camera-toggling, no per-frame await, no re-entrancy; robust).
  - output: N PNGs + a 2×2 composite (spec §2.3) + `asset_meta.json` (aabb_bounds, tri_count, angle_set, resolution — the Judge's non-visual checks).

### Proof capture (one asset through the rig) — WORKS
- Ran the d2 skeleton mob rig (`res://scenes/rigs/mobs/rig_mob_d2_skeleton.tscn`) → 4× 1024×1024 PNGs (a0/a90/a180/a270) + `_composite2x2.png` (2048×2048) + `_meta.json`.
- Proof: `03_CaptureRig_proof_skeleton_2x2.png` (front/right/back/left, locked lighting + framing, #2b2b2b bg — the POLYGON flat-atlas look reads correctly). `_meta.json`: aabb size 1.93×1.70×0.28 m (human-scale), tri_count 3574 — sensible.
- GATE (spec §6.2 ground-truth): the SubViewport returns a **null texture under pure `--headless`** on 4.6.3/M2 — capture needs a render surface. RUN WINDOWED (no `--headless`); the offscreen SubViewport still renders but the process then has a Metal surface. Documented in the script header + a defensive null-guard. (This is the same headless gate the spec §6.2 flagged; settled here empirically: WINDOWED works, headless does not, for SubViewport readback.)
- The full Judge bake-off is a LATER lap; this lane authored the rig + one proof capture only.

## AGENT_STATE / TODO(drax) tracker
- MCP addon updated in-project 4.0.1→4.1.0; the drax `class_name MCPGameBridge` patch in `game_bridge/mcp_game_bridge.gd` is PRESERVED and re-verified against 4.1.0 (collision persists). `// TODO(drax): remove when upstream drops the dead class_name` — carry forward.
- Isolated-node capture: NOT available on the GDScript server; needs .NET/Mono build (Matt fork) — parked, not a demo/loadout override.
- Godot user:// capture outputs: `user://caprig/` (CaptureRig) and `user://kf6b_*_tick51.png` (walls). Committed copies in `agentic_orchestration/drax/captures/2026-07-23-kf6b-walls/`.
