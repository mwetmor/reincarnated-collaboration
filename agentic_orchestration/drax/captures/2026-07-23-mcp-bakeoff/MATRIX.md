# MCP-BAKEOFF — capability matrix (drax, executor)

**Date:** 2026-07-23 · **Charter:** `agentic_orchestration/gandalf/notes/2026-07-23-mcp-bakeoff-run-charter.md` (RATIFIED) · **Conductor:** gandalf · **Executor:** drax
**Common test scene:** `reincarnated-godot` (Godot 4.6.3) — `kt3_arena.tscn`, `CaptureRig.tscn`/`capture_rig.gd`, d2-skeleton (`res://scenes/rigs/mobs/rig_mob_d2_skeleton.tscn`).
**Host:** Mac mini (Apple Silicon), macOS, Metal / Forward+ renderer.

---

## Verdict line

**Both reachable columns FILLED (2 of 3). Incumbent = baseline-proven, runtime-capable, structure-first native. IvanMurzak = FULLY LIVE on this host (NOT BLOCKED-ENV — the .NET toolchain stood up and the MCP round-trip ran end-to-end), a strong editor-time authoring + reflection instrument, but weak on the project's proven needs: its one native isolated-capture tool renders BLANK on this Metal host, it has no GridMap batch primitive, and no game-time freeze/step (conductor-eye) capability at all.** Pro column PARKED-OPEN (matt_to_do T5 — buy nothing). Conductor verdict recommendation to follow (gandalf), with galadriel P2 judge-note as input.

---

## The matrix (3 products × 6 probes)

| Probe | **Incumbent** (satelliteoflove/godot-mcp, addon 4.1.0, $0) | **IvanMurzak/Godot-MCP** (addon 4.1.0 / server 9.2.1 / 39 tools, Apache-2.0, $0) | **Pro** (youichi-uda, 162 tools, $15) |
|---|---|---|---|
| **P1** isolated-node capture | **P1-FAIL / P1-alt-PASS** — no isolated-capture command (`UNKNOWN_COMMAND`); the CaptureRig standard-build runtime path produces real d2-skeleton renders (4 angles + 2×2 composite, aabb 1.93×1.70×0.28, tri 3574). | **PRESENT-BUT-BLANK-ON-HOST** — native `screenshot-isolated` tool EXISTS + executes (valid 512² PNG, auto-framed, correct bg), but rendered **background-only** (exactly 1892 B) for every subject/angle tried: runtime-rig d2-skeleton (no editor-time geometry), CSGBox3D (CSG not rebuilt in isolated world), authored flat `MeshInstance3D` from Front **and** Top. `screenshot-viewport` returns a real 77 626 B render → the editor renders; the isolated World3D SubViewport specifically yields no geometry on this Metal host. | **PARKED-OPEN** |
| **P2** screenshot comparison (galadriel channel) | **PARTIAL** — captures yes; NO native diff. Two CaptureRig frames diffed externally → similarity artifacts (a0-vs-a0 = 100%, a0-vs-a180 = 92.98%). Parked for galadriel. | **PARTIAL** — `screenshot-viewport` real render (77 626 B); `screenshot-camera`/`-isolated` present (isolated blank, see P1). NO native diff/compare tool. External-diffable → parked for galadriel. | **PARKED-OPEN** |
| **P3** GridMap (structure-first law) | **PASS** — native `set_gridmap_cells_batch`: 54 cells set + read-back 54 match, one call, editor-time. | **FAIL (vs criterion)** — no native GridMap tool; `node-create` makes a GridMap node, but there is no batch cell-set primitive and reflection `SetCellItem` needs exact 3-arg signature + instance-target serialization that did not resolve in-session (≥50 cells would be 50 reflection calls). | **PARKED-OPEN** |
| **P4** freeze/step + runtime-state (KT-5 conductor-eye) | **PASS** — `game_time_freeze/step/step_until/thaw/status` + `get_runtime_state` + `watch_start/collect/stop`; froze, stepped, read node transforms matching scene truth (game-bridge, running game). | **FAIL** — `editor-application-get-state` reads editor state (`isPlaying:false`, `4.6.3-stable`), but there is **no game-time freeze/step/tick tool at all**; the "runtime" family is only `runtime-errors-*`, `console-*`, `reflection-*`. Editor-time authoring tool, not a tick-controllable runtime debugger. | **PARKED-OPEN** |
| **P5** editor-script escape hatch | **PASS** — `exec_run` runs arbitrary GDScript in a running game with injected context (tree/root/autoloads); created node, set property, verified via independent tree read. | **STRONG PASS** — `reflection-method-call` executes arbitrary C# (incl. private): `Mathf.Sqrt(16)→4` (static, verified); `node-create` (Node3D) + `node-modify` set `Position.X` 0→7 (before/after in response) + `reflection-method-find` (schema). Instance-method targeting has a SerializedMember snag, but static-call + property-set are proven. | **PARKED-OPEN** |
| **P6** wire stability | **PASS** — proven command surface ×3 cycles, no restart/hang; sub-second/seconds latency; editor screenshot 1024×649. | **PASS** — 39 tools registered over the live MCP round-trip; `ping` ×3 cycles all echoed; no server restart/hang; sub-second latency class. | **PARKED-OPEN** |

**Cells filled:** 12 of 18 reachable (6 incumbent + 6 IvanMurzak). Pro 6 cells PARKED-OPEN (undelivered at run time — honorable pause per charter §4).

---

## Toolchain-feasibility finding (the charter's headline BLOCKED-ENV risk — did NOT trip)

The charter expected IvanMurzak might be **BLOCKED-ENV** (Mono/.NET requirement). It was **not**. On this host, from-zero, all of the following stood up:

1. **.NET 8 SDK** — installed locally, non-sudo, reversible (`~/.dotnet`, 8.0.423).
2. **Godot 4.6.3 .NET (mono) editor** — downloaded side-by-side (`/tmp/godot_mono`, `4.6.3.stable.mono.official`, GodotSharp Api+Tools present); never replaced the project-default `/Applications/Godot.app`.
3. **Throwaway branch** carried the project `.csproj` (`Godot.NET.Sdk` + `com.IvanMurzak.ReflectorNet` 5.3.2 + `com.IvanMurzak.McpPlugin` 7.3.0) + the addon copy — `dotnet restore` (8.2 s) + `dotnet build` **green, 0 errors**.
4. **gamedev-mcp-server 9.2.1** (osx-arm64, self-contained Mach-O) launched streamableHttp:8080, auth=none, offline.
5. **Live round-trip** — mono editor loaded the C# plugin (version handshake OK: Plugin 4.1.0 / API 2.0.0 / Godot 4.6.3), registered **39 tools**; a minimal MCP streamableHttp client (`/tmp/mcp_http.mjs`) drove `initialize → tools/list → tools/call` end-to-end.

**Architectural note:** IvanMurzak is a **3-hop** stack (MCP client → `gamedev-mcp-server` → C# editor plugin), cloud-optional (`ai-game.dev`) or self-hosted; the incumbent is a **direct** `ws://127.0.0.1:6550` command server (1 hop). The 3-hop stack is heavier to stand up (SDK + mono editor + server binary + client) but ran cleanly once up.

---

## Evidence index (command transcript + artifact per cell)

**Incumbent** — `incumbent/`: P1 `P1_isolated_capture_transcript.json` + `caprig_skeleton_*.png` + `caprig_skeleton_composite2x2.png` + `caprig_skeleton_meta.json`; P2 `p2_similarity_report.json` + `p2_diff_*.png`; P3 `P3_gridmap_transcript.json` + `P3_open_scene.json`; P4 `P4_freeze_step_runtime_transcript.json` + `P4_P5_game_screenshot.png` + `P45_run_project.json`; P5 `P5_exec_transcript.json` + `P5_exec_verify_transcript.json`; P6 `P6_wire_stability_transcript.json` + `P6_editor_screenshot.png`.

**IvanMurzak** — `ivanmurzak/`: tool surface `toolsurface_tools-list.json` (39 tools); P1 `P1_isolated_capture_raw.json` + `P1_isolated_d2skeleton.png` (blank) + `P1b_isolated_{box,groundref,groundref_top}.png` (all blank) + `P1_node_create.json` + `P1_scene_tree.json`; P2 `P2_viewport_raw.json` + `P2_editor_viewport.png` (real render); P3 `P3_gridmap_create.json` + `P3_gridmap_setcell.json` + `P3_scene_open_kt3.json`; P4 `P4_editor_state.json`; P5 `P5_create.json` + `P5_modify.json` + `P5_reflection_find.json` + `P5_reflection_static_call.json` + `P5_readback_reflection.json`; P6 (ping cycles inline in transcript).

**P2 → galadriel:** both columns produce captures but neither has a native diff/compare tool. The incumbent similarity artifacts (`incumbent/p2_*`) + IvanMurzak viewport render (`ivanmurzak/P2_editor_viewport.png`) are parked for galadriel's verdict-stage judge-note.

---

## Findings (not fixes) routed to conductor

1. **IvanMurzak P1 blank-on-host** is the decisive capability fact for the KFL-20 motivator: the ONE product with a *native* isolated-node capture tool cannot produce a usable isolated render on our Mac/Metal host (viewport capture works, isolated World3D SubViewport does not). If P1 native-isolation is the deciding capability, this needs a fresh-eyes retry (possible fixes: render-frame settle, forcing the isolated SubViewport update mode) before IvanMurzak can be credited P1-PASS.
2. **Structure-first (P3) + conductor-eye (P4)** are incumbent-only among the two live columns — IvanMurzak has neither a GridMap batch primitive nor any game-time tick control. These are exactly the project's proven laws (structure-first GridMap; KT-5 freeze/step).
3. **IvanMurzak's strength is P5** (C# reflection escape hatch, incl. private methods) — a capability the incumbent covers with GDScript `exec_run`. Not a differentiator that serves an unmet need.
4. **Cleanup:** throwaway branch `mcp-bakeoff-ivanmurzak-throwaway` DELETED; `reincarnated-godot` main is untouched (project.godot clean, incumbent addon intact). The .NET SDK (`~/.dotnet`), mono editor (`/tmp/godot_mono`), server (`/tmp/gamedev-server`) remain on-disk for any re-probe; none are in a repo.

**Signed:** drax, 2026-07-23. Matrix complete for reachable columns; conductor (gandalf) authors the verdict recommendation + Matt ratifies the pick (commitment boundary, charter §4/§5).
