# db-lyon/ue-mcp — Install Record

**Date:** 2026-06-08
**Author:** mantis (Pattern A sub-agent for David-H)
**Phase:** 1 of 4 (install only; validation in Phase 2)
**Target project:** C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject (UE 5.7)
**Source dispatch:** agentic_orchestration/dispatches/2026-06-08-david-h-ue-mcp-bridge-spike-AMENDMENT-db-lyon-primary.md

---

## 0. TL;DR

Install SUCCESS. `npx ue-mcp deploy` executed non-interactively against the UE 5.7 project, deployed the C++ bridge plugin source tree to `C:\dev\reincarnated-unreal\Reincarnated\Plugins\UE_MCP_Bridge\`, and added `PythonScriptPlugin` + `UE_MCP_Bridge` to `Reincarnated.uproject`. C++ compilation is required before the bridge is functional — this is Phase 2 scope (`npx ue-mcp build` or first UE Editor launch triggers recompile). No blockers for Phase 2.

---

## 1. Pre-flight verification

| Item | Status | Detail |
|---|---|---|
| Node.js | PASS | v24.15.0 at `C:\Program Files\nodejs\node.exe` |
| npm | PASS | 11.12.1 |
| npx | PASS | 11.12.1 |
| UE 5.7 | PASS | Installed at `C:\Program Files\Epic Games\UE_5.7\` (per prior mantis sessions) |
| UE project | PASS | `C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject` exists; confirmed UE 5.7 `EngineAssociation` |
| Plugins dir | PRE-INSTALL ABSENT | `C:\dev\reincarnated-unreal\Reincarnated\Plugins\` did not exist before install — expected, deploy creates it |
| Visual Studio | ASSUMED PRESENT | Per mantis spike sessions 1-3; not re-verified in Phase 1 (Phase 2 build will surface any gap) |
| RAM | NOTE | PC host (myoriganalcomp); R48.4 single-seam discipline applies; UE Editor + VS compete for memory — Phase 2 must not open Editor while other heavy tasks run |

**uproject state before install (snapshot):**
- Plugins array: `ModelingToolsEditorMode` (enabled, Editor-only) only.
- `PythonScriptPlugin` and `UE_MCP_Bridge` absent.

---

## 2. Install procedure source

**Sources read:**

1. `https://github.com/db-lyon/ue-mcp` (README) — primary install command is `npx ue-mcp init` (interactive). Manual config pattern `npx ue-mcp <uproject-path>` (server startup, not install) also documented.

2. `https://db-lyon.github.io/ue-mcp/getting-started` — confirmed plugin deploys to `<YourProject>/Plugins/UE_MCP_Bridge/`. WebSocket bridge binds to `ws://localhost:9877`. Non-interactive path is `npx ue-mcp deploy` (copies C++ bridge plugin sources) optionally followed by `npx ue-mcp build` (compiles).

3. `https://db-lyon.github.io/ue-mcp/configuration` — `ue-mcp.yml` format documented. Key config: `ue-mcp.disable[]` for tool categories; `http.port` defaults to `7723`; `http.host` defaults to `127.0.0.1`. The `ue-mcp.yml` is only written during `init`, not `deploy`.

4. `https://raw.githubusercontent.com/db-lyon/ue-mcp/main/src/deploy-cli.ts` — confirmed `deploy` is non-interactive: locates uproject (via arg or cwd), calls `deploy()`, enables plugins, reports status. No prompts.

5. `https://raw.githubusercontent.com/db-lyon/ue-mcp/main/src/deployer.ts` — confirmed `deploy()` does three things: (1) enables `PythonScriptPlugin` in `.uproject`, (2) copies `plugin/ue_mcp_bridge/` source to `Plugins/UE_MCP_Bridge/` skipping `Binaries/`, `Intermediate/`, `Saved/`, (3) enables `UE_MCP_Bridge` in `.uproject`. Writes only changed files (byte-level diff). Uses Windows registry + Epic Games Launcher for engine discovery.

6. `https://raw.githubusercontent.com/db-lyon/ue-mcp/main/src/build-cli.ts` — confirmed `npx ue-mcp build` is non-interactive; accepts optional uproject path or cwd. Calls `buildProject()` internally. Phase 2 may use this to trigger C++ compilation headlessly.

**Key insight for non-interactive install decision:** `npx ue-mcp deploy` is the documented non-interactive path to plugin deployment, bypassing the interactive `init` wizard entirely. The `init` wizard is only needed for MCP client config detection (Claude Desktop, Cursor, etc.) which is not required for the Claude Code MCP integration pattern used here.

---

## 3. Install steps executed

**Working directory:** `C:\dev\reincarnated-unreal\Reincarnated\`

**Command 1 — execute deploy:**
```
npx ue-mcp deploy "C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject"
```

**Exit code:** 0 (success)

**stdout (ANSI codes stripped):**
```
npm warn exec The following package was not found and will be installed: ue-mcp@1.0.79

  UE-MCP Deploy

  v Project: Reincarnated (UE 5.7)
  v Plugin sources updated - rebuild required
  v Enabled PythonScriptPlugin
  v Enabled UE_MCP_Bridge

  C++ sources changed - the plugin must be rebuilt before the editor will see new handlers.
  From the project root:
    ue-mcp build
  Then start (or restart) the editor.
```

**Package installed:** `ue-mcp@1.0.79` (downloaded from npm registry on first run; cached in npx cache).

**Note on npm notice:** npm 11.16.0 is available (currently 11.12.1). Minor version difference; not blocking. Do not upgrade during spike — version already confirmed sufficient.

---

## 4. Configuration choices made

Deploy was executed without interactive prompts. No explicit configuration choices were made by the operator during Phase 1. The following defaults are in effect:

| Configuration | Value | Source |
|---|---|---|
| Tool categories enabled | ALL (no disable list) | `ue-mcp.yml` not created by `deploy`; all categories active by default |
| WebSocket port | 9877 | Hardcoded default in bridge; `ws://localhost:9877` |
| HTTP REST server | Disabled | `ue-mcp.yml` `http.enabled: false` is default |
| HTTP port (if enabled) | 7723 | Default; not active |
| HTTP host (if enabled) | 127.0.0.1 | Default |
| Content roots | `/Game/` | Default |
| MCP client config | NOT CONFIGURED | `deploy` does not write `.mcp.json`; Phase 2 must configure Claude Code `.mcp.json` manually |
| `ue-mcp.yml` | NOT PRESENT | Written by `init` only; deploy skips this |

**MCP client config required for Phase 2:** A `.mcp.json` (or `claude_desktop_config.json` entry) must be written pointing at the uproject before Claude Code can connect. Template per docs:
```json
{
  "mcpServers": {
    "ue-mcp": {
      "command": "npx",
      "args": ["ue-mcp", "C:/dev/reincarnated-unreal/Reincarnated/Reincarnated.uproject"]
    }
  }
}
```
Note: forward slashes required in uproject path even on Windows per db-lyon docs.

---

## 5. Plugin placement verification

**Plugin directory created:** `C:\dev\reincarnated-unreal\Reincarnated\Plugins\UE_MCP_Bridge\`

**Top-level contents:**
- `UE_MCP_Bridge.uplugin` (1,390 bytes) — version 0.3.0; FriendlyName "UE MCP Bridge"; 185+ editor tools via MCP protocol; `LoadingPhase: PostEngineInit`; `Type: Editor`
- `Source\UE_MCP_Bridge\` — full C++ source tree

**uplugin plugin dependencies declared (all must be present in UE 5.7):**
PythonScriptPlugin, DataValidation, EditorScriptingUtilities, EnhancedInput, GameplayAbilities, Niagara, PCG, IKRig, ControlRig, PoseSearch, PropertyBindingUtils, StructUtils, StateTree

All of the above ship with UE 5.7 Editor install. No third-party plugin dependencies.

**C++ source files present (handler surface confirmed):**
- `BridgeServer.cpp` / `.h` — WebSocket server core
- `GameThreadExecutor.cpp` / `.h` — game-thread dispatch
- `HandlerRegistry.cpp` / `.h` — handler registration
- `Handlers/` directory containing 40+ `.cpp` + `.h` files:
  - AnimationHandlers (+ Sequence, SkeletalLive, StateMachine)
  - AssetHandlers (+ Import, Mesh, Sockets)
  - BlueprintHandlers (+ Functions, Graph, Properties)
  - EditorHandlers (+ Build, PIE)
  - GameplayHandlers (+ Input)
  - GasHandlers (+ Runtime)
  - LevelHandlers (+ Lights, Trace, Volumes)
  - MaterialHandlers (+ Advanced, Function, Graph)
  - NiagaraHandlers
  - PCGHandlers
  - WidgetHandlers (+ Properties)
  - AnimationHandlers_StateMachine, StateTreeHandlers
  - Plus: Audio, Demo, Dialog, Foliage, Landscape, Networking, Physics, Project, Reflection, Sequencer, Spline handlers

**C++ compile state:** SOURCE ONLY — no `Binaries/` directory present. Rebuild required before the bridge is functional. This is expected per deploy output message.

**uproject state after install:**
```json
{
  "FileVersion": 3,
  "EngineAssociation": "5.7",
  "Plugins": [
    { "Name": "PythonScriptPlugin", "Enabled": true },
    { "Name": "ModelingToolsEditorMode", "Enabled": true, "TargetAllowList": ["Editor"] },
    { "Name": "UE_MCP_Bridge", "Enabled": true }
  ]
}
```

---

## 6. SSH/remote topology defaults observed

| Parameter | Value | Notes |
|---|---|---|
| WebSocket bind address | `ws://localhost:9877` | Localhost-only; bridge starts when UE Editor loads the plugin (`PostEngineInit`) |
| WebSocket port | 9877 | Hardcoded default; not configurable in `ue-mcp.yml` (only HTTP port is configurable) |
| HTTP REST server | Disabled by default | Enabled via `ue-mcp.yml http.enabled: true`; binds `127.0.0.1:7723` |
| MCP server (TypeScript) | stdio transport | No network port; communicates with AI client via stdin/stdout |

**Phase 2 SSH port-forwarding requirement:** The WebSocket bridge at `ws://localhost:9877` is localhost-only. When mantis is SSH-invoked from Mac and the UE Editor runs on PC, the MCP server (TypeScript/Node.js via npx) also runs on PC — both are PC-resident. No SSH port forwarding is needed for the MCP server-to-bridge connection since both processes live on the PC. The Claude Code MCP client integration (the `npx ue-mcp` process spawned by Claude Code's `stdio` transport) also runs PC-side. This is the correct topology for the SSH-invoked mantis pattern: Claude Code session on PC, MCP server on PC, WebSocket bridge on PC.

**If Mac-resident Claude Code session were used instead:** port forwarding would be needed (`ssh -L 9877:localhost:9877 user@192.168.1.133`). Not applicable to mantis's PC-resident invocation pattern.

---

## 7. Blockers encountered

None. Install completed cleanly.

**Anticipated Phase 2 prerequisites (not blockers, but must be satisfied before bridge is live):**

1. **C++ compilation:** `npx ue-mcp build` (or UE Editor first launch) must compile the plugin. Visual Studio must be present and configured for UE 5.7 builds. This was confirmed in prior mantis spike sessions (sessions 1-3 exercised VS compile paths) but should be verified at Phase 2 start.

2. **MCP client config:** `.mcp.json` must be written at project root (or equivalent Claude Code config) before Claude Code can enumerate the ue-mcp tools. Template in § 4 above.

3. **Editor launch:** The WebSocket bridge activates at `PostEngineInit` — the UE Editor must be running with the Reincarnated project loaded for Phase 2 connectivity tests. Phase 2 dispatch must scope this explicitly.

4. **`ue-mcp.yml` tool scope decision:** No `ue-mcp.yml` was written. All 21 tool categories are active by default. Phase 2 may want to write a minimal `ue-mcp.yml` to disable unused categories (e.g., `gas`, `networking`, `foliage`, `landscape`) to reduce handler surface during spike validation. This is optional — spike can proceed with defaults.

---

## 8. Reproducibility notes

To reproduce this install on a clean project:

```powershell
# Preconditions: Node.js 18+, npm, UE 5.7 installed, valid .uproject in target dir
# Working directory: anywhere (uproject path passed as arg)

npx ue-mcp deploy "C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject"

# Expected output: 4 green checkmarks (project detected, plugin sources updated,
# PythonScriptPlugin enabled, UE_MCP_Bridge enabled)
# Expected artifact: Plugins\UE_MCP_Bridge\ created in project root
# Expected uproject change: PythonScriptPlugin + UE_MCP_Bridge added to Plugins array

# After deploy — compile the C++ plugin:
npx ue-mcp build "C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject"
# OR launch UE Editor (will prompt to rebuild outdated modules on first open)

# After compile — write MCP client config at project root:
# Create .mcp.json per template in § 4

# After config — launch UE Editor, verify Output Log for:
# "LogMCPBridge: [UE-MCP] Bridge listening on ws://localhost:9877"
```

**Package version pinned:** `ue-mcp@1.0.79` (installed by npx on 2026-06-08). Future runs will pick up latest unless version-pinned in `.mcp.json` args or `package.json`.

**No `ue-mcp.yml` defaults file written** — deploy omits this. If tool-category scoping is needed, create manually at `C:\dev\reincarnated-unreal\Reincarnated\ue-mcp.yml` using template from § 4.

---

## 9. Sign-off

mantis (Pattern A sub-agent for David-H)
Phase 1 complete. Install SUCCESS. No blockers for Phase 2.
Phase 2 scope: (1) compile C++ plugin via `npx ue-mcp build`, (2) write `.mcp.json`, (3) launch UE Editor, (4) verify WebSocket bridge listening message in Output Log, (5) execute tool connectivity tests (`project(action="get_status")`), (6) validate SSH-topology per AMENDMENT § 1.1 #3.
Routed back to David-H for Phase 2 dispatch authoring.
