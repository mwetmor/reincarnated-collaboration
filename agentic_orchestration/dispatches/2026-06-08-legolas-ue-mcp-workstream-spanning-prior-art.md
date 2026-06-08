# Dispatch — Legolas Mode A Research: UE + MCP Workstream-Spanning Ecosystem Inventory + Needs Mapping

**Date:** 2026-06-08
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-07 ratification ("Please write both of these (legolas and design recognition) into tomorrow's session") + Matt 2026-06-08 scoping refinement ("find everything available... then we can review the data wholistically and make design decisions") + Matt 2026-06-08 "rescope confirmed, fire it"
**To:** legolas (researcher / scout; Mode A analytical research)
**Cycle:** Pre-MCP-bridge-spike + pre-WS1-WS5-commissioning research investment; informs MCP bridge spike scope expansion AND workstream-commission tooling-awareness AND build-vs-adopt-vs-extend posture
**Type:** Mode A — analytical research; ecosystem discovery + capability inventory + needs-lens synthesis; not a catalogue crawl
**Cost budget:** $0 LLM (web fetch + analysis); ~2-4 hr legolas wall-clock
**Critical anchors:**
- `agentic_orchestration/dispatches/2026-06-07-legolas-ue-mcp-prior-art-research.md` (PRIOR commission — creation-moment-scoped; this commission EXTENDS not replaces)
- `agentic_orchestration/legolas/research/2026-06-07-ue-mcp-prior-art/synthesis.md` (PRIOR synthesis — REFERENCE+BUILD verdict; 5+ implementations identified; use as INVENTORY NUCLEUS to extend)
- `agentic_orchestration/dispatches/2026-06-07-david-h-ue-remote-control-mcp-bridge-spike.md` (the spike whose scope this research may revise)
- `agentic_orchestration/dispatches/2026-06-07-david-h-earth-avatar-creation-moment-vertical-slice-spike.md` (the vertical-slice spike whose execution pattern this research informs)
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (foundational architectural commitment driving the spike chain)
- `agentic_orchestration/mantis/research/ue-architecture-validation-spike-2026-06-06/port-workstream-gating-verdict.md` (mantis spike GREEN — WS1-WS5 unblocked architecturally)

---

## 0. TL;DR

The PRIOR commission (2026-06-07) was **creation-moment-scoped** — surveyed UE-MCP prior art through the narrow lens of one scene. Matt surfaced the scoping gap: we don't just need MCP coverage for the creation moment; we need it for the full WS1–WS5 port + production chain, plus general gameplay-code iteration. AND Matt heard via mobile-Claude conversation about a "recently created universal UE 5.7 extension allowing 20+ MCP connection types with many actions per type" — which may or may not be one of the implementations the prior synthesis already surfaced (remiphilippe/mcp-unreal with 48 tools across 17 categories; NAJEMWEHBE/unreal-ai-connection with 147 tools across 15 categories) OR may be something the prior commission missed.

**This commission rescopes the research as ecosystem discovery first, needs mapping second.** Per substrate-led discipline (Discipline #41 at the research-scoping layer): don't pre-impose what we need; let the MCP+UE ecosystem vote, THEN apply the workstream lens at synthesis-time.

**Deliverable: three-part synthesis.** Part A = comprehensive capability inventory (no needs filter). Part B = workstream-lens mapping applied to inventory. Part C = design-decision feedstock (build-vs-adopt-vs-extend posture; MCP bridge spike scope implications; Blueprint editing scope-in/-out revisit; productionization viability).

**Timeline:** ~2-4 hr legolas wall-clock as sub-agent invocation.

---

## 1. Methodological framing — why this commission's structure differs from the prior

### 1.1 The shift: needs-driven → ecosystem-discovery

The prior commission (2026-06-07) was needs-driven — Q1-Q6 framed per use case (UE+MCP existing implementations; UE Remote Control API; DCC-tool patterns; UE Python alternative; AI-driven game dev SOTA; auth/security). That framing pre-imposes the project's current model of what MCP capabilities we need.

**The risk:** a tool/extension may exist that exposes capabilities we haven't yet imagined we'd want. A per-need keyword crawl misses it because it doesn't name itself by our vocabulary.

**The rescope:** discover the MCP+UE ecosystem comprehensively as substrate inventory, THEN apply the workstream lens at synthesis-time. Same structural pattern as the style-register decision per `canonical/story/style-register.md` — the catalogue is scored comprehensively; consumption applies the filter, not the crawl. Same structural pattern as Discipline #41 (pre-authored taxonomy interrogation) at the research-scoping layer — the substrate votes.

### 1.2 What this commission EXTENDS vs REPLACES

**EXTENDS (not redoes):** the prior synthesis's 5+ implementations (chongdashu/unreal-mcp, remiphilippe/mcp-unreal, NAJEMWEHBE/unreal-ai-connection, ChiR24/Unreal_mcp, Flux-Point-Studios/unreal-mcp, ayeletstudioindia/unreal-analyzer-mcp) are the **inventory nucleus.** Don't re-survey what's already characterized; deep-extend characterization and find what was missed.

**ADDS:** comprehensive ecosystem crawl beyond the prior survey's GitHub-topic + community-listing scope. Specifically:
- MCP server registries (the official Anthropic-blessed registry + mcpservers.org + Awesome MCP catalogues)
- GitHub topic-crawl with broader keywords (not just `unreal-mcp` / `ue-mcp` but `mcp-server` + `unreal-engine`, `ue5` + `model-context-protocol`, etc.)
- Marketplace presence (Unreal Marketplace / FAB MCP-tagged offerings)
- Recent (last 30-60 days) blog posts, dev journals, Discord-announcement threads
- Twitter/X recent announcements (last 30 days)
- The specific 20+-connection-type UE-5.7 extension Matt heard about (see § 2.3)

**ADDS:** workstream-lens mapping (Part B). The prior synthesis returned REFERENCE+BUILD verdict on the question "does prior art cover the spike's needs." This commission asks the broader question "does prior art cover each of WS1-WS5 + general iteration's needs."

### 1.3 Substrate-led discipline compliance

Per `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` Pattern 6 + Discipline #41: don't pre-impose taxonomy where substrate should vote. Part A inventory must be **capability-honest** — record what each implementation actually exposes, even if it's a capability our workstreams don't currently use. Adjacent capabilities surfaced during Part A may prompt design conversations we haven't yet had.

Per `engineering-disciplines.md` Discipline #25 (semantic-layer rep-audit): bold claims in repository READMEs ("20+ connection types"; "production-ready"; "147 tools") get verified against actual code, not just trusted as marketing copy. Rep-audit is mandatory for any implementation considered for adoption.

---

## 2. Part A — Ecosystem capability inventory (no needs filter)

### 2.1 Inventory table schema

Build a master capability table. One row per discovered server / extension / implementation / plugin / bridge. Required columns:

| Column | Required content |
|---|---|
| **name** | Repository name or canonical identifier |
| **maintainer** | Organization / individual handle |
| **source_url** | Primary repo URL or distribution URL |
| **license** | Specific license (MIT / Apache-2.0 / GPL / proprietary / unclear) |
| **freshness** | Last-commit date; commit-frequency last 90 days; maintainer-active indicator |
| **ue_version_support** | Specific UE versions explicitly supported (5.5 / 5.6 / 5.7 / 5.7.4 etc.); "5.7" specifically called out where relevant |
| **architecture_pattern** | C++ plugin + TCP / C++ plugin + HTTP / Remote Control wrapper / Python-binding / Go-binary / TypeScript-server / Blueprint-binding / hybrid; categorize cleanly |
| **connection_type_count** | If implementation organizes by "connection types" or "categories," count + list |
| **action_count_per_type** | Tools per category — count + sample names |
| **total_tool_count** | Total exposed MCP tools (this is the headline capability metric) |
| **install_pattern** | Self-contained binary / plugin-build-required / Python+Plugin / Docker / etc. |
| **public_api_surface** | Live-editor control / headless commandlet / build automation / asset inspection / runtime-game ops / hybrid; categorize |
| **stars + forks** | GitHub social signal (treat as soft maturity proxy only; quality > stars per first synthesis's NAJEMWEHBE observation) |
| **test_coverage** | Test suite presence + count + CI integration (engineering-quality signal) |
| **rep_audit_status** | Per Discipline #25: bold-claim verification status (verified / unverified / partially verified); any discovered discrepancies between README claims and actual code |
| **gandalf_review_notes** | Any landscape-context observation that wouldn't fit elsewhere (e.g., "fork of chongdashu with 6 added tools"; "appears abandoned after 2025-12") |

### 2.2 Crawl scope expansion

Crawl broader than the prior commission. Specifically search:

**GitHub topic-crawl (extended keyword set):**
- `unreal-mcp` / `ue-mcp` / `ue5-mcp` / `ue57-mcp` (prior commission's scope)
- `mcp-server` + (`unreal-engine` / `ue5` / `ue4` / `ue-editor`)
- `model-context-protocol` + (`unreal` / `ue` / `game-engine`)
- `unreal-engine-ai` / `ue-ai-bridge` / `ue-llm` (adjacent semantic space)
- `unreal-remote-control` + AI / MCP / LLM (Remote Control adjacency)
- `unreal-python` + MCP (Python-binding adjacency)
- `blueprint-editor` + MCP / AI (Blueprint-authoring adjacency)
- `niagara` + MCP / AI / scripting (VFX-iteration adjacency)
- `unreal-sequencer` + MCP / AI (cinematics adjacency)
- `unreal-datatable` + MCP / AI (data-layer adjacency)

**MCP server registries:**
- Official Anthropic MCP server registry (whatever URL is current; the modelcontextprotocol.io GitHub registry or successor)
- mcpservers.org (referenced in prior synthesis)
- Awesome-MCP-Servers GitHub repositories (multiple exist; survey at least 2-3)
- mcp.so (community listing site)
- Smithery.ai or other emerging MCP-server discovery surfaces if encountered

**Marketplace + plugin distribution:**
- Unreal Marketplace + FAB search for "MCP" / "model context protocol" / "AI assistant" / "AI bridge" / "Claude" / "LLM" + UE compatibility
- VS Code marketplace MCP extensions that target UE (some MCP servers ship as VS Code extensions wrapping the protocol)
- Cursor/Claude Desktop ecosystem package listings

**Recent dev-journal + community-channel crawl (last 60 days):**
- Epic Developer Community forums "MCP" / "AI" + UE 5.7 threads
- Reddit r/unrealengine "MCP" / "Claude" / "AI assistant" recent posts
- DEV.to / Medium / Hashnode UE + MCP posts since 2026-04 onward
- Hacker News submissions matching UE + MCP / Claude UE / AI + game engine
- Anthropic blog posts mentioning UE / game engines / 3D tools
- Twitter/X recent (last 30 days) announcements with `#UnrealEngine` + (`#MCP` / `Claude Code` / `MCP server`)

**DCC-tool MCP context (light coverage; prior synthesis already covered some):**
- Verify Blender-MCP, Maya-MCP, Houdini-MCP, Godot-MCP, Unity-MCP capability shapes (1-row each) for cross-engine landscape context. Do NOT deep-dive — these are reference data points only.

### 2.3 Specific verification target — the 20+-connection-type UE-5.7 extension

Matt heard via mobile-Claude conversation 2026-06-08 about "a recently created universal extension for UE 5.7 that allowed 20+ MCP connection types with many actions within each type." This may be:

- **Hypothesis A:** It IS one of the prior synthesis's already-identified implementations (most likely NAJEMWEHBE/unreal-ai-connection with 147 tools across 15 categories; or remiphilippe/mcp-unreal with 48 tools across 17 categories) — counted differently or characterized differently in mobile-Claude's response than in our prior synthesis. If so: rep-audit the implementation against the 20+/many-per-type characterization claim.

- **Hypothesis B:** It is a DIFFERENT implementation the prior commission missed. If so: surface it in Part A inventory with full row + rep-audit pass.

- **Hypothesis C:** Mobile-Claude's response was inaccurate or hallucinated. If so: Part A inventory will show what genuinely exists vs the misattributed claim; report as nuance in Part C.

**Verification methodology:** search GitHub recent (last 60 days) UE + MCP + "20" or "twenty" + "connection types" or "categories"; search Anthropic registry and Awesome lists for any UE entry claiming 20+ types; cross-check against prior synthesis's 5+ entries; rep-audit any match.

### 2.4 Anti-patterns for Part A

- **Don't filter by current workstream needs.** Inventory is needs-blind by construction. Capability "Render BIK video preview from Sequencer" is recorded even if our WS3 doesn't currently use BIK — adjacents matter.
- **Don't auto-trust README claims.** Per Discipline #25 rep-audit: spot-verify tool counts, UE version claims, "production-ready" claims against actual code structure when an implementation is a candidate for adoption.
- **Don't redo what's already characterized.** The prior synthesis's nucleus (5+ implementations) is starting state, not work to repeat. Deep-extend characterization where prior was thin; survey freshly only what's new.
- **Don't enumerate every minor fork.** Many UE-MCP repos are forks of chongdashu/unreal-mcp; record forks with substantive divergence (added tools, different architecture, active maintenance) but skip pure-mirror forks.

---

## 3. Part B — Workstream-lens mapping

After Part A inventory is comprehensive, apply WS1–WS5 + general-iteration lens to the inventory. Per workstream, identify:

- Which inventory entries cover the workstream's likely tooling needs (full / partial / minimal)
- Specific capability gaps (workstream need X is unaddressed by any inventory entry)
- Quality / production-readiness of coverage (experimental / production-suitable / hybrid)
- License + commercial-use compatibility for adoption-or-extension path

### 3.1 WS1 — Data layer port (engine → UE)

Needs to investigate:
- Batch asset import (mesh, texture, material from external JSON / file system)
- DataTable manipulation (engine kit-data → UE DataTable rows; programmatic CRUD)
- Asset Registry queries (resolve asset references; cross-asset dependency walking)
- Build configuration scripting (per-platform config; cook target switching)
- Engine JSON ingestion pipeline integration (consumes the cosmograph-pivot JSON packet shipped from engine offline pre-generation)

### 3.2 WS2 — Rendering layer (Niagara VFX, materials, lighting)

Needs to investigate:
- Niagara authoring patterns (HTTP-driven parameter iteration; emitter creation; module configuration; bound-parameter exposure)
- Material instance management (parameter set, parent material swap, dynamic instance creation)
- LOD setup (mesh LOD chain; material LOD; HLOD)
- Lumen / Lighting config (Lumen scene config; Reflection Capture; Sky Light)
- Per-skill VFX asset selection consuming Phase 6 visual coalescence output

### 3.3 WS3 — Materialization cinematic

Needs to investigate:
- Sequencer manipulation (track creation; keyframe authoring; camera transform animation; spawn/destroy events)
- Camera animation (cinematic camera; CineCamera Actor; FOV/focus animation)
- Audio cueing (Sound Cue trigger; Wwise/MetaSounds if relevant)
- Materialization-cinematic trigger logic per Earth-Avatar canonical § 2.1 scene

### 3.4 WS4 — Continuity / save-load

Needs to investigate:
- Save game systems (SaveGame class; programmatic save/load; runtime serialization)
- Asset persistence patterns (mostly runtime; less MCP-relevant — record coverage but note relative deprioritization)

### 3.5 WS5 — Mobile polish

Needs to investigate:
- Mobile preview launch (mobile preview PIE; Android/iOS specific)
- Platform-specific build settings (per-platform .ini overrides; device-profile management)
- Perf profiling triggers (Insights / Trace start/stop; stat capture)

### 3.6 General iteration + gameplay code authoring

Needs to investigate:
- PIE start / stop / pause control
- Log file tailing (Output Log capture; specific category filtering)
- Hot-reload (Live Coding integration; C++ recompile; Blueprint reinstancing)
- Breakpoint manipulation (Blueprint debugger; C++ debugger if MCP-bridged)
- **Blueprint editing scope-in / scope-out revisit** (prior commission recommended OUT for creation-moment scope; workstream-spanning view may revise — Blueprint editing is load-bearing for lasso input handlers, ingredient drag-drop, tablet drawing handler per Earth-Avatar canonical § 2.3 + § 2.5 design contributions Element 3 + Element 5, materialization-cinematic triggers, hand-authored gameplay logic across WS1-WS5)

### 3.7 Workstream-lens mapping deliverable shape

Per workstream, produce a coverage table:

| Workstream Need | Inventory Coverage (entries) | Quality Tier (full / partial / minimal / absent) | Recommended Action (adopt / extend / build / defer) |
|---|---|---|---|

Plus a textual synthesis per workstream identifying the top 1-2 candidate implementations for adoption-or-extension, with rationale.

---

## 4. Part C — Design-decision feedstock

Synthesize Part A + Part B into design-decision input. Required output sections:

### 4.1 Build-vs-adopt-vs-extend posture

Given the comprehensive landscape: what's the recommended posture?

- **Adopt one implementation outright** (most-coverage entry, license-compatible, maintainer-active, rep-audit-clean) — name it, justify
- **Adopt one + extend** (use as base, add capabilities) — name the base, name the gaps
- **Adopt multiple** (different implementations for different workstreams) — name the assignments
- **Build from scratch informed by reference** (prior synthesis's REFERENCE+BUILD posture upheld at broader scope) — name the references
- **Pivot away from MCP entirely** (if landscape is too immature or fundamentally mismatched) — justify

### 4.2 MCP bridge spike scope implications

The current MCP bridge spike commission (`2026-06-07-david-h-ue-remote-control-mcp-bridge-spike.md`) was scoped as "Remote Control HTTP MVP for creation moment." Per Part B findings, does scope expand? Specifically:

- Does Remote Control HTTP MVP remain the right primary bridge, or should the spike evaluate a different architecture (C++ plugin + TCP per chongdashu; Go binary + Remote Control per remiphilippe; native C++ + Python bridge per NAJEMWEHBE)?
- Should the spike include additional bridge capabilities beyond Remote Control (Niagara HTTP; DataTable CRUD; Sequencer manipulation; etc.)?
- Should the spike pivot to evaluation-of-existing rather than from-scratch build?

### 4.3 Blueprint editing scope-in / scope-out revisit

Prior commission recommended scope-OUT for creation moment. Per workstream-spanning lens + Earth-Avatar canonical § 2.3 + § 2.5 design contributions (tablet drawing input handler; lasso input handler; ingredient drag-drop; materialization-cinematic triggers), Blueprint editing capability is load-bearing across the workstream chain. Revisit:

- Which inventory entries have meaningful Blueprint editing coverage (node graph CRUD; variable management; event binding)?
- Is the maturity sufficient to integrate as part of MCP bridge spike or vertical-slice spike?
- If not: should Blueprint authoring remain human-driven across all workstreams (no MCP automation), or partial-automation possible (e.g., simple property edits via MCP; complex node-graph editing human-driven)?

### 4.4 Productionization viability

If the MCP bridge becomes keeper-tooling (not throwaway spike), what does production-grade coverage look like?

- Which inventory entry has the strongest production-readiness signal?
- License + commercial-use compatibility for our project?
- Maintainer-activity signal (project will be maintained 6-12 months out)?
- Auth / security posture for productionization?

### 4.5 Open questions for gandalf review

Surface anything that requires gandalf design decision rather than legolas research determination. Examples:
- "X implementation covers WS2 Niagara HTTP but requires UE 5.8 — gandalf decides whether to upgrade UE version or accept the gap"
- "Y implementation has commercial-use license restriction — gandalf decides whether to accept restriction or build alternative"
- "Z capability is not covered by any inventory entry — gandalf decides whether to build, defer, or scope out"

---

## 5. Methodology

Standard Mode A pattern per legolas OP:

- Web search across extended-scope registries + GitHub + forums + community discussions per § 2.2
- Document sources with URLs + dates + maintainer-activity signals
- Build Part A inventory table comprehensively before applying Part B lens
- Synthesize Part B per workstream from inventory
- Compose Part C from Parts A + B
- Inline-cite all sources

**Rep-audit (Discipline #25) — mandatory triggers:**
- Any implementation under consideration for adoption (Part C § 4.1)
- Any implementation claiming 20+ connection types (§ 2.3 verification target)
- Any implementation claiming "production-ready" / "production-suitable" status
- Any implementation claiming UE 5.7 native support (vs older-UE-version-with-claimed-5.7-compatibility)

Rep-audit method: clone or browse repo via GitHub web; verify tool count by counting actual MCP tool registrations in source; verify UE version by checking .uplugin manifest + build.cs target version; verify "production-ready" claim by examining test coverage + recent issue activity + maintainer response patterns.

**If methodology consultation needed at a research subtopic:** surface to gandalf via inline note in deliverable. Examples: unclear whether a discovered implementation belongs in inventory (boundary question); unclear whether a rep-audit discrepancy is meaningful or noise.

---

## 6. Deliverable

Synthesis file at `agentic_orchestration/legolas/research/2026-06-08-mcp-workstream-spanning-prior-art/synthesis.md`.

Required structure:

- **TL;DR** (1 paragraph — landscape headline + Part C recommendation headline)
- **Part A — Capability inventory** (master inventory table per § 2.1 schema + per-entry detailed assessments for top-5 to top-10 most-relevant implementations + § 2.3 20+-type verification target findings)
- **Part B — Workstream-lens mapping** (per-workstream coverage tables + textual synthesis per WS1-WS5 + general iteration + Blueprint editing scope revisit)
- **Part C — Design-decision feedstock** (§ 4.1 build-vs-adopt-vs-extend posture + § 4.2 MCP bridge spike scope implications + § 4.3 Blueprint editing scope revisit + § 4.4 productionization viability + § 4.5 open questions for gandalf review)
- **Sign-off**

Estimated length: 6-12 pages markdown. Substantially longer than the prior commission's 2-5 pages because the inventory + workstream-lens + design-feedstock structure expands scope.

---

## 7. Verdict shapes for design-decision recommendations

Possible Part C § 4.1 recommendation outcomes:

| Recommendation | Trigger |
|---|---|
| **ADOPT-OUTRIGHT** | One inventory entry has comprehensive WS1-WS5 + general-iteration coverage at production-suitable quality, license-compatible, maintainer-active, rep-audit-clean. MCP bridge spike pivots to evaluation + adoption. |
| **ADOPT-AND-EXTEND** | Strong base implementation exists but with identified workstream gaps. MCP bridge spike adopts base + extends to fill named gaps. |
| **ADOPT-MULTIPLE** | Different implementations cover different workstreams optimally (e.g., remiphilippe for WS1-WS3; NAJEMWEHBE for general-iteration Blueprint editing). MCP bridge spike evaluates per-workstream assignment. |
| **REFERENCE+BUILD (upheld)** | Prior synthesis verdict holds at broader scope — no single implementation is adoption-ready; build from scratch informed by multiple references. |
| **PIVOT TO PYTHON-SCRIPTING** | Workstream-spanning landscape shows MCP coverage is too immature; UE Python scripting via SSH provides simpler architecture for our use case. MCP bridge spike defers. |
| **DEFER MCP** | Landscape sufficiently immature OR our needs sufficiently exotic that MCP bridge investment doesn't yet pay back. Continue manual UE-editor iteration across all workstreams. |
| **HYBRID** | Combination — e.g., adopt one implementation for WS2 + build custom for WS1 + Python-scripting for general iteration. |

---

## 8. Anti-patterns

- **Don't pre-filter inventory by current workstream needs.** Part A inventory is needs-blind by construction. Capabilities adjacent to our current model are recorded — they may prompt design conversations we haven't yet had.
- **Don't auto-trust README claims.** Rep-audit (Discipline #25) is mandatory for adoption candidates + 20+-type claim verification + UE 5.7 claims + production-ready claims.
- **Don't redo the prior synthesis's nucleus from scratch.** The 5+ implementations characterized at `agentic_orchestration/legolas/research/2026-06-07-ue-mcp-prior-art/synthesis.md` are starting state — extend characterization where prior was thin, survey freshly only what's new.
- **Don't deep-dive UE Remote Control API documentation** — surface-level coverage was sufficient in prior synthesis; full API documentation is mantis's job during spike execution.
- **Don't try to BUILD an MCP server** — research only; spike builds.
- **Don't recommend Part C posture without clear inventory evidence** — recommendations grounded in cited Part A inventory + Part B workstream-lens mapping, not speculation.
- **Don't enumerate every fork-mirror.** Forks of chongdashu/unreal-mcp with no substantive divergence are skipped; forks with added tools / different architecture / active maintenance are recorded.

---

## 9. Sign-off

**Authored:** gandalf 2026-06-08 per Matt 2026-06-07 ratification + 2026-06-08 scoping refinement following Matt's mobile-Claude conversation surfacing the "20+ connection-type UE-5.7 extension" reference point AND Matt's 2026-06-08 "rescope confirmed, fire it" authorization.

**Authority:** gandalf cross-cutting research-commission authority for Mode A analytical research informing pre-spike + pre-workstream-commission scoping decisions; substrate-led discipline at research-scoping layer per Discipline #41 extension.

**Routing:** legolas executes Mode A sub-agent invocation immediately upon dispatch reaching legolas; returns synthesis findings inline + writes deliverable to disk path per § 6.

**Empirical-evidence trigger for MCP bridge spike re-scoping + WS1-WS5 commission tooling-awareness:** legolas synthesis Part C recommendations per § 7 — gandalf reviews Part A holistically with Matt + amends MCP bridge spike commission AND WS1-WS5 commission templates before David-H fires execution.

**Composition with prior commission:** this commission EXTENDS not replaces `2026-06-07-legolas-ue-mcp-prior-art-research.md`. Prior synthesis's REFERENCE+BUILD verdict is provisional pending this commission's broader-scope findings.

**End of dispatch.**
