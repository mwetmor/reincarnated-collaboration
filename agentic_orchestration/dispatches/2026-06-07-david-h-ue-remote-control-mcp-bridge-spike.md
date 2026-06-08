# Dispatch — UE Remote Control MCP Bridge Spike (Pre-WS1 Tooling Investment)

**Date:** 2026-06-07
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-07 ratification of Tier 2 (D) pre-WS1 tooling spike + David-H-led-with-mantis-sub-agent operational pattern
**To:** David-H (PC-side orchestrator; PC-resident) — Mantis invoked as Pattern A sub-agent for UE-side validation
**Cycle:** Pre-WS1 tooling investment; informs vertical-slice spike execution + all subsequent mantis sessions
**Type:** SPIKE — empirical tooling-feasibility validation; build minimal viable MCP bridge; validate mantis can drive UE editor via MCP tools
**Cost budget:** $0 LLM / $0 Meshy / engineering session time only (~4-8 hr david-h + mantis)
**Time budget:** ~4-8 hr wall-clock across 1-2 sessions
**Critical anchors:**
- `agentic_orchestration/mantis/research/ue-architecture-validation-spike-2026-06-06/port-workstream-gating-verdict.md` § "Architectural surfaces for gandalf review" #2 (mantis recommendation)
- `agentic_orchestration/qa/findings/2026-06-07-mantis-ue-architecture-validation-spike-gate-2.md` INFO-3 (jack-ryan Gate-2 endorsement)
- `canonical/story/2026-06-07-federated-pc-team-architecture-commit.md` (David-H + mantis seam relationship)
- `matt_notes_handoff_docs/reincarnated-headless-ssh-handoff.md` (SSH operational reference; baseline for what MCP would replace/augment)
- Anthropic MCP documentation (search "Model Context Protocol" + "MCP server" if needed)
- Unreal Engine Remote Control documentation (search "UE Remote Control Plugin" + "Web API")

---

## 0. TL;DR

Build a minimal-viable MCP (Model Context Protocol) server that wraps Unreal Engine's built-in Remote Control Plugin Web API. Validates whether mantis (running under Claude Code on PC) can directly drive UE Editor via MCP tools — setting properties, running console commands, invoking Blueprint functions, manipulating actors — WITHOUT requiring Matt-pilot UE interaction relay.

**Why this matters now (post-spike-close):**
- Mantis Session 3 required Matt-pilot UE Editor for Phases 1-4 (criterion 3.2 + 3.4 + 3.6 + 3.7 STRETCH)
- Future workstreams (vertical-slice spike + WS1-WS5 production) involve substantially more UE Editor work
- Without MCP, every UE interaction requires Matt-pilot relay → slows execution + adds Matt-touches
- WITH MCP, mantis sub-agent invocations (per David-H-led orchestration pattern) directly query/set UE state → dramatically reduces friction

**Spike scope:** validate feasibility + characterize latency/reliability/ergonomics. NOT a production-grade build — prototype-grade MCP server sufficient to demonstrate the capability + identify scope for subsequent productionization.

**Spike verdict shape:** GREEN (works; productionize as full tooling) / YELLOW (works with caveats; document for future) / RED (doesn't work; fall back to Matt-pilot pattern for vertical slice + WS1-WS5).

---

## 1. Scope

### 1.1 What David-H produces (orchestration)

Delivery packet at `agentic_orchestration/david-h/notes/2026-06-07-ue-remote-control-mcp-bridge-spike/`:

| Artifact | Format | Purpose |
|---|---|---|
| `spike-findings.md` | markdown | Spike verdict (GREEN/YELLOW/RED) + mantis sub-agent invocation log + latency/reliability characterization + productionization recommendation |
| `mcp-server-prototype/` | directory | Minimal MCP server code (Python or TypeScript per implementation choice) wrapping UE Remote Control HTTP API |
| `session-boundary-memo.md` | markdown | David-H wind-down summary per OP § 5 |

### 1.2 What Mantis produces (sub-agent invocations)

Per David-H sub-agent invocations:
- UE Remote Control Plugin enabled in `C:\dev\reincarnated-unreal\Reincarnated\Reincarnated.uproject` (one-time setup)
- Validation tests: each MCP tool exercise documented (property-set; console-command; actor-place; Blueprint-function-invoke; etc.)
- Findings: latency per operation, reliability characteristics, error modes, ergonomics
- Recommendations for production MCP server scope (Phase 2 productionization if spike GREEN)

### 1.3 What spike does NOT produce

- **No production-grade MCP server.** Prototype-grade sufficient for capability validation.
- **No installation as default tooling.** Spike validates whether to invest in productionization; productionization is separate workstream.
- **No documentation of all UE Remote Control API surface.** Validate ~5-8 representative tool patterns; document what's needed for vertical slice + WS1-WS5 work.
- **No replacement of SSH operational reference.** SSH-headless-UE pattern remains operational; MCP adds live-editor-state access as augmentation.

---

## 2. Background — what MCP is + how it composes with UE

### 2.1 Model Context Protocol (MCP) — brief

MCP (Anthropic) is a standardized protocol for AI applications to interact with external systems via servers. Claude Code can invoke MCP servers as tools — read filesystem, query databases, call APIs, etc. MCP server = thin process that exposes a defined tool surface to Claude; protocol handles serialization + invocation + return.

Many MCP servers exist (filesystem, git, GitHub, etc.). Custom MCP servers are buildable for project-specific tools.

### 2.2 UE Remote Control Plugin — brief

Built into UE 5.x. Exposes Web API (HTTP + WebSocket) for remote editor control. Used in virtual production / broadcast / live performance contexts. Allows:
- Property setting on UObjects (cvars, actor properties, Blueprint variables, etc.)
- Function invocation on UObjects (call Blueprint functions, native UFUNCTIONs)
- Console command execution
- Actor manipulation (spawn, transform, destroy)
- Live editor state querying (selection, asset state, etc.)

Requires: UE Editor running with Remote Control Plugin enabled + Web Remote Control server started + project-side preset configurations exposing specific UObjects/properties for remote access.

### 2.3 The bridge — what to build

A small MCP server (Python or TypeScript) that:
1. Connects to UE Remote Control Plugin's HTTP API (defaults to `http://localhost:30010` or similar)
2. Exposes MCP tools wrapping common UE operations:
   - `ue.set_property(object_path, property_name, value)` — set property on UObject
   - `ue.call_function(object_path, function_name, args)` — invoke UFUNCTION
   - `ue.console_command(cmd)` — run console command
   - `ue.spawn_actor(class_path, location, rotation)` — spawn actor in level
   - `ue.get_property(object_path, property_name)` — query property value
   - `ue.list_assets(path_filter)` — list assets matching filter
3. Returns results to invoking Claude Code session (mantis sub-agent)

Implementation language is David-H's choice (Python via FastMCP / TypeScript via @modelcontextprotocol/sdk both viable). Recommend Python for ergonomic match with existing project tooling.

---

## 3. Spike execution (David-H orchestration)

### Phase 1 — Setup + plugin enablement (~30-45 min)

David-H invokes mantis sub-agent:
- Enable UE Remote Control Plugin in `Reincarnated.uproject` (Edit → Plugins → search "Remote Control" → enable + restart editor)
- Confirm Remote Control panel appears in editor (Window → Remote Control)
- Verify default HTTP server starts (`http://localhost:30010` or similar; check editor logs)
- Create a minimal Remote Control Preset exposing 2-3 representative properties for testing (e.g., a directional light's intensity + color; a static mesh actor's location)
- Validate Web API responds to test requests via `curl` or similar

Mantis returns: confirmation editor + plugin operational; preset URL paths + property paths for next phase.

### Phase 2 — MCP server prototype (~1-3 hr)

David-H invokes mantis sub-agent OR David-H authors directly (David-H's call):
- Pick implementation language (Python recommended)
- Install MCP SDK (`fastmcp` for Python OR `@modelcontextprotocol/sdk` for TypeScript)
- Wrap UE Remote Control HTTP API as MCP tools (start with 3-5 most useful: set_property, get_property, console_command, list_assets, spawn_actor)
- Implement minimal error handling (UE editor not running; property doesn't exist; type mismatch; etc.)
- Test MCP server starts cleanly
- Document MCP server installation + invocation pattern for Claude Code

### Phase 3 — Mantis sub-agent validation (~1-2 hr)

David-H invokes mantis sub-agent with MCP server registered:
- Test each MCP tool exercise (property set → query back; console command → verify; actor spawn → confirm in level; etc.)
- Latency measurements per operation
- Reliability characterization (error modes; timeouts; reconnection behavior)
- Ergonomics assessment (does mantis-as-Claude-Code-sub-agent flow feel natural with MCP tools? Or awkward?)
- Identify gaps: what UE operations are needed for vertical slice + WS1-WS5 work that aren't covered yet?

### Phase 4 — Verdict + productionization recommendation (~30-60 min)

David-H synthesizes:
- Spike verdict (GREEN / YELLOW / RED)
- If GREEN: productionization scope estimate (Phase 2 = full UE Remote Control API wrapper for project; ~1-2 weeks engineering)
- If YELLOW: document caveats; recommend prototype-as-is for vertical slice; productionization deferred
- If RED: document failure mode; vertical slice + WS1-WS5 fall back to Matt-pilot pattern; reconsider tooling investment later

Commits all artifacts + push (or surface push to Matt per established cycle pattern + push-credential gap workaround).

---

## 4. Verdict criteria

| Verdict | Criteria |
|---|---|
| **GREEN** | All 5 representative MCP tool exercises succeed; latency <1s per operation; reliable across 20+ invocations; mantis sub-agent flow feels natural; clear path to productionization for vertical slice + WS1-WS5 use |
| **YELLOW** | Most exercises succeed but with caveats (specific operations awkward; latency variable; some error modes require recovery logic); usable for vertical slice but full productionization needs scope investigation |
| **RED** | Fundamental blockers — UE Remote Control unavailable in 5.7 OR MCP integration incompatible OR latency unacceptable OR mantis-as-Claude-Code can't invoke MCP servers in current Claude Code version. Fall back to Matt-pilot pattern. |

---

## 5. Composition with downstream work

### 5.1 If GREEN — vertical-slice spike benefits immediately

Earth-Avatar Creation Moment Vertical-Slice Spike commission (separate dispatch authored this session) inherits the MCP bridge as primary execution pattern. David-H invokes mantis sub-agent per phase; mantis uses MCP tools to drive UE Editor; Matt-touch reduced dramatically.

### 5.2 If YELLOW — vertical-slice executes with hybrid pattern

Mantis uses MCP tools for code-controllable actions; Matt-pilot for actions MCP can't reach (UI-only operations, complex multi-step UE workflows). Slower than GREEN but faster than full Matt-pilot.

### 5.3 If RED — vertical-slice executes per Session-3 pattern

Matt pilots UE Editor; mantis directs + records; David-H orchestrates. Same as mantis Session 3 close pattern. Spike was worth firing — empirical refutation of tooling hypothesis is valuable.

### 5.4 Productionization path (if GREEN)

Post-spike productionization workstream (~1-2 weeks engineering):
- Expand MCP server to cover full UE Remote Control API surface
- Add project-specific tool patterns (Niagara emitter manipulation; Blueprint authoring; asset import workflows; etc.)
- Document tool usage patterns for mantis OP amendments
- Optionally: add MCP server auto-launch on UE Editor start (one-time setup eliminates per-session friction)
- Mantis OP amendment codifying MCP-driven workflow patterns

### 5.5 WS1-WS5 port commission scoping inherits

WS1-WS5 commission scoping (gandalf deferred to next session) inherits the MCP tooling outcome. Tooling-aware scoping is meaningfully different from tooling-naive scoping (different effort estimates per workstream; different mantis session profiles).

---

## 6. Cross-host coordination

David-H is PC-resident; mantis is PC-resident. Operating wholly within PC seam.

Mac-side coordination: gandalf (this session OR next gandalf session) consumes the spike verdict to inform vertical-slice + WS1-WS5 scoping. No cross-host coordination during spike execution.

If spike surfaces a cross-host implication (e.g., MCP server should live on Pi for centralized access?): David-H files consultation note at `agentic_orchestration/david-h/notes/<date>-consultation-mac-gandalf-mcp-architecture.md`; routes to Mac-gandalf for cross-host architecture decision.

---

## 7. Anti-patterns to avoid

- Productionizing the MCP server in this spike. Prototype-grade only; productionization is separate workstream.
- Wrapping the entire UE Remote Control API surface. Start with 3-5 representative tools; expand later.
- Building project-specific Niagara/Blueprint workflow automation in this spike. Validate the bridge; specialize later.
- Skipping latency measurement. Mantis ergonomics depend on responsive operations; characterize latency empirically.
- Falling into "MCP server architecture redesign" rabbit-hole. Use existing fastmcp / TypeScript MCP SDK patterns; don't invent.

---

## 8. Sign-off

**Authored:** gandalf 2026-06-07 per Matt ratification of Tier 2 (D) tooling spike + Pre-WS1 sequencing recommendation + David-H-led-with-mantis-sub-agent operational pattern.

**Authority:** gandalf cross-cutting design authority for tooling-spike commissions; David-H orchestrator authority for execution within PC seam per federated-team-commit § 5.1.

**Empirical-evidence trigger:** spike verdict (GREEN / YELLOW / RED) informs vertical-slice spike execution pattern + WS1-WS5 commission scoping per § 5.

**Recommended execution sequencing:** fire BEFORE OR IN PARALLEL with vertical-slice spike per Matt-prioritization. If both fired in parallel: vertical-slice can absorb MCP bridge mid-execution if spike GREEN; falls back to Matt-pilot if RED.

**Routing:** David-H consumes at session-start; executes per § 3; returns verdict to gandalf for vertical-slice + WS1-WS5 scoping integration.

**End of dispatch.**
