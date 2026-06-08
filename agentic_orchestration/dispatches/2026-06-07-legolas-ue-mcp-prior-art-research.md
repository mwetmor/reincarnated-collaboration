# Dispatch — Legolas Mode A Research: UE + MCP Prior Art Survey

**Date:** 2026-06-07
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-07 ratification ("fire legolas research commission and invoke legolas immediately as a sub agent") following gandalf surface that pre-spike research was not done
**To:** legolas (researcher / scout; Mode A analytical research)
**Cycle:** Pre-MCP-bridge-spike research investment; informs MCP bridge spike scope + may discover existing implementations to fork+adopt
**Type:** Mode A — analytical research; web survey + synthesis; not a catalogue crawl
**Cost budget:** $0 LLM (web fetch + analysis); ~1-2 hr legolas wall-clock
**Critical anchors:**
- `agentic_orchestration/dispatches/2026-06-07-david-h-ue-remote-control-mcp-bridge-spike.md` (the spike this research informs)
- `agentic_orchestration/mantis/research/ue-architecture-validation-spike-2026-06-06/port-workstream-gating-verdict.md` (mantis surface that triggered the spike)
- Anthropic MCP documentation
- Unreal Engine Remote Control Plugin documentation

---

## 0. TL;DR

Survey existing prior art for UE + MCP integration before David-H + mantis fire the MCP bridge spike. Honest gap: gandalf authored the spike commission as from-scratch engineering without checking for existing implementations. Brief Mode A research investment reduces risk of reinventing OR going down dead-end paths.

**Deliverable:** synthesis findings document with structured assessment of prior art + recommendations for spike scope.

**Timeline:** ~1-2 hr legolas wall-clock as sub-agent invocation.

---

## 1. Research questions

### 1.1 Q1 — Existing UE + MCP implementations

Has anyone published an MCP server for Unreal Engine?

- Search Anthropic MCP server registry / community lists (mcp.so, official Anthropic docs, GitHub topic:mcp-server)
- Search GitHub for "unreal-mcp" / "ue-mcp" / "unreal-remote-control-mcp" or similar
- Search Reddit r/unrealengine / Twitter / Hacker News for community discussion
- Search Anthropic Discord MCP discussions if accessible

If exists: assess maturity + license + maintainability + feature coverage. Could we fork+adopt rather than build from scratch?

### 1.2 Q2 — UE Remote Control Web API documentation + community gotchas

Survey what the UE Remote Control Plugin Web API actually exposes + what's reliable in practice:

- Official UE Remote Control documentation (Epic docs)
- Community forum discussions (Unreal forums, Reddit r/unrealengine, r/unrealengine community guides)
- Blog posts / dev logs from virtual production studios using Remote Control
- Stack Overflow tagged questions for UE Remote Control

Specifically:
- What HTTP endpoints exist by default?
- What requires project-side Preset configuration?
- Latency characteristics in practice (per-request roundtrip; throughput limits)?
- Common failure modes / gotchas?
- WebSocket vs HTTP — which is more reliable for our use case?
- Authentication / security defaults?

### 1.3 Q3 — DCC-tool MCP server patterns

Other DCC (Digital Content Creation) tools likely have community MCP servers — established patterns translate cleanly. Survey:

- Blender MCP servers (most likely candidate given Blender's Python API + open community)
- Maya / 3ds Max MCP servers (Autodesk DCC tools; possibly enterprise-built)
- Houdini MCP servers (SideFX has Python; possibly community)
- Godot MCP servers (open-source; AI-friendly community)
- Unity MCP servers (if anyone has built Unity equivalents; comparison point for UE)

For each found: architecture pattern (HTTP wrapper vs language-binding vs IPC), tool surface scope, maintainer activity, lessons learned.

### 1.4 Q4 — UE Python scripting as alternative

UE has built-in Python scripting (Python Editor Script Plugin). Could mantis SSH-execute Python scripts directly instead of building an HTTP MCP wrapper?

- Survey UE Python API surface (what UE operations are scriptable via Python?)
- Survey community examples of Python automation in UE (build pipelines, asset processing, etc.)
- Compare: Python-script-via-SSH vs MCP-wrapper-around-Remote-Control — which is simpler architecture? Which has lower friction for mantis-as-Claude-Code-agent?
- Note: Python scripts can also call UE Remote Control programmatically; not exclusive

### 1.5 Q5 — AI-driven game development tooling state-of-the-art

What's the published state-of-the-art for AI assistants controlling 3D engines / game development tools?

- Cursor + Unity workflows (community discussions)
- Claude / ChatGPT + Godot patterns
- AI-pair-programming in UE Blueprint authoring
- Anthropic blog posts on Claude + 3D engines if any exist
- Industry conference talks (GDC, Unreal Fest) on AI tooling integration

Surface anything that's a known pattern worth adopting vs avoiding.

### 1.6 Q6 — Authentication / security patterns for editor automation

Local-only is fine for spike but worth knowing standard patterns:

- How does UE Remote Control handle authentication by default?
- Are there known security advisories for HTTP API exposure?
- For productionization: what auth patterns are recommended for AI-driven editor tools?

Light coverage; not a blocker for spike but useful for productionization planning.

---

## 2. Methodology

Standard Mode A pattern per legolas OP:
- Web search across registries + GitHub + forums + community discussions
- Document sources with URLs + dates + maintainer activity (when relevant)
- Synthesize per research question (Q1-Q6 above)
- Recommendations section: what should MCP bridge spike scope change based on findings?

If methodology consultation needed at a research subtopic: surface to gandalf via inline note in deliverable (rare for this commission; Mode A research is well-bounded).

---

## 3. Deliverable

Synthesis file at `agentic_orchestration/legolas/research/2026-06-07-ue-mcp-prior-art/synthesis.md`.

Required structure:
- TL;DR
- Per-question findings (Q1-Q6) with citations
- Recommendations for MCP bridge spike scope changes (if any)
- Open questions / surfaces for gandalf consideration
- Sign-off

Estimated length: 2-5 pages markdown.

---

## 4. Verdict shapes for recommendations

Possible recommendation outcomes:

| Recommendation | Trigger |
|---|---|
| **FORK+ADOPT** | Existing UE MCP server found with mature implementation + acceptable license + reasonable maintainer activity. MCP bridge spike pivots to evaluation + adoption rather than from-scratch build. |
| **REFERENCE+BUILD** | Existing UE MCP implementation found but inadequate (immature, abandoned, wrong license, narrow scope). MCP bridge spike still builds from scratch but informed by prior-art patterns + gotchas. |
| **BUILD AS PLANNED** | No existing UE MCP implementation found. MCP bridge spike proceeds as originally scoped per dispatch `2026-06-07-david-h-ue-remote-control-mcp-bridge-spike.md`. |
| **PIVOT TO PYTHON-SCRIPTING** | Q4 research surfaces that Python-script-via-SSH is materially simpler than MCP-wrapper architecture for our use case. MCP bridge spike pivots to evaluating Python scripting path; MCP wrapper deferred. |
| **HYBRID** | Combination — e.g., adopt existing MCP server for core ops + add UE Python scripting for specialized operations. |

---

## 5. Anti-patterns

- **Don't crawl** — this is Mode A analytical, not Mode B catalogue. Light-touch web search; not exhaustive enumeration.
- **Don't deep-dive UE Remote Control API documentation** — surface-level survey sufficient; full API documentation is mantis's job during spike execution.
- **Don't try to BUILD an MCP server** — research only; spike builds.
- **Don't recommend architectural pivots without clear evidence** — recommendations grounded in cited prior art, not speculation.

---

## 6. Sign-off

**Authored:** gandalf 2026-06-07 per Matt ratification "fire legolas research commission and invoke legolas immediately as a sub agent" following gandalf surface that pre-spike research gap existed.

**Authority:** gandalf cross-cutting research-commission authority for Mode A analytical research informing pre-spike scoping decisions.

**Routing:** legolas executes Mode A sub-agent invocation immediately; returns synthesis findings inline + writes deliverable to disk path per § 3.

**Empirical-evidence trigger for MCP bridge spike re-scoping:** legolas synthesis recommendations per § 4 — if FORK+ADOPT or PIVOT recommended, gandalf amends MCP bridge spike commission before David-H fires execution.

**End of dispatch.**
