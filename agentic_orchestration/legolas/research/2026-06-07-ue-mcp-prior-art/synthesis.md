# Research — UE + MCP Prior Art Survey — 2026-06-07

**Mode:** A (analytical)
**Commissioner:** gandalf (story-and-design steward)
**Commission file:** `agentic_orchestration/dispatches/2026-06-07-legolas-ue-mcp-prior-art-research.md`
**Sources consulted:** GitHub (7 repositories), Epic Developer Community docs + forums, DEV Community, community snippet registry, BlenderMCP project page, Unity MCP project page
**Crawl date:** 2026-06-07

---

## TL;DR

The prior art landscape is substantially richer than anticipated. At minimum five distinct UE + MCP implementations exist on GitHub, ranging from experimental to moderately mature. Two are directly relevant to our spike: **chongdashu/unreal-mcp** (MIT, 2,000+ stars, C++ TCP plugin + Python MCP server, UE 5.5+) and **remiphilippe/mcp-unreal** (Apache-2.0, UE 5.7 native, Go binary wrapping Remote Control HTTP + MCPUnreal plugin, 48 tools). A third, **NAJEMWEHBE/unreal-ai-connection** (MIT, 147 tools, 581 tests, C++ TCP plugin + Python bridge), shows the most engineering rigor but 5 stars — possibly a newer arrival. Blender MCP (ahujasid, 22.4k stars, MIT) establishes the canonical DCC-tool MCP pattern: TCP socket into a thin in-engine addon, MCP server in Python/TypeScript wrapping the socket. UE Remote Control HTTP API (port 30010, no auth by default, local-only by default) is a viable but limited integration surface — it requires Preset configuration for property access and has known packaged-game gotchas. UE Python scripting is a real alternative for asset operations but is not interactive-session-compatible via SSH without a running editor, and has no live-actor manipulation in headless commandlet mode.

**Recommended verdict: REFERENCE+BUILD** — two existing implementations are informative and partially adoptable as reference, but neither matches our exact use case (mantis as headless SSH agent driving a live UE Editor on a remote PC). Build from scratch informed by chongdashu's C++ TCP plugin architecture and remiphilippe's Remote Control HTTP wrapping pattern.

---

## Q1 — Existing UE + MCP Implementations

### Findings

Multiple implementations exist. The five most relevant:

**1. chongdashu/unreal-mcp**
- URL: https://github.com/chongdashu/unreal-mcp
- Description: "Enable AI assistant clients like Cursor, Windsurf and Claude Desktop to control Unreal Engine through natural language using MCP."
- Architecture: C++ UE plugin runs a TCP server on port 55557 inside the running editor. A Python MCP server (using FastMCP) connects to the TCP socket and exposes MCP tools to AI clients. No Remote Control HTTP API involved — direct TCP to native C++ plugin.
- Tool scope: 15+ operations — actor create/delete/transform/query, Blueprint class creation, Blueprint node graph (event/function nodes, variables, connections), editor viewport control.
- License: MIT
- Stars: 2,000+ stars, 321 forks
- UE version: 5.5+
- Status: Explicitly "Experimental — production use not recommended." Breaking changes expected.
- Installation: Visual Studio required to build C++ plugin; Python 3.12+; MCP client (Claude Desktop, Cursor, or Windsurf).

**2. remiphilippe/mcp-unreal**
- URL: https://github.com/remiphilippe/mcp-unreal
- Description: "Full control over UE 5.7 projects — headless builds & tests, Blueprint editing, actor manipulation, procedural mesh generation, and UE API documentation lookup."
- Architecture: Single Go binary (zero external dependencies). Three communication layers: (a) `UnrealEditor-Cmd` invocation for headless builds/tests/cooking; (b) UE Remote Control HTTP API on port 30010 for actor/property ops; (c) MCPUnreal editor plugin HTTP server on port 8090 for Blueprint editing, asset queries, mesh operations.
- Tool scope: 48 tools — build/compile, cooking, project config, test automation, actor spawning, property manipulation, Blueprint editing, animation blueprints, materials, characters, input, PCG, GAS, Niagara VFX, procedural mesh, RealtimeMesh, level management, console commands, Play In Editor control.
- License: Apache-2.0
- Stars: 46 stars, 6 forks
- UE version: 5.7 minimum
- Requirements: Go 1.25+, Remote Control Plugin enabled, MCPUnreal editor plugin for advanced features.
- Limitations: Editor does not auto-save; some headless tools may exceed 60-second timeout; C++ tests are local opt-in.

**3. NAJEMWEHBE/unreal-ai-connection**
- URL: https://github.com/NAJEMWEHBE/unreal-ai-connection
- Description: "105 editor-automation tools over a local TCP socket, ~50ms round-trip, 489 passing tests, one-command install. Vendor-neutral, MIT."
- Architecture: Three layers — MCP client (Claude Code, Cursor, Cline) → Python bridge (stdio MCP ↔ TCP translation) → C++ plugin module binding to 127.0.0.1:18888. 110 native C++ handlers + 37 synthetic Python-composition tools = 147 tools total.
- Tool scope: 15 categories — Python execution, asset registry, Blueprint/widget authoring, materials, textures, Level Sequences, actor spawning, Niagara FX, cinematics rendering, viewport control, console interaction, event subscriptions, audio introspection.
- License: MIT
- Stars: 5 stars, 2 forks
- UE version: Primary target UE 5.7.4 Windows 11; prebuilt binaries for UE 5.6 Win64.
- Testing: 581 pytest cases, GitHub Actions CI. Smoke test validates all default-on handlers against live editor.
- Note: Low star count suggests this is newly published or niche; engineering quality appears high.

**4. ChiR24/Unreal_mcp**
- URL: https://github.com/ChiR24/Unreal_mcp
- Description: "Comprehensive MCP server enabling AI assistants to control Unreal Engine through native C++ Automation Bridge plugin, built with TypeScript and C++."
- Architecture: TypeScript MCP server + native C++ Automation Bridge plugin. Exposes 23 MCP tools in broad all-tools mode.
- License: Not retrieved in detail; activity level unknown.

**5. Flux-Point-Studios/unreal-mcp**
- URL: https://github.com/Flux-Point-Studios/unreal-mcp
- Description: "Unreal Engine MCP server for AI-powered automation."
- Details: Limited metadata retrieved; appears to be a fork/variant rather than original work.

**6. ayeletstudioindia/unreal-analyzer-mcp**
- URL: https://github.com/ayeletstudioindia/unreal-analyzer-mcp
- Description: MCP server providing source code analysis capabilities for UE codebases — enabling AI assistants to analyze UE source. Narrower scope (read-only analysis) than the editor-control implementations.

**Community listing:** mcp-unreal appears in Awesome MCP Servers catalogue (https://mcpservers.org/servers/remiphilippe/mcp-unreal), confirming community visibility.

**DEV community article** ("How I taught Claude to see inside Unreal Engine", https://dev.to/colton_willey_ef3d8727ae9/how-i-taught-claude-to-see-inside-unreal-engine-23a9): One developer built custom tooling by extending the UnrealClaude plugin to parse binary `.uasset` files and build a script interface layer. Finding: "No existing solution existed at the time" for LLM understanding of Unreal assets. Project evolved into the Unreal Engine LLM Toolkit (open source). Lesson: token-efficient tool design matters — "reading entire blueprints for single-node inspection proved wasteful."

### Assessment

FORK+ADOPT is not recommended because:
- chongdashu is self-described experimental, breaking-change-likely, and does not cover our use case (headless SSH agent → remote live editor).
- remiphilippe (46 stars, 4 commits on main) is too immature to fork with confidence, though its architecture is the closest match.
- NAJEMWEHBE has the highest engineering rigor (581 tests, CI) but 5 stars and Windows 11 primary target — unknown SSH/remote viability.

REFERENCE+BUILD is the correct posture: these implementations validate that the C++ TCP plugin + Python MCP server pattern works for UE editor control, and that Remote Control HTTP API is usable for actor/property ops. remiphilippe's hybrid approach (Remote Control HTTP for actor ops + custom plugin for Blueprint ops) is the most instructive reference for mantis's spike.

---

## Q2 — UE Remote Control Web API: Endpoints + Community Gotchas

### HTTP Endpoints (UE 5.7)

Official documentation: https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-control-api-http-reference-for-unreal-engine

Default port: **30010**. Server listens on 127.0.0.1 by default (local-only). To allow remote access: change `DefaultBindAddress` in `DefaultEngine.ini`.

Available endpoints:

| Endpoint | Method | Description | Preset Required? |
|---|---|---|---|
| `/remote/info` | GET | Returns all available HTTP routes + descriptions | No |
| `/remote/object/call` | PUT | Invoke functions on UObjects (BlueprintCallable + Blueprint-defined) | No |
| `/remote/object/property` | PUT | Read/write UObject properties (READ_ACCESS, WRITE_ACCESS, WRITE_TRANSACTION_ACCESS) | No |
| `/remote/object/thumbnail` | PUT | Retrieve asset thumbnail images from Content Browser | No |
| `/remote/search/assets` | PUT | Search Asset Registry with filters (PackageNames, ClassNames, PackagePaths) | No |
| `/remote/object/describe` | PUT | Returns metadata about UObject properties, functions | No |
| `/remote/batch` | PUT | Group multiple HTTP requests into a single ordered call | No |
| `/remote/object/event` | PUT | (Experimental) Listen for ObjectPropertyChanged events | No, but requires `WebControl.EnableExperimentalRoutes=1` in DefaultEngine.ini |
| Preset endpoints | Various | Access exposed preset properties/functions by name | Yes — Preset must be created and configured |

**Property access restrictions:** Properties must be `public`, lack custom BlueprintGetter/BlueprintSetter, be marked `EditAnywhere` (Editor) or `BlueprintVisible` (PIE/game mode).

**Preset vs presetless:** Most core endpoints (`/remote/object/call`, `/remote/object/property`) work without a Preset if you know the UObject path. Presets enable named-property access via the Preset HTTP reference API (separate endpoint set).

### Community Gotchas

Source: https://forums.unrealengine.com/t/things-to-know-about-the-remote-control-api/652426

1. **PIE object path prefix**: Runtime requests require `_UEDPIE_X_` prefix in object paths. Omitting this executes against editor objects, not the running PIE instance — silent failure where operations appear to succeed but affect the wrong object.

2. **WebSocket notification limitation**: WebSockets synchronize values between multiple client instances, but the engine does not push notifications to clients for engine-side changes. Clients must poll or listen for explicit events.

3. **WebSocket instability history**: Older UE versions (4.26) reported editor crashes on WebSocket connection. UE 5.5 packaged builds have reported Motion Design WebSocket API issues. HTTP is the more reliable integration surface for our use case.

4. **Packaged build requirements**: Packaged executables need launch flags `-RCWebControlEnable -RCWebInterfaceEnable`. Presets must be dragged into the scene as actors to function in packaged builds. Only one preset active simultaneously.

5. **Property modification in packaged builds**: Cannot modify preset properties via API in packaged games despite properties being present. `ActivePreset` field appears unset with no documented configuration path.

6. **Character animation gotcha**: Character-specific properties like `AnimToPlay` show parameter changes in PIE but fail to affect behavior in packaged games.

**For our spike:** These gotchas primarily affect packaged game and PIE runtime scenarios. For editor automation (mantis driving the UE Editor, not a packaged game), the main gotchas are: (a) correct UObject path resolution, (b) property access flag requirements, (c) HTTP is more stable than WebSocket for request-response control operations.

**Authentication:** No application-level authentication by default. Epic documentation explicitly warns: "Do not attempt to open the hostname and port to the open Internet." Default bind to 127.0.0.1 (local-only). For our use case (mantis via SSH tunnel → localhost on the PC), no auth needed. Any future productionization should add network-level controls (VPN, firewall rule) rather than relying on application-level auth that doesn't exist.

**WebSocket vs HTTP verdict:** HTTP for request-response control operations (actor placement, property setting, function calls). WebSocket only if mantis needs streaming event subscriptions (e.g., watching for property change events). HTTP is more reliable and simpler for spike scope.

---

## Q3 — DCC-Tool MCP Server Patterns

### Blender MCP (canonical pattern)

- Primary repo: https://github.com/ahujasid/blender-mcp (22.4k stars, 2.2k forks, MIT, actively maintained as of v1.5.5)
- Architecture: Blender addon (`addon.py`) creates a TCP socket server inside Blender. External Python MCP server connects to addon over TCP, exchanging JSON `{type, params}` objects. MCP server exposes tools to AI clients via stdio.
- This is the **dominant pattern for DCC tool MCP integration**: thin in-engine addon (TCP server) + external MCP server wrapping socket protocol. Avoids tight coupling to engine internals.
- Comparison repo: https://github.com/djeada/blender-mcp-server — 22 tools across 6 namespaces; same architecture.

### Godot MCP

- Repo: https://github.com/bradypp/godot-mcp (MIT)
- Also: https://github.com/hi-godot/godot-ai ("Production-grade MCP server and AI tools for Godot." Snap install.)
- Tool coverage: 120+ operations across ~39 MCP tools — scenes, nodes, GDScript editing, signals, UI, materials, animations, particles, cameras, environments.
- Community activity: Multiple competing implementations exist; Godot's open-source culture and GDScript accessibility have driven MCP adoption faster than UE.

### Unity MCP

- Repo: https://github.com/CoplayDev/unity-mcp (MIT, 10.4k stars, 1.2k forks, v9.7.1 as of May 24 2026, sponsored by Aura)
- Architecture: C# Unity Editor plugin + Python MCP server. Active Discord. 61 releases.
- Pattern: Same two-process model (in-engine plugin + external MCP server) but using C# for the in-engine side instead of C++ (Unity's native scripting environment is C#).
- Relevant comparison for UE: Unity MCP's maturity (10k stars, sponsored, 61 releases) vs UE's most mature (chongdashu 2k stars, experimental) reflects Unity's more accessible scripting environment.

### Maya / Houdini / 3ds Max

No prominent MCP implementations surfaced in search results. DCC tool MCP coverage appears concentrated in Blender, Godot, Unity, and UE — the tools with most accessible scripting APIs and open communities. Autodesk tools likely have proprietary or enterprise-internal integrations not in public registry.

### Architectural pattern summary

The canonical pattern across all DCC tools is: **in-engine TCP socket server (addon/plugin) ↔ external Python/TypeScript MCP server (stdio to MCP client)**. Remote Control HTTP API is a UE-specific variant where Epic already provides the in-engine HTTP server, reducing the need to write the in-engine side from scratch. chongdashu chose to write their own C++ TCP server anyway (bypassing Remote Control), gaining lower latency and finer-grained control at the cost of more C++ code. remiphilippe wraps the existing Remote Control HTTP API (plus a custom plugin for Blueprint ops), trading some control for less C++ required.

---

## Q4 — UE Python Scripting as Architectural Alternative

### What is scriptable via UE Python

Official documentation: https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python

The Python Editor Script Plugin exposes the `unreal` module — an automatic reflection of nearly everything exposed from C++ to Blueprints in the Editor environment. Scriptable operations include:

- Asset management: import, move, organize, generate LODs — via `unreal.EditorAssetLibrary`, `unreal.AssetTools`
- Actor and level manipulation: place, query, modify actors; load levels via `unreal.LevelEditorSubsystem`
- Object properties: `set_editor_property()` / `get_editor_property()` with transaction support
- Automation: LOD generation, procedural level layout, batch asset operations

**Runtime restriction**: Python is available in the Unreal Editor only. Not usable in PIE, standalone game, or packaged executables. Cannot be used as a gameplay scripting language.

### Invocation methods

| Method | Headless? | Notes |
|---|---|---|
| Python Console (interactive) | No | Requires Editor UI |
| `py "script.py"` (console command) | No | Requires Editor running |
| File menu execution | No | Requires Editor UI |
| `-ExecutePythonScript="path"` (command line) | No | Full Editor launches — slow but full API surface |
| `-run=pythonscript -script="..."` (commandlet) | Yes | Fast, no UI, but limited: does NOT auto-load levels, fewer APIs available |
| `init_unreal.py` (startup script) | Partial | Auto-runs on Editor startup; requires Editor to start |

### Python-via-SSH vs MCP-wrapper comparison

**Python-via-SSH architecture:**
- mantis SSH-executes scripts on the PC running UE
- Script uses `-ExecutePythonScript` (editor must be running) or `-run=pythonscript` (headless commandlet)
- For live editor session: mantis would need to either (a) inject commands into a running editor via `py` console command, which requires a mechanism to send keystrokes/commands to the running editor process, or (b) launch a separate Editor process per script, which is slow (UE startup is 30-60+ seconds)
- For headless commandlet: fast for asset operations but cannot manipulate the live editor session or interact with actors placed in the world
- No interactive session: Python executes to completion and exits; no persistent connection for back-and-forth tool calls

**MCP-wrapper architecture (our spike plan):**
- mantis connects to MCP server via stdio
- MCP server wraps Remote Control HTTP API (or TCP to C++ plugin)
- Live connection to running Editor instance
- Persistent, request-response capable — mantis calls tools iteratively
- Actor manipulation, Blueprint editing, viewport control all available through live editor

**Assessment:** Python-via-SSH is NOT a viable replacement for MCP-wrapper for mantis's use case. The core requirement is that mantis drives a **live running Editor session** on the remote PC (per the mantis architecture-validation spike findings). Python headless commandlet mode cannot do this. Python commands injected into a running Editor via `py` console command would require a separate mechanism to deliver those commands (essentially reinventing the same socket/HTTP bridge problem). Python scripting is complementary — useful for specific asset batch operations — but does not replace the MCP bridge for live editor control.

**One hybrid use case worth noting:** remiphilippe/mcp-unreal demonstrates that Python execution can be one of the 48 MCP tools (via the NAJEMWEHBE implementation, "Python execution" is explicitly in the tool surface). An MCP server can offer a `run_python_script` tool, giving mantis both live editor control and the ability to fire batch Python scripts when appropriate. This is the HYBRID pattern.

---

## Q5 — AI-Driven Game Development Tooling State of the Art

### Key developments

**UnrealClaude / Claude Code + UE 5.7:**
- URL: https://github.com/Natfii/UnrealClaude
- Claude Code CLI integration for UE 5.7 — embeds a chat panel within the editor for AI coding assistance with live streaming responses and built-in UE 5.7 documentation context.
- Also listed at: https://mcpmarket.com/server/unrealclaude

**Unreal Engine LLM Toolkit (open source):**
- Evolved from the "How I taught Claude to see inside Unreal Engine" project (see Q1).
- Focuses on making UE asset binary data readable/interpretable by LLMs — complementary to MCP editor control.

**Industry adoption (2026 data):**
- Source: https://kevurugames.com/blog/using-claude-ai-in-game-development-tools-use-cases-and-industry-statistics/
- 95% of game studios worldwide have adopted AI into workflows (2026 Unity Game Development Report).
- 62% employ AI agents like Claude for backend and coding.
- Claude 3.7+ leads for Unreal-specific tasks involving C++ macros (`UFUNCTION`, `UPROPERTY`, `TObjectPtr` vs standard pointers).

**Claude vs ChatGPT for UE:**
- Source: https://kevurugames.com/blog/claude-vs-chatgpt-for-game-development-capabilities-benchmarks-and-data/
- Claude positions as "senior architect for mapping complex multi-file systems." ChatGPT better for rapid prototyping and generating placeholder assets.
- For UE-specific work, Claude's ability to handle Unreal's C++ macros without hallucinating standard C++ patterns is a practical advantage.

**AI Blueprint authoring:**
- Multiple MCP servers (chongdashu, NAJEMWEHBE, remiphilippe) all include Blueprint editing tools, validating this as an established use case.
- Cursor + UE Blueprint authoring is an active community topic but fragmented.

**GDC / conference coverage:**
- No specific GDC 2025/2026 conference talk on AI + UE MCP surfaced. The space is moving primarily through open-source community channels, not yet mainstreamed in industry conferences.

**Relevant pattern:** The most technically sophisticated teams are building custom plugin + MCP server stacks (pattern established by Blender, Unity, and now multiple UE implementations), rather than waiting for Epic to provide first-party tooling. Epic has not published a first-party MCP server; all implementations are community/third-party.

---

## Q6 — Authentication and Security Patterns for Editor Automation

### UE Remote Control defaults

- Default bind address: `127.0.0.1` (local-only). Server does not listen on external interfaces unless explicitly configured in `DefaultEngine.ini`.
- No application-level authentication: no API key, no token, no OAuth. Connection is accepted from any client that can reach the listening address/port.
- Epic's explicit guidance: "Do not attempt to open the hostname and port of your Unreal Engine application to the open Internet, as doing so may make your Project and computer vulnerable to malicious actions from third parties." (Remote Control Quick Start documentation)
- The server only runs when explicitly activated.
- Port 30010 (HTTP), port 30020 (WebSocket) by default. Both configurable in Project Settings → Web Remote Control.

### Security posture for our spike

For the spike (mantis via SSH → localhost on the Matt-side PC), the security model is:
- SSH tunnel provides transport security for the mantis → PC leg
- UE Remote Control API bound to 127.0.0.1 is only reachable over the SSH tunnel
- No application-layer auth needed; network-level isolation is sufficient

This is the correct posture for the spike. No auth implementation required.

### Productionization patterns (informational)

If the spike succeeds and mantis needs more persistent/automated access:
- Standard pattern for local editor automation: firewall rule restricting port 30010 to loopback or VPN subnet
- SSH port-forward is the idiomatic remote-access mechanism (already how mantis operates)
- No community examples found of API-key auth layered on top of UE Remote Control — this is not a standard pattern; the community accepts network-level isolation as sufficient
- The C++ TCP plugin approach (chongdashu, NAJEMWEHBE) has the same no-auth default; same local-only posture applies

---

## Recommendations for MCP Bridge Spike Scope

### Verdict: REFERENCE+BUILD

**Rationale:**
- Multiple existing implementations confirm the technical approach is viable — this is not unexplored territory.
- None of the existing implementations match our specific use case: mantis (SSH agent, headless PC-side) needs to drive a live UE Editor session on a remote Windows PC via MCP tools. chongdashu assumes a local MCP client (Claude Desktop, Cursor). remiphilippe targets the same machine. NAJEMWEHBE targets local Windows 11.
- The SSH-mediated remote architecture requires mantis to be the MCP client connecting through an SSH-forwarded port — none of the existing projects were designed for this topology.
- chongdashu (MIT, 2k+ stars) is the best candidate for reference; its C++ TCP plugin + Python FastMCP server pattern is proven and its Blueprint node graph editing capability is directly relevant. Its "experimental" status and breaking-change warning make FORK+ADOPT risky.
- remiphilippe (Apache-2.0, 46 stars) is architecturally most similar to our planned spike (Remote Control HTTP API + Go/Python wrapper). Too young to adopt, but ideal reference for how to structure the Remote Control HTTP wrapping layer.

### Scope adjustments for spike

1. **Reference chongdashu's C++ TCP plugin rather than wrapping Remote Control HTTP exclusively.** The C++ TCP plugin approach gives lower latency and avoids the Remote Control API's property access restrictions (EditAnywhere requirement). Consider whether the spike should wrap Remote Control HTTP, implement a C++ TCP plugin (reference chongdashu's source), or both. remiphilippe uses both: Remote Control HTTP for actor/property ops, custom plugin (MCPUnreal) for Blueprint ops.

2. **Start with Remote Control HTTP as the zero-C++ MVP.** Remote Control is already in UE 5.7, requires no compilation, and covers actor spawning, property manipulation, and function calls. This reduces spike risk. If Blueprint editing is required in the spike, add the C++ plugin layer — reference chongdashu or NAJEMWEHBE.

3. **Python MCP server with FastMCP is the recommended server pattern.** All three main implementations (chongdashu, NAJEMWEHBE, and the Blender/Godot/Unity ecosystem) converge on Python + FastMCP for the MCP server layer. Go (remiphilippe) is an alternative but has a smaller community and adds a language dependency.

4. **Include a `run_python_script` tool in the MCP server's tool surface.** This enables mantis to fire UE Python batch operations (asset import, LOD generation, etc.) without requiring separate MCP tools for each operation. Reference NAJEMWEHBE's pattern.

5. **SSH port-forwarding is the correct topology for mantis remote access.** Spike should explicitly document: mantis SSH-forwards port 30010 (Remote Control HTTP) and optionally the C++ TCP plugin port (55557 or 18888 depending on implementation chosen) through the SSH connection. No auth layer needed for spike.

6. **Do not implement WebSocket in the spike.** HTTP is more stable (per community gotchas) and sufficient for request-response editor control. WebSocket adds complexity without benefit for spike scope.

---

## Open Questions / Surfaces for Gandalf Consideration

1. **C++ compilation dependency.** If the spike expands beyond Remote Control HTTP to include a C++ TCP plugin (for Blueprint editing), mantis or David-H will need to build and install the C++ plugin into the UE project on Matt's PC. This requires Visual Studio and project file regeneration. Is that within the spike scope, or should the spike be constrained to pure Remote Control HTTP (no C++ required) for the initial pass?

2. **UE 5.7 compatibility gap.** chongdashu requires UE 5.5+ (should work on 5.7). remiphilippe targets UE 5.7 exactly. NAJEMWEHBE targets UE 5.7.4 Windows 11 as primary. The spike's target is UE 5.7, which aligns with all three. No compatibility gap identified, but worth confirming Matt's exact UE version before David-H fires.

3. **MCP server process location.** In the chongdashu pattern, the Python MCP server runs on the machine with the MCP client (Claude Desktop). In mantis's case, the MCP server needs to run either on the PC (Matt-side) or as a bridge process. Spike commission should clarify where the Python MCP server process runs — on the PC (started by mantis via SSH) or on the Mac (connecting to PC over SSH tunnel). Both are architecturally valid but have different operational implications for mantis's autonomy.

4. **Tool scope for spike vs. production.** The Earth-Avatar creation moment spike likely needs: actor placement, material assignment, Niagara VFX spawning, and possibly Blueprint property setting. This is a subset of what all three main implementations cover. Spike should define minimal tool surface (5-10 tools) rather than attempting comprehensive coverage — this is the "smoke-test vs full-regen" discipline applied to MCP server scope.

5. **License compatibility.** chongdashu (MIT) and NAJEMWEHBE (MIT) are straightforwardly adoptable. remiphilippe (Apache-2.0) has attribution requirements but is permissive. No license conflict for reference use. If code is copied (not just referenced), attribution requirements of Apache-2.0 apply.

---

## Source List

- chongdashu/unreal-mcp: https://github.com/chongdashu/unreal-mcp
- remiphilippe/mcp-unreal: https://github.com/remiphilippe/mcp-unreal
- NAJEMWEHBE/unreal-ai-connection: https://github.com/NAJEMWEHBE/unreal-ai-connection
- ChiR24/Unreal_mcp: https://github.com/ChiR24/Unreal_mcp
- Flux-Point-Studios/unreal-mcp: https://github.com/Flux-Point-Studios/unreal-mcp
- ayeletstudioindia/unreal-analyzer-mcp: https://github.com/ayeletstudioindia/unreal-analyzer-mcp
- gingerol/vhcilab-unreal-engine-mcp: https://github.com/gingerol/vhcilab-unreal-engine-mcp
- mcp-unreal on Awesome MCP Servers: https://mcpservers.org/servers/remiphilippe/mcp-unreal
- ahujasid/blender-mcp: https://github.com/ahujasid/blender-mcp
- djeada/blender-mcp-server: https://github.com/djeada/blender-mcp-server
- CoplayDev/unity-mcp: https://github.com/CoplayDev/unity-mcp
- bradypp/godot-mcp: https://github.com/bradypp/godot-mcp
- hi-godot/godot-ai: https://github.com/hi-godot/godot-ai
- UE 5.7 Remote Control HTTP API reference: https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-control-api-http-reference-for-unreal-engine
- UE 5.7 Remote Control WebSocket API reference: https://dev.epicgames.com/documentation/en-us/unreal-engine/remote-control-api-websocket-reference-for-unreal-engine
- UE 5.7 Python scripting documentation: https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python
- UE community snippet — headless Python: https://dev.epicgames.com/community/snippets/J5R1/unreal-engine-run-headless-unreal-editor-with-python-script
- UE community forum — Remote Control gotchas: https://forums.unrealengine.com/t/things-to-know-about-the-remote-control-api/652426
- UE community forum — WebSocket issues UE5.5: https://forums.unrealengine.com/t/ue5-5-motion-design-remote-control-websocket-api-issues-in-package/2308226
- DEV Community — How I taught Claude to see inside UE: https://dev.to/colton_willey_ef3d8727ae9/how-i-taught-claude-to-see-inside-unreal-engine-23a9
- Claude vs ChatGPT for game dev: https://kevurugames.com/blog/claude-vs-chatgpt-for-game-development-capabilities-benchmarks-and-data/
- Claude AI in game development statistics: https://kevurugames.com/blog/using-claude-ai-in-game-development-tools-use-cases-and-industry-statistics/
- Natfii/UnrealClaude: https://github.com/Natfii/UnrealClaude
- UnrealClaude on MCP Market: https://mcpmarket.com/server/unrealclaude
- cgtoolbox/UnrealRemoteControlWrapper (Python wrapper for UE Remote Control HTTP): https://github.com/cgtoolbox/UnrealRemoteControlWrapper

---

## Knowledge Gaps Not Resolved

1. **chongdashu maintainer activity / last commit date**: star count and fork count retrieved but exact commit recency not confirmed. Marked experimental but could be recently or rarely updated.
2. **remiphilippe production readiness**: 46 stars and 4 commits on main suggest early-stage. Full test coverage unknown. Go 1.25+ requirement not yet validated against mantis's PC environment.
3. **NAJEMWEHBE launch date**: Engineering quality appears high (581 tests, CI) but 5 stars may indicate very recently published. Recommend a second pass in 2-4 weeks to assess if community adoption grows.
4. **Remote Control HTTP API latency benchmarks**: No published latency numbers found for HTTP round-trip in practice (forum discussions mention it but don't give measured numbers). The C++ TCP plugin (NAJEMWEHBE) claims ~50ms; Remote Control HTTP is likely similar or slightly higher due to HTTP overhead. Not a blocker for spike.
5. **SSH port-forward reliability with UE Remote Control**: No community examples of mantis-style remote-SSH architecture. This is the genuinely novel piece of our use case. Spike should explicitly validate SSH tunnel + Remote Control HTTP connectivity as its first milestone.

---

## Sign-off

**Legolas** — Mode A analytical research  
**Delivered:** 2026-06-07  
**Commission:** `agentic_orchestration/dispatches/2026-06-07-legolas-ue-mcp-prior-art-research.md`  
**Output path:** `agentic_orchestration/legolas/research/2026-06-07-ue-mcp-prior-art/synthesis.md`  
**Verdict:** REFERENCE+BUILD  
