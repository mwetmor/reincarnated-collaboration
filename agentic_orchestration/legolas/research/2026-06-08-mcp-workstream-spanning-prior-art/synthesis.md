# Research — UE + MCP Workstream-Spanning Ecosystem Inventory + Needs Mapping — 2026-06-08

**Mode:** A (analytical; Pattern A-deep)
**Commissioner:** gandalf (story-and-design steward)
**Commission file:** `agentic_orchestration/dispatches/2026-06-08-legolas-ue-mcp-workstream-spanning-prior-art.md`
**Prior synthesis:** `agentic_orchestration/legolas/research/2026-06-07-ue-mcp-prior-art/synthesis.md` (used as inventory nucleus; EXTENDED not replaced)
**Crawl date:** 2026-06-08
**Sources consulted:** GitHub (17+ repositories), mcpservers.org, mcp.so, Docker Hub, StraySpark documentation and Epic Developer Community forum, PulseMCP, Glama.ai, strayspark.studio/docs

---

## TL;DR

The UE + MCP ecosystem has expanded dramatically beyond the six implementations characterized in the prior synthesis. At least **17 distinct implementations** are now confirmed, ranging from the lightweight (runreal, 17 tools, pure Python Remote Execution) to the industrially ambitious (StraySpark, 359 tools across 50+ categories, commercial, with bearer-token auth and production-grade transaction support). **Three implementations are strong adoption candidates** for different postures: (1) NAJEMWEHBE/unreal-ai-connection (MIT, 147 tools, 607 tests, UE 5.7.4, the highest engineering-rigor open-source option); (2) StraySpark (commercial, 359 tools, UE 5.7, the only production-grade option with auth, transaction safety, and PIE control — but requires commercial license for studio use); (3) remiphilippe/mcp-unreal (Apache-2.0, 49 tools, UE 5.7 native, single Go binary, narrowest install burden). The 20+-connection-type claim Matt heard via mobile-Claude is **most likely Hypothesis A** (already-identified implementation characterized differently): db-lyon/ue-mcp (21 tool categories, 569+ actions) and StraySpark (34-50+ categories) are both plausible sources; no genuinely new implementation matching "recently created universal UE 5.7 extension with 20+ connection types" was found that wasn't already in the prior nucleus or closely adjacent to it. **Part C recommendation: ADOPT-AND-EXTEND** — NAJEMWEHBE as the open-source base (UE 5.7.4 native, MIT, highest test coverage, 15 categories covering WS1-WS5 materially); extend with Sequencer depth and SSH-remote topology validation. StraySpark warrants evaluation as a commercial alternative if David-H's spike determines custom-build cost exceeds StraySpark's commercial license cost.

---

## Part A — Capability Inventory

### A.1 Master Capability Table

| # | Name | Maintainer | Source URL | License | Freshness | UE Version | Architecture | Categories | Total Tools | Install Pattern | Public API Surface | Stars/Forks | Test Coverage | Rep-Audit | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | unreal-mcp | chongdashu | https://github.com/chongdashu/unreal-mcp | MIT | Active; 33 commits; last ~2026 | 5.5+ | C++ TCP plugin (port 55557) + Python FastMCP MCP server | 4 domains | ~16 distinct capabilities | Visual Studio required (C++ build) + Python 3.12+ | Live editor: actor CRUD, Blueprint node graph, editor viewport | 2,000 stars / 322 forks | Not documented | PARTIALLY VERIFIED — "experimental" claim confirmed in README; Blueprint graph CRUD confirmed; tool count ~16 (not higher) | Highest star count; explicitly experimental; local-only topology assumed |
| 2 | mcp-unreal | remiphilippe | https://github.com/remiphilippe/mcp-unreal | Apache-2.0 | Active; v0.1.x; Go binary releases | 5.7 minimum | Go binary (zero deps); 3 layers: headless cmd exec + Remote Control HTTP (30010) + MCPUnreal plugin HTTP (8090) | 22 categories | 49 tools | Download pre-built Go binary; enable Remote Control Plugin + MCPUnreal plugin | Headless builds/tests, actor ops, Blueprint editing, Niagara, DataTable, Sequencer (absent) | 47 stars / 6 forks | Not documented | PARTIALLY VERIFIED — 49 tools confirmed (prior synthesis said 48; +1 on recount); 22 categories confirmed; NO Sequencer tools confirmed by recount; UE 5.7 confirmed | Best architecture reference for Remote Control HTTP wrapping pattern |
| 3 | unreal-ai-connection | NAJEMWEHBE | https://github.com/NAJEMWEHBE/unreal-ai-connection | MIT | Active; v0.9.1 (2026-05-23); v0.9.1-ue5.6 (2026-05-25) | 5.7.4 primary; 5.6 prebuilt binaries | C++ editor plugin + Python TCP bridge (port 18888); stdio MCP ↔ TCP JSON-RPC | 15 categories | 147 tools (110 C++ handlers + 37 bridge synthetic) | One-command install; plugin drops into `<Project>/Plugins/` | Full editor: Blueprint, Niagara, Level Sequences (Sequencer), DataTable, materials, actor ops, audio, camera, console, Python exec | 6 stars / 3 forks | 607 pytest cases; GitHub Actions CI; smoke test vs live editor | VERIFIED — 147 tool claim partially verified (C++ category sum = 103 not 110, but README claims 110; discrepancy ~7 tools; synthetic list confirms ~34 not 37; overall ~137-147 range; not fabricated, minor counting methodology difference); 607 tests confirmed; UE 5.7.4 confirmed | Highest engineering rigor; low star count likely new publication (May 2026); MIT |
| 4 | Unreal_mcp | ChiR24 | https://github.com/ChiR24/Unreal_mcp | MIT | Active; v0.5.30 (2026-06-05); 23 releases | 5.0–5.8 (5.8 preview) | TypeScript MCP server + C++ Automation Bridge plugin; dual transport: HTTP/SSE or WebSocket | 28+ categories | 35 tools (Docker image); 23 in broad-mode per prior | 28+ categories | npm/npx or Docker; C++ plugin build required | Live editor: animation, AI, assets, audio, BT, blueprints, chars, combat, GAS, char, geometry, input, interactions, inventory, lighting, materials, networking, navigation, performance, sequencer, sessions, skeletons, splines, textures, volumes, widgets, system | 686 stars / 128 forks | Unit tests referenced (npm run test:unit); no metrics published | PARTIALLY VERIFIED — UE 5.0-5.8 claim: .uplugin not directly checked; 686 stars confirms community traction; Docker Hub presence (294 weekly pulls) confirms deployment adoption; "production-ready" not explicitly claimed | Strong growth trajectory; Docker Hub publishing signals ops maturity; licensed MIT |
| 5 | Unreal_mcp (fork) | Flux-Point-Studios | https://github.com/Flux-Point-Studios/unreal-mcp | MIT (assumed) | Low activity | Unknown | Fork of chongdashu | ~16 | ~16 | Same as chongdashu | Same as chongdashu | Low | None | UNVERIFIED — treated as fork; skip per dispatch anti-pattern | Skip — no substantive divergence confirmed |
| 6 | unreal-analyzer-mcp | ayeletstudioindia | https://github.com/ayeletstudioindia/unreal-analyzer-mcp | MIT | Unknown | UE5 | TypeScript MCP server; read-only analysis of UE source | 1 (analysis) | ~10 analysis tools | npm | Read-only: source analysis, class hierarchy, API docs | Low | None | UNVERIFIED | Narrow scope — read-only code analysis; not editor control |
| 7 | vhcilab-unreal-engine-mcp | gingerol | https://github.com/gingerol/vhcilab-unreal-engine-mcp | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Scene building | Low | None | UNVERIFIED | Academic/lab use; insufficient metadata |
| 8 | **unreal-mcp (GenOrca)** | GenOrca | https://github.com/GenOrca/unreal-mcp | Apache-2.0 | Active; v1.5.0 | 5.6+ | Python MCP server + UnrealMCPython plugin (Python API bridge; no C++ recompile needed) | 8 categories | 84 tools | Python 3.11+, `uv` package manager, MCP client | Live editor via Python: actors, levels, assets, materials, Blueprint graph, Behavior Trees, UMG widgets, editor tools | 109 stars / 14 forks | Not documented | PARTIALLY VERIFIED — 84 tools confirmed; Python-only bridge confirmed (no C++ recompile); UE 5.6+ confirmed; Niagara absent confirmed | Distinctive: no C++ required; Python plugin bridge; BT authoring included |
| 9 | **ue5-mcp** | mirno-ehf | https://github.com/mirno-ehf/ue5-mcp | MIT | v1.0.0 (2026-02-14) | UE5 | UE5 editor plugin + local HTTP server + MCP wrapper | Blueprint-focused | Not specified | "Set up via Claude Code" prompt | Blueprint, material, AnimBlueprint editing | 56 stars / 17 forks | None documented | PARTIALLY VERIFIED — Blueprint-focused confirmed; tool count not extractable from public source | Narrow focus; useful for Blueprint-only use case |
| 10 | **ue5-mcp-bridge** | Natfii | https://github.com/Natfii/ue5-mcp-bridge | MIT (Attribution) | Active | 5.7 | Node.js stdio MCP server → UE5 HTTP backend (localhost:3000) | 10 categories | 30+ tools | Node.js 18+; requires HTTP endpoint | Level, actors, assets, scripts, viewport, Blueprints, AnimBPs, characters, materials, Enhanced Input, async task queue | 48 stars / 16 forks | 87 Vitest tests; 97% coverage | PARTIALLY VERIFIED — 30+ tools confirmed; 87 tests/97% coverage confirmed; UE 5.7 confirmed; architecture confirmed (Node.js bridge to HTTP endpoint) | Solid test coverage for bridge layer; depends on external HTTP endpoint implementation |
| 11 | **ue-mcp** | db-lyon | https://db-lyon.github.io/ue-mcp/ / https://github.com/db-lyon/ue-mcp | BUSL-1.1 (free: individuals/education; commercial license for studios) | Active; v1.0.79 (2026-06-06) | 5.4–5.7 Windows; 5.6+ Linux | TypeScript/Node.js MCP server (stdio) + WebSocket JSON-RPC → C++ bridge plugin; filesystem direct reads for config/INI | 21 categories | 569+ actions across 21 tool entry points | `npx ue-mcp init` interactive setup | Full editor: Levels, Blueprints, Materials, Assets, Animation, VFX, Landscape, PCG, Gameplay, GAS, Networking, UI, Editor, Reflection, Project, StateTree, plus YAML flow engine | 125 stars / 29 forks | Not documented | PARTIALLY VERIFIED — 21 categories confirmed (package.json version 1.0.79, description "21 tools, 569+ actions" confirmed); BUSL-1.1 license confirmed; UE 5.4-5.7 confirmed; commercial license required for studios | LICENSE IS LOAD-BEARING: BUSL-1.1 means studio use requires paid commercial license |
| 12 | **unreal-engine-mcp** | flopperam | https://github.com/flopperam/unreal-engine-mcp | MIT | Active | 5.5–5.7 | Dual: hosted (agent.flopperam.com, C++/Python) + open-source local (Python + C++ plugin) | 9 domains | 50+ (hosted); variable (local) | MIT for open source; hosted requires Fab/subscription | Blueprint authoring, materials, VFX, animation, landscape, AI/BT, cinematics, PCG, data assets | 1,000 stars / 190 forks | Not documented | PARTIALLY VERIFIED — 1,000 stars confirmed; dual-mode architecture confirmed; hosted vs open-source distinction confirmed | Hosted model introduces external dependency; open-source component is the relevant comparison point |
| 13 | **unreal-mcp** | runreal | https://github.com/runreal/unreal-mcp | MIT | Active; v0.1.1 (2025-06-03) | 5.4+ | TypeScript MCP server + UE built-in Python Remote Execution (no new plugin required) | 5 categories | 17 tools | npm; no new UE plugin | Asset management, Python execution, viewport control, object manipulation, project inspection | 106 stars / 24 forks | Not documented | PARTIALLY VERIFIED — 17 tools confirmed; no-new-plugin confirmed (uses built-in Python Remote Execution); UE 5.4+ confirmed | Architecturally distinctive: zero new plugin; uses UE's built-in Python exec; lowest install burden; fewest tools |
| 14 | **UEBlueprintMCP** | lilklon | https://github.com/lilklon/UEBlueprintMCP | MIT | Active; 9 commits | 5.7+ | Python MCP server + C++ plugin (TCP/JSON, port 55558); `FEditorAction` subclass pipeline | 7 categories | 60+ tools | Python + C++ plugin build | Blueprint CRUD, graph nodes, event dispatchers, Enhanced Input, materials, UMG widgets, editor ops | 33 stars / 5 forks | Not documented | PARTIALLY VERIFIED — 60+ tools confirmed; UE 5.7+ confirmed; C++ (80.7%) primary language confirms non-trivial plugin engineering | Blueprint-specialized; 7 categories all relate to Blueprint/material/widget authoring |
| 15 | **UnrealEngine5-mcp** | gimmeDG | https://github.com/gimmeDG/UnrealEngine5-mcp | MIT | Active | 5.6+ | Python MCP server + C++ plugin (TCP); BM25 RAG for UE Python API docs | 5 categories | 83 tools | Python 3.11+, uv; C++ plugin | Blueprint/GAS, editor tools, PCG, RAG search, Python exec | 7 stars / 3 forks | Not documented | PARTIALLY VERIFIED — 83 tools confirmed; RAG-powered Python scripting confirmed; no Niagara/Sequencer/DataTable confirmed | RAG for UE Python API is distinctive; GAS authoring depth is strong |
| 16 | **Unreal MCP Server** | StraySpark | https://www.strayspark.studio + https://www.fab.com/listings/aa699a85-04b1-4746-a29c-962fc3a78f55 | Commercial (Fab.com) | Active; latest release June 2026; Forum thread ongoing | 5.7 (Win64, Mac, Linux) | C++ plugin; HTTP JSON-RPC 2.0 (port 13579); game-thread dispatch; bearer-token + origin allow-list | 50+ categories (v3) | 359 tools (v3) | Pre-compiled binary via Fab.com; no compilation required | Full editor: 51 Blueprint tools, 12 Sequencer tools, 3 Niagara tools, 3 DataTable tools, 9 PIE tools, 8 source control tools, actor/level/materials/landscape/PCG/GAS/Enhanced Input/audio/MetaSound/physics | Price not confirmed (403 on Fab listing); 207 tools (v1); 305 tools (v2); 359 tools (v3 per docs) | No test metrics published | PARTIALLY VERIFIED — 359 tool claim: confirmed by official documentation; 50+ categories per v3 docs; bearer-token auth confirmed; production-safe scope gating confirmed; UE 5.7 confirmed; commercial license required confirmed | STRONGEST commercial option; only implementation with auth + scope gating + undo transactions; price unknown |
| 17 | **UnrealMotionGraphicsMCP** | winyunq | https://github.com/winyunq/UnrealMotionGraphicsMCP | MIT | Active | 5.6+ | Python MCP server + C++ `UmgMcpBridge` plugin (TCP) | 7 categories | 50+ tools | Python + C++ build | UMG, Sequencer (10 tools), Blueprint API (11 tools), Material/HLSL (11 tools) | 161 stars / 36 forks | Not documented | PARTIALLY VERIFIED — 50+ tools confirmed; UMG/Sequencer focus confirmed; UE 5.6+ confirmed | UMG + Sequencer depth is distinctive; token-efficiency optimization for context windows |

**Implementations skipped (forks with no substantive divergence):** jl-codes/unreal-5-mcp (chongdashu fork), VedantRGosavi/UE5-MCP (insufficient metadata), edi3on/py-ue5-mcp-server (minimal, FastMCP demo), AlexKissiJr/UnrealMCP (minimal), kvick-games/UnrealMCP (6 commands; early-stage), sallahboussettah-unrealmcp (minimal).

**Additional noted but not deep-characterized:** prajwalshettydev/UnrealGenAISupport (multi-LLM UE plugin, broader AI integration rather than pure MCP bridge), NAJEMWEHBE/UnrealClaudeMCP (11 tools, earlier/simpler version of the main unreal-ai-connection project), LOOMLE/loomle (MIT, Blueprint/PCG/Material/UMG focused, Fab install path; tool count not confirmed — listed on mcpservers.org but documentation insufficient for full characterization).

---

### A.2 Detailed Assessments — Top Implementations for Adoption/Extension Consideration

#### NAJEMWEHBE/unreal-ai-connection (Rep-Audit: PARTIALLY VERIFIED)

**Headline claim verification:** Prior synthesis cited "147 tools across 15 categories." Current README states 147 tools (110 C++ + 37 synthetic). The per-category C++ sum in the README resolves to 103, not 110; synthetic list names ~34 tools explicitly, not 37. The discrepancy is ~7-10 tools — likely a documentation lag from ongoing development rather than fabrication. The 15 categories are confirmed. Test count has grown from 581 (prior synthesis) to 607 (current), consistent with active development. License MIT confirmed.

**Key capabilities confirmed:**
- Blueprint/widget/animation: 20 C++ handlers + synthetic composition tools — includes `inspect_blueprint`, `edit_widget_tree`, `add_blueprint_node`, `connect_blueprint_pins`
- Niagara FX: `spawn_niagara_at_location`, `spawn_niagara_attached`, `set_niagara_user_param` — three tools
- Level Sequences (Sequencer): `add_camera_cut_track`, `add_audio_track`, `add_visibility_track`, `render_sequence_mrq` — 9 tools in category
- DataTable: `create_data_table`, `inspect_data_table` — present but thin (2 tools)
- Python execution: 5 tools including run_python_script capability
- Asset registry: 10 tools

**SSH/remote topology:** Architecture is C++ plugin binding 127.0.0.1:18888 + Python bridge stdio. The Python bridge is the MCP client endpoint — mantis connects to the bridge via stdio, which connects to the plugin over TCP. This is compatible with SSH port-forwarding of port 18888 (same pattern as Remote Control HTTP). No SSH-specific documentation found, but the local-TCP architecture is SSH-forwardable by construction.

**Maturity signal:** v0.9.1 released 2026-05-23 (recent). 607 tests + CI + smoke test discipline. Maintainer from Kuwait (HD Media). Low star count (6) is a genuine adoption-risk signal — community small; if maintainer goes quiet, the project is effectively orphaned. No commercial backing or sponsorship found.

**Production-ready claim:** Not made. Accurately described as functional with one-command install.

---

#### StraySpark Unreal MCP Server (Rep-Audit: PARTIALLY VERIFIED)

**Headline claim verification:** "359 tools across 50+ categories" (v3) — confirmed by official documentation at strayspark.studio/docs. v1 was 207/34 categories (March 2026 Epic Dev Community forum post), v2 was ~305/42 categories, v3 is 359/50+ (current). Active iteration confirmed.

**Key capabilities confirmed:**
- Blueprint: 51 tools — "Create, modify, and compile Blueprints entirely through AI"
- Sequencer: 12 tools
- Niagara VFX: 3 tools
- DataTable: 3 tools
- PIE control: 9 tools (write code → hit Play → observe → fix workflow)
- Source control: 8 tools (Perforce, Git LFS, Plastic, SVN)
- Auth: bearer-token + origin allow-list + Read/Scene/Destructive scope gates
- Transaction safety: every mutating action is a first-class UE editor transaction (undo-safe)
- Architecture: HTTP JSON-RPC 2.0 on port 13579; C++ plugin dispatches to game thread; pre-compiled binary (no compilation required)

**License:** Commercial (Fab.com). Individual/education free or reduced — not confirmed from publicly accessible source (Fab listing returned 403). Studio commercial use requires paid license. This is the single most significant adoption risk: cost unknown without purchase investigation.

**Production-ready claim:** The bearer-token auth, scope gating, undo transaction support, and multi-version iteration record are the strongest production-readiness signals in the ecosystem. No explicit "production-ready" language found in documentation, but the feature set is functionally production-oriented in a way no other implementation matches.

**SSH/remote topology:** HTTP port 13579 is SSH-forwardable by the same pattern as Remote Control HTTP (30010). No specific SSH documentation, but the architecture is compatible.

---

#### db-lyon/ue-mcp (Rep-Audit: PARTIALLY VERIFIED — License flagged)

**Headline claim verification:** "21 tools, 569+ actions" — confirmed from package.json (version 1.0.79; description field is verbatim "21 tools, 569+ actions"). The "21 categories" framing is the key characterization — 21 entry-point tools each covering many sub-actions. This is likely the source of "20+ connection types" mobile-Claude framing: 21 categories is close to "20+ connection types."

**License BUSL-1.1:** Business Source License 1.1 is NOT MIT/Apache-permissive. Free for individuals and education; commercial use (which includes studio game development) requires a commercial license. This is a significant adoption constraint. Price not publicly listed.

**Capabilities:** 21 categories covering Levels, Blueprints, Materials, Assets, Animation, VFX, Landscape, PCG, Gameplay, GAS, Networking, UI, Editor, Reflection, Project, StateTree, plus YAML flow engine for multi-step workflows. Broad coverage including Niagara (VFX category) and DataTable (Assets category) and Sequencer (implied in Animation category). Full confirmation of per-category tool depths not extracted.

---

#### remiphilippe/mcp-unreal (Rep-Audit: PARTIALLY VERIFIED — Updated)

Tool count is 49 (prior synthesis said 48; consistent). 22 categories confirmed. Key recount finding: **NO Sequencer tools** despite categories covering Build, Config, Tests, Actors/Properties, Blueprints, Animation BPs, Assets, Materials, Characters/Input, PCG, GAS, Niagara, Mesh Generation, Levels, Editor Utils, Components, Textures, DataTables, Fab Marketplace, Subsystems/UI, Network Debug, Documentation. DataTable tools present (1 tool: `data_asset_ops`). Niagara tools present (1 tool: `niagara_ops`). Blueprint editing present (2 tools: `blueprint_query`, `blueprint_modify`). Architecture confirmed: three communication layers (headless cmd, Remote Control HTTP, MCPUnreal plugin HTTP).

Stars: 47 (minimal growth from 46 in prior synthesis). Go 1.25+ requirement unchanged.

---

#### chongdashu/unreal-mcp (Rep-Audit: PARTIALLY VERIFIED — Updated)

Stars: 2,000 (unchanged from prior synthesis). Still explicitly "experimental — production use not recommended." Tool count revised downward from "15+" to approximately 16 distinct capabilities in 4 domains. Blueprint node graph CRUD confirmed as key differentiator (prior synthesis was accurate). UE 5.5+ confirmed. No Niagara, Sequencer, or DataTable coverage.

---

#### ChiR24/Unreal_mcp (Rep-Audit: PARTIALLY VERIFIED — Major update)

Prior synthesis characterized this with limited metadata. Current findings: 686 stars / 128 forks; 23 releases; v0.5.30 (2026-06-05); Docker Hub presence with 294 weekly pulls. Tool count is 35 (Docker image characterization) covering ~28 categories. UE 5.0-5.8 (5.8 preview) claimed — this is the broadest UE version range of any implementation. Dual transport (HTTP/SSE or WebSocket). The jump from near-zero metadata in prior synthesis to 686 stars and Docker publishing indicates significant community adoption growth. The 48-phase development roadmap suggests ambitious scope but also ongoing experimental status.

UE 5.8 preview support claim: not verified against .uplugin manifest. Flagged as unverified per Discipline #25.

---

### A.3 Section 2.3 Verification — The 20+-Connection-Type Claim

**Matt's mobile-Claude reference:** "a recently created universal extension for UE 5.7 that allowed 20+ MCP connection types with many actions within each type."

**Hypothesis evaluation:**

**Hypothesis A (most likely — already-identified, characterized differently):** Two prior-nucleus implementations match the "20+ categories with many actions per category" pattern:
- remiphilippe/mcp-unreal: 22 categories, 49 tools. If mobile-Claude used "connection types" to mean "tool categories," this matches exactly — 22 > 20, each with multiple actions.
- db-lyon/ue-mcp: 21 categories, 569+ actions. The 21-category/569-action structure is precisely "20+ connection types with many actions within each." db-lyon is also newer (v1.0.79 active as of 2026-06-06) and "universal" in scope. The "21 tools" in the package.json description, where each "tool" is a category, perfectly matches mobile-Claude's framing.

**Hypothesis B (possible — missed implementation):** No genuinely new implementation was found that specifically uses "connection types" as terminology or claims 20+ of them. The crawl covered 17 confirmed implementations plus a dozen minor forks. No uncatalogued implementation matching the description surfaced.

**Hypothesis C (partial — mobile-Claude reframing):** Mobile-Claude may have used "connection types" loosely to mean either "tool categories" or "communication layers" across multiple implementations. The characterization blends multiple real implementation features into a single description.

**Verdict:** **Hypothesis A is the most likely explanation.** The "20+ connection types" is almost certainly mobile-Claude's characterization of remiphilippe/mcp-unreal (22 categories) OR db-lyon/ue-mcp (21 categories). Both were already in the ecosystem at the time. No new implementation fitting the description was found that was missed by the prior synthesis. The "recently created" qualifier fits db-lyon (active development to v1.0.79 in June 2026) somewhat better than remiphilippe (stable at ~47 stars since the prior synthesis). db-lyon is the recommended specific candidate to investigate further if Matt wants to trace the exact mobile-Claude reference.

---

## Part B — Workstream-Lens Mapping

### B.1 WS1 — Data Layer Port (engine → UE)

| Workstream Need | Inventory Coverage (entries) | Quality Tier | Recommended Action |
|---|---|---|---|
| Batch asset import (mesh, texture, material from external JSON/filesystem) | NAJEMWEHBE (`import_mesh`, `bulk_move_assets`, Python exec); StraySpark (Asset category); GenOrca (Asset Management); gimmeDG (editor tools) | Partial | adopt NAJEMWEHBE + validate import toolchain |
| DataTable CRUD (engine kit-data → UE DataTable rows) | NAJEMWEHBE (`create_data_table`, `inspect_data_table`); remiphilippe (`data_asset_ops`); StraySpark (3 DataTable tools); db-lyon (Assets category) | Partial (CRUD = create+inspect; UPDATE/DELETE not confirmed) | extend — DataTable write/update tools need verification or addition |
| Asset Registry queries (resolve asset references; cross-asset dependency) | NAJEMWEHBE (Project/asset registry: 10 tools, `get_reference_chain`, `inspect_dependency_graph`); GenOrca (Asset Management); runreal (asset management); db-lyon | Full (NAJEMWEHBE best coverage) | adopt NAJEMWEHBE |
| Build configuration scripting (cook target switching) | remiphilippe (Build & Compile: 3 tools; Test Automation: 4 tools; Project & Config: 2 tools); StraySpark | Partial | adopt remiphilippe for build/cook ops specifically |
| Engine JSON ingestion (cosmograph-pivot JSON packet consumption) | NAJEMWEHBE (Python exec + synthetic bulk ops); StraySpark (Full asset pipeline) | Partial — Python exec tool enables ad-hoc ingestion; dedicated JSON-to-DataTable pipeline not present in any implementation | build custom tool wrapping Python exec |

**WS1 synthesis:** NAJEMWEHBE has the strongest WS1 coverage — asset registry, bulk asset ops, Python exec for custom ingestion, and DataTable creation. The gap is DataTable CRUD completeness (update/delete rows not confirmed). remiphilippe covers build/cook automation well but is weak on asset import. Recommended: NAJEMWEHBE as primary WS1 base; confirm DataTable write depth before committing.

---

### B.2 WS2 — Rendering Layer (Niagara VFX, Materials, Lighting)

| Workstream Need | Inventory Coverage | Quality Tier | Recommended Action |
|---|---|---|---|
| Niagara authoring (parameter iteration, emitter creation, module config) | NAJEMWEHBE (3 tools: spawn, attach, set_user_param); remiphilippe (1 tool: niagara_ops); StraySpark (3 tools); ChiR24 (effects category); db-lyon (VFX category) | Partial — parameter setting confirmed; emitter CREATION and module configuration unconfirmed across all implementations | extend — verify emitter creation capability or add |
| Material instance management (parameter set, parent swap, dynamic instance) | NAJEMWEHBE (Materials: 6 tools); GenOrca (Material System: 11 tools — strongest); StraySpark (MaterialGraph: 8 tools); db-lyon (Materials category); remiphilippe (1 tool) | Full — GenOrca has deepest material coverage (11 tools) | adopt GenOrca or NAJEMWEHBE for material ops |
| LOD setup (mesh LOD chain, material LOD, HLOD) | StraySpark (StaticMesh: 7 tools); ChiR24 (static mesh category) | Minimal — LOD config referenced but depth unconfirmed | verify or build |
| Lumen/Lighting config (sky light, reflection capture) | ChiR24 (lighting category); StraySpark (environment category) | Minimal — lighting tools present but Lumen-specific not confirmed | verify against implementation source |
| Per-skill VFX asset selection (Phase 6 coalescence output consumption) | NAJEMWEHBE (Python exec + bulk asset ops); StraySpark | Partial — requires custom Python script via Python exec tool | build via Python exec wrapper |

**WS2 synthesis:** Material management is well-covered (GenOrca strongest at 11 tools; NAJEMWEHBE solid at 6). Niagara coverage is present but thin across all implementations — parameter setting exists; emitter CREATION is the unverified gap. No implementation has confirmed deep LOD or Lumen-specific tooling. Recommended: NAJEMWEHBE for unified WS2 coverage; GenOrca is a supplementary reference for material depth patterns.

---

### B.3 WS3 — Materialization Cinematic

| Workstream Need | Inventory Coverage | Quality Tier | Recommended Action |
|---|---|---|---|
| Sequencer manipulation (track creation, keyframe authoring, camera animation) | NAJEMWEHBE (Level Sequences: 9 tools — `add_camera_cut_track`, `add_audio_track`, `add_visibility_track`, `render_sequence_mrq`); StraySpark (Sequencer: 12 tools); UnrealMotionGraphicsMCP (Sequencer API: 10 tools — specialized); db-lyon (Animation category) | Partial (NAJEMWEHBE: 9 tools; transform keyframe confirmed via synthetic tool `sequencer_add_transform_keyframe`; StraySpark deepest at 12 tools) | adopt NAJEMWEHBE; StraySpark if commercial viable |
| Camera animation (CineCamera Actor, FOV/focus animation) | NAJEMWEHBE (Camera: 3 tools + `batch_capture_cameras`); StraySpark; UnrealMotionGraphicsMCP | Partial | adopt NAJEMWEHBE |
| Audio cueing (Sound Cue trigger) | NAJEMWEHBE (Audio: 3 tools, `inspect_sound_class`, `inspect_sound_submix`, `inspect_audio_bus`); StraySpark (Audio + MetaSound: 6 tools) | Partial — inspection confirmed; trigger/playback control not confirmed | verify playback control tools |
| Materialization-cinematic trigger logic | NAJEMWEHBE (Blueprint + actor ops + event push/subscriptions: 5 tools); StraySpark (Blueprint: 51 tools) | Partial | adopt NAJEMWEHBE; StraySpark for deeper Blueprint event control |

**WS3 synthesis:** This is the most demanding workstream for Sequencer automation. NAJEMWEHBE has meaningful coverage (9 Sequencer tools including camera cut track and transform keyframe), but StraySpark has the deepest Sequencer toolset at 12 tools. UnrealMotionGraphicsMCP is a specialized option with 10 Sequencer tools and deep UMG integration but is UE 5.6+ only and experimental. The materialization cinematic relies heavily on Sequencer + Blueprint triggers — if NAJEMWEHBE's 9 Sequencer tools don't cover all the required track types, extension work is needed. remiphilippe has NO Sequencer tools — confirmed gap.

---

### B.4 WS4 — Continuity / Save-Load

| Workstream Need | Inventory Coverage | Quality Tier | Recommended Action |
|---|---|---|---|
| Save game systems (SaveGame class, programmatic save/load) | StraySpark (Editor category — auto-save is a feature); NAJEMWEHBE (Editor state/undo: 2 tools) | Minimal — save/load as MCP ops not confirmed in any implementation; editor auto-save present | build — this is runtime game system, not editor automation; MCP not the right tool |
| Asset persistence (runtime serialization) | Not covered by any implementation | Absent | defer — runtime game system, not editor automation scope |

**WS4 synthesis:** WS4 is the least MCP-relevant workstream. SaveGame system is a runtime game system implemented in C++ or Blueprint, not an editor automation concern. MCP tooling is editor-time automation; save-load is runtime behavior. Recommendation: WS4 does NOT benefit materially from MCP investment. Exclude from MCP bridge spike scope. Human-driven UE implementation is appropriate.

---

### B.5 WS5 — Mobile Polish

| Workstream Need | Inventory Coverage | Quality Tier | Recommended Action |
|---|---|---|---|
| Mobile preview launch (mobile PIE, Android/iOS specific) | StraySpark (PIE: 9 tools including Play control and screenshot capture); ChiR24 (session tools) | Partial — PIE control confirmed in StraySpark; mobile-specific preview not confirmed | verify StraySpark PIE includes mobile platform selection |
| Platform-specific build settings (per-platform .ini overrides, device profiles) | remiphilippe (Project & Config: 2 tools); db-lyon (Project category) | Minimal | build or defer |
| Perf profiling triggers (Insights/Trace start/stop, stat capture) | StraySpark (performance category); NAJEMWEHBE (`bulk_set_console_variables` for stat commands); ChiR24 (performance category) | Minimal | build via console variable tool |

**WS5 synthesis:** Mobile PIE control has partial coverage in StraySpark (9 PIE tools). Platform-specific build settings are minimally covered. Perf profiling can be approximated via console variable tools. WS5 MCP automation is not a primary driver of spike investment — most mobile polish is iterative manual work. Recommended: Low priority for MCP bridge spike scope; defer WS5 MCP tooling until WS1-WS3 coverage is proven.

---

### B.6 General Iteration + Gameplay Code Authoring

| Workstream Need | Inventory Coverage | Quality Tier | Recommended Action |
|---|---|---|---|
| PIE start/stop/pause control | StraySpark (PIE: 9 tools — strongest; write code → Play → observe → fix loop); ChiR24 (session control); NAJEMWEHBE (`execute_console_command` for PIE cmds) | Full (StraySpark); Partial (others) | adopt StraySpark if commercial; NAJEMWEHBE console tool as fallback |
| Log file tailing (Output Log capture) | NAJEMWEHBE (Console/logs: 5 tools including Output Log capture); remiphilippe (via console commands) | Full (NAJEMWEHBE) | adopt NAJEMWEHBE |
| Hot-reload (Live Coding, Blueprint reinstancing) | remiphilippe (Build & Compile: 3 tools); StraySpark; NAJEMWEHBE (via compile tools) | Partial — compile trigger confirmed; Blueprint reinstancing confirmation unclear | verify |
| Breakpoint manipulation | None confirmed in any open-source implementation; StraySpark roadmap item (unconfirmed) | Absent | build or defer |
| **Blueprint editing (node graph CRUD, variable management, event binding)** | **chongdashu** (Blueprint node graph: full CRUD confirmed, best-in-class for open-source); **NAJEMWEHBE** (Blueprint/widget/animation: 20 tools); **StraySpark** (Blueprint: 51 tools — deepest); **lilklon/UEBlueprintMCP** (Blueprint-specialized, 60+ tools); **GenOrca** (Blueprint Graph: 16 tools); **gimmeDG** (Blueprint: 47 tools) | **Full** — multiple implementations; StraySpark deepest; chongdashu most battle-tested for node graph CRUD | adopt NAJEMWEHBE (unified); extend with chongdashu's node graph patterns if gaps |

**General iteration synthesis:** PIE control and log tailing have meaningful coverage. Blueprint editing is the strongest-covered capability across the entire ecosystem — multiple implementations, ranging from 16 to 51 tools. Breakpoint manipulation is absent across all implementations; this is a genuine gap.

---

### B.7 Blueprint Editing Scope-In / Scope-Out Revisit

**Prior commission recommendation:** Blueprint editing SCOPED OUT for creation-moment spike.

**Workstream-spanning reassessment:**

Blueprint editing is load-bearing across WS1-WS5:
- WS1: DataTable injection via Blueprint batch scripts
- WS2: Material instance Blueprint functions
- WS3: Materialization-cinematic trigger Blueprint (lasso input handler, ingredient drag-drop, tablet drawing handler per Earth-Avatar canonical § 2.3 + § 2.5)
- WS5: Mobile input handler Blueprints (touch, tablet)
- General iteration: gameplay logic across all workstreams

The prior commission's scope-out was appropriate for the narrow creation-moment vertical slice. At workstream-spanning scope, Blueprint editing MCP automation is load-bearing — not for complex node-graph surgery (which likely remains human-driven), but for:
1. **Property-level editing** (setting Blueprint variables, component properties, event dispatcher connections) — this is automatable and covered by NAJEMWEHBE/StraySpark
2. **Blueprint compilation** (trigger compile after property changes) — confirmed in NAJEMWEHBE, StraySpark, chongdashu
3. **Blueprint introspection** (inspect current node graph, find variable references) — confirmed in NAJEMWEHBE, chongdashu

**Revised verdict:** Blueprint editing should be **SCOPED IN** at the property/compile/inspect level for the workstream-spanning MCP bridge. Complex node-graph CRUD (creating new function graphs, wiring complex event chains from scratch) should remain **human-driven**. The demarcation: "read and configure existing Blueprint structure via MCP; build new Blueprint logic by hand."

This is a partial reversal of the prior commission's scope-out — not a full reversal. NAJEMWEHBE has sufficient Blueprint tooling for the property/compile/inspect tier without requiring chongdashu's full node-graph CRUD surface.

---

## Part C — Design-Decision Feedstock

### C.1 Build-vs-Adopt-vs-Extend Posture

**Recommended verdict: ADOPT-AND-EXTEND (open-source path) or ADOPT-OUTRIGHT (commercial path)**

**Open-source path — ADOPT-AND-EXTEND with NAJEMWEHBE as base:**

NAJEMWEHBE/unreal-ai-connection is the strongest open-source adoption candidate:
- MIT license — no restrictions
- UE 5.7.4 primary target — exact match with our platform
- 147 tools across 15 categories — broadest open-source coverage
- 607 tests + CI + smoke test discipline — highest engineering rigor in open-source field
- Covers WS1 (asset registry, bulk asset ops, DataTable), WS2 (materials, Niagara), WS3 (Sequencer 9 tools, camera, audio), WS6 (Blueprint introspection, log tailing, Python exec)
- Low star count (6) is a risk; mitigated by recent active development (v0.9.1 May 2026) and strong internal engineering discipline

**Gaps to extend:**
- DataTable CRUD completeness (update/delete row operations — 2 confirmed tools may not cover all needed patterns)
- Sequencer depth for WS3 (9 tools may need extension for complex materialization-cinematic track types)
- SSH/remote topology validation (no documented SSH use case; architecture is compatible but untested)
- PIE control tools (NAJEMWEHBE has console command approach; dedicated PIE start/stop tools from StraySpark/ChiR24 pattern may be cleaner)

**Alternative open-source references for extension:**
- chongdashu: node-graph CRUD patterns for Blueprint extension
- remiphilippe: Remote Control HTTP wrapping pattern; Go binary architecture as reference
- UnrealMotionGraphicsMCP: Sequencer track patterns for WS3 depth extension

**Commercial path — ADOPT-OUTRIGHT with StraySpark:**

StraySpark is the only implementation with:
- Production-grade auth (bearer-token + scope gating)
- Transaction safety (undo-safe mutations)
- PIE control (write → play → observe loop)
- Deep coverage across all workstreams (51 Blueprint, 12 Sequencer, 3 DataTable, 3 Niagara)
- Pre-compiled binary (zero C++ compilation for David-H)
- UE 5.7 Win64/Mac/Linux
- Active commercial development (v3 current; v4 roadmap visible)

**Commercial path blocker:** Price unknown (Fab listing 403); studio commercial license terms unknown. If StraySpark's commercial license is affordable (< several hundred USD), the avoided build cost likely justifies adoption outright. If pricing is enterprise-level, the open-source path with NAJEMWEHBE extension is the right call.

**This decision point requires gandalf escalation** — see C.5.

**Why REFERENCE+BUILD (prior verdict) is REVISED:**

The prior synthesis recommended REFERENCE+BUILD because no single implementation matched the remote-SSH mantis topology. This remains true — no implementation was built for SSH-mediated remote editor control. However, NAJEMWEHBE's architecture (C++ plugin binding localhost:18888 + Python bridge) is SSH-forwardable by construction, and its tool coverage now materially covers WS1-WS3. The extend cost is lower than the build-from-scratch cost. REFERENCE+BUILD was the correct verdict at creation-moment scope; ADOPT-AND-EXTEND is the correct verdict at workstream-spanning scope.

---

### C.2 MCP Bridge Spike Scope Implications

**Current spike commission:** Remote Control HTTP MVP for creation moment.

**Revised scope recommendations:**

1. **Evaluate NAJEMWEHBE in addition to (or instead of) Remote Control HTTP from scratch.** The spike's primary question should become: "Can we adapt NAJEMWEHBE's architecture for SSH-remote topology?" rather than "Can we build a Remote Control HTTP wrapper?" The answer to the former is likely yes with less work.

2. **SSH port-forwarding validation remains the first milestone** — unchanged from prior synthesis. Forward port 18888 (NAJEMWEHBE) and/or 30010 (Remote Control HTTP) through the SSH connection; verify connectivity before any tool implementation work.

3. **Evaluate StraySpark as a parallel spike track** if price is accessible. StraySpark's pre-compiled binary + HTTP JSON-RPC on port 13579 is SSH-forwardable and requires no C++ build. If StraySpark's license is affordable, the spike becomes: install StraySpark plugin on Matt's PC → David-H SSH-forwards port 13579 → mantis calls StraySpark tools via MCP client → verify tool coverage against WS1-WS3 needs. This could reduce spike effort by 80%.

4. **Architecture decision: C++ TCP plugin (NAJEMWEHBE pattern) vs Remote Control HTTP (remiphilippe pattern) vs pre-built binary (StraySpark pattern).** The spike should test at least two of these paths:
   - Path A: NAJEMWEHBE adoption (install MIT plugin, port-forward 18888, validate SSH connectivity, test WS1-WS3 tools)
   - Path B: StraySpark evaluation (if price is accessible; test pre-compiled binary, port-forward 13579, validate WS1-WS3 tools)
   - Path C (original): Remote Control HTTP wrapper from scratch (build; test)
   Path A and B are both lower effort than Path C. Spike should attempt A first.

5. **Remove "from scratch" presumption.** The MCP bridge spike commission should be amended to replace "Remote Control HTTP MVP" with "MCP bridge MVP via best-fit existing implementation (NAJEMWEHBE primary candidate; StraySpark if commercial viable)."

---

### C.3 Blueprint Editing Scope-In / Scope-Out Revisit

**Prior recommendation:** Scope OUT (creation-moment scope).

**Revised recommendation:** PARTIAL SCOPE-IN at property/compile/inspect tier; node-graph CRUD remains human-driven.

**Evidence:** Blueprint editing is confirmed across 6+ implementations with varying depth. The ecosystem has reached sufficient maturity that Blueprint property inspection, compilation triggering, and variable reading via MCP are reliable operations. NAJEMWEHBE covers this tier within its 20-tool Blueprint/widget/animation category. StraySpark covers it across 51 Blueprint tools.

**Practical scope for spike:** The spike should include:
- `inspect_blueprint` — read current Blueprint variable values and component list (needed for debug/verify workflows)
- `compile_blueprint` — trigger compilation after human-authored node edits (needed for iteration loop)
- `set_blueprint_property` / `bulk_set_actor_property` — set exposed Blueprint properties from MCP (needed for lasso input handler configuration, ingredient drag-drop parameters)

**Out of scope for spike (remains human-driven):**
- Creating new function graphs
- Wiring complex event chains from scratch
- Blueprint node graph construction for novel gameplay logic

This scope is achievable within NAJEMWEHBE's confirmed tool surface without extension work.

---

### C.4 Productionization Viability

**Open-source path (NAJEMWEHBE-based):**
- License: MIT — no commercial restrictions
- Maintainer activity: Active (v0.9.1 May 2026); recent commits; CI running
- Maintainer risk: Single maintainer (HD Media, Kuwait); low star count = small community safety net; if maintainer goes quiet, adoption owner (David-H) inherits maintenance burden
- Auth/security posture: No application-layer auth; localhost binding; SSH tunnel provides transport security — appropriate for our topology
- Test coverage: 607 tests + CI — best in open-source field; extension work can follow the established test discipline
- 6-12 month viability: Moderate confidence — active development trajectory is positive, but community size is a risk

**Commercial path (StraySpark):**
- License: Commercial (requires purchase; studio license) — cost TBD
- Maintainer activity: Strong commercial trajectory (v1 → v2 → v3 in ~3 months; Epic Dev Community presence; active forum thread)
- Auth/security posture: Bearer-token + scope gating — production-grade by design; appropriate for production
- Test coverage: Not published — opaque
- 6-12 month viability: High confidence as commercial product with Fab.com distribution and paying customers

**Recommendation:** For a spike, NAJEMWEHBE is the right path (no cost, MIT, evaluate risk before committing to commercial). For production (if MCP bridge becomes keeper tooling), StraySpark's commercial offering is worth the cost investigation given its superior production-safety features.

---

### C.5 Open Questions for Gandalf Review

1. **StraySpark pricing and studio-license acceptability.** StraySpark is the only implementation with production-grade auth, transaction safety, and PIE control — but requires a commercial Fab.com license. If gandalf/Matt can determine the price is acceptable for studio use, the recommended posture shifts from ADOPT-AND-EXTEND (NAJEMWEHBE) to ADOPT-OUTRIGHT (StraySpark). This decision gates the spike architecture. **Recommended action:** Check StraySpark pricing at fab.com/listings/aa699a85-04b1-4746-a29c-962fc3a78f55 and determine if the commercial license is acceptable.

2. **db-lyon/ue-mcp commercial license applicability.** db-lyon uses BUSL-1.1. If we adopt db-lyon as our MCP bridge, we require a commercial license for studio game development. This may or may not be acceptable depending on price. db-lyon has the strongest coverage breadth (21 categories, 569+ actions) at a lower engineering maturity than StraySpark. **Gandalf decides:** is the BUSL-1.1 license acceptable, or should db-lyon be restricted to reference only?

3. **NAJEMWEHBE single-maintainer risk tolerance.** NAJEMWEHBE is the strongest open-source option but has one maintainer and 6 stars. If we adopt it as our base and the maintainer goes quiet, David-H inherits the maintenance burden. **Gandalf/Matt decides:** is a one-person-maintained MIT project an acceptable foundation for keeper tooling, or does the commercial path (StraySpark) better serve the project's risk tolerance?

4. **MCP bridge spike re-scoping authority.** The current spike commission (2026-06-07-david-h-ue-remote-control-mcp-bridge-spike.md) was scoped as "Remote Control HTTP MVP for creation moment." This research recommends pivoting to NAJEMWEHBE evaluation as the spike's primary path. **Gandalf/knight-rider decides:** re-scope the spike commission to reflect ADOPT-AND-EXTEND posture, or commission a new spike-evaluation dispatch that David-H executes as a parallel track.

5. **WS4 MCP scope exclusion.** This research finds WS4 (continuity/save-load) has no meaningful MCP coverage in any implementation because it is a runtime game concern, not an editor automation concern. **Gandalf confirms or corrects:** is WS4 correctly excluded from MCP bridge scope?

6. **Sequencer depth for WS3.** NAJEMWEHBE has 9 Sequencer tools; StraySpark has 12. The materialization-cinematic may require specific track types (SubObjectProperty animation, Material Parameter Collection tracks, Blueprint-driven spawn/destroy events) that are not confirmed in NAJEMWEHBE's 9-tool set. **Gandalf or mantis verifies:** do NAJEMWEHBE's `add_camera_cut_track`, `add_audio_track`, `add_visibility_track`, `render_sequence_mrq` (+ 5 others unnamed) cover the materialization-cinematic's required track types, or is Sequencer tooling an extension priority?

---

## Source List

- chongdashu/unreal-mcp: https://github.com/chongdashu/unreal-mcp
- remiphilippe/mcp-unreal: https://github.com/remiphilippe/mcp-unreal
- NAJEMWEHBE/unreal-ai-connection: https://github.com/NAJEMWEHBE/unreal-ai-connection
- ChiR24/Unreal_mcp: https://github.com/ChiR24/Unreal_mcp
- ChiR24 Docker Hub: https://hub.docker.com/r/mcp/unreal-engine-mcp-server
- GenOrca/unreal-mcp: https://github.com/GenOrca/unreal-mcp
- mirno-ehf/ue5-mcp: https://github.com/mirno-ehf/ue5-mcp
- Natfii/ue5-mcp-bridge: https://github.com/Natfii/ue5-mcp-bridge
- db-lyon/ue-mcp: https://github.com/db-lyon/ue-mcp (docs: https://db-lyon.github.io/ue-mcp/)
- flopperam/unreal-engine-mcp: https://github.com/flopperam/unreal-engine-mcp
- runreal/unreal-mcp: https://github.com/runreal/unreal-mcp
- lilklon/UEBlueprintMCP: https://github.com/lilklon/UEBlueprintMCP
- gimmeDG/UnrealEngine5-mcp: https://github.com/gimmeDG/UnrealEngine5-mcp
- StraySpark Unreal MCP Server (commercial): https://www.strayspark.studio/docs/unreal-mcp-server
- StraySpark Epic Dev Community forum: https://forums.unrealengine.com/t/strayspark-unreal-mcp-server-200-ai-tools-for-ue5-editor-automation-via-mcp/2707474
- winyunq/UnrealMotionGraphicsMCP: https://github.com/winyunq/UnrealMotionGraphicsMCP
- LOOMLE: https://mcpservers.org/servers/loomle/loomle
- mcpservers.org UE listings: https://mcpservers.org/ (searches conducted 2026-06-08)
- mcp.so UE5 tag: https://mcp.so/tag/unreal-engine-5
- Official MCP Registry: https://registry.modelcontextprotocol.io/ (no UE entries confirmed in visible registry)
- PulseMCP — mirno-ehf/ue5-mcp: https://www.pulsemcp.com/servers/mirno-ehf-ue5-blueprint
- Glama.ai — NAJEMWEHBE: https://glama.ai/mcp/servers/NAJEMWEHBE/unreal-ai-connection
- StraySpark 2026 guide: https://www.strayspark.studio/blog/mcp-server-game-development-complete-guide-2026
- Prior synthesis (nucleus): agentic_orchestration/legolas/research/2026-06-07-ue-mcp-prior-art/synthesis.md

---

## Knowledge Gaps Not Resolved

1. **StraySpark pricing.** Fab.com listing returned 403. Price and studio-commercial-license terms unknown. This is the single most critical unresolved item — it gates the ADOPT-OUTRIGHT vs ADOPT-AND-EXTEND decision.

2. **NAJEMWEHBE C++ handler count discrepancy.** README claims 110 C++ handlers; per-category sum resolves to 103. The 7-tool discrepancy may be undocumented categories or documentation lag. Not fabrication — but exact tool count is 140-147 range rather than a confirmed 147.

3. **SSH topology validation for any implementation.** No community examples of SSH-mediated remote MCP use found. Architecture is compatible for all localhost-binding implementations (NAJEMWEHBE on 18888; StraySpark on 13579; Remote Control HTTP on 30010) but untested. Spike must validate this as first milestone.

4. **db-lyon/ue-mcp commercial license cost.** BUSL-1.1 commercial license terms and pricing not found in public documentation.

5. **LOOMLE tool count and UE version.** LOOMLE (MIT, Blueprint/PCG/Material focused) has insufficient public documentation to confirm tool count and UE version support. Relevant for WS2 (PCG + Material) but metadata insufficient for Part A characterization.

6. **ChiR24 UE 5.8 claim.** .uplugin manifest not verified. UE 5.8 preview support is unverified. The broadest version range claim (5.0-5.8) is likely aspirational or based on API compatibility inference, not tested compilation.

7. **Sequencer track type coverage in NAJEMWEHBE.** The 9 Level Sequence tools are named but 5 of 9 are confirmed by name; the remaining 4 are uncharacterized. Critical for WS3 scope confirmation.

---

## Sign-off

**Legolas** — Mode A analytical research (Pattern A-deep)
**Delivered:** 2026-06-08
**Commission:** `agentic_orchestration/dispatches/2026-06-08-legolas-ue-mcp-workstream-spanning-prior-art.md`
**Output path:** `agentic_orchestration/legolas/research/2026-06-08-mcp-workstream-spanning-prior-art/synthesis.md`
**Verdict:** ADOPT-AND-EXTEND (NAJEMWEHBE as open-source base) — or ADOPT-OUTRIGHT (StraySpark commercial) if pricing is acceptable
**Extends:** `agentic_orchestration/legolas/research/2026-06-07-ue-mcp-prior-art/synthesis.md` (prior REFERENCE+BUILD verdict revised upward at workstream-spanning scope)
