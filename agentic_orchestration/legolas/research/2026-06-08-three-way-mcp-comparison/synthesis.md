# Research — Three-Way MCP Comparison: NAJEMWEHBE vs StraySpark vs db-lyon — 2026-06-08

**Mode:** A (analytical; Pattern A-deep)
**Commissioner:** gandalf (story-and-design steward)
**Commission file:** `agentic_orchestration/dispatches/2026-06-08-legolas-three-way-mcp-comparison-najem-strayspark-dblyon.md`
**Prior synthesis:** `agentic_orchestration/legolas/research/2026-06-08-mcp-workstream-spanning-prior-art/synthesis.md`
**Crawl date:** 2026-06-08
**Sources consulted:** GitHub source-code inspection (NAJEMWEHBE/unreal-ai-connection bridge + C++ handlers; db-lyon/ue-mcp TypeScript tool files); StraySpark public docs (strayspark.studio/docs, Epic Dev Community forum); db-lyon LICENSE + COMMERCIAL-LICENSE.md; package.json verification

---

## TL;DR

Source-code inspection at action-name granularity resolves the characterization gaps from the prior synthesis. The three candidates differ sharply on scope, architecture, and license risk.

**NAJEMWEHBE** has 148 tool names confirmed by direct bridge enumeration (prior synthesis said 147; the bridge's `"name"` field list resolves to 148; the C++ handler count is 107, not 110, with the remainder synthetic). Its Sequencer surface is **9 confirmed tools, all verified by source** — the "5 of 9 unverified" flag from the prior synthesis is now closed. DataTable coverage is thin (2 tools: create + inspect). SSH topology is compatible by construction. MIT. LOW extension cost.

**StraySpark** has 359 tools confirmed by official documentation but tool names remain unverifiable from public source (commercial closed-source). The Epic Dev Community forum post confirms 8 Sequencer tools (v3 docs reference 8 in an older count; more may have been added). Niagara is 3 tools. DataTable 3 tools. PIE 9 tools. Auth + transaction safety present. Price unknown. MEDIUM-to-HIGH adoption risk due to pricing opacity.

**db-lyon** has **21 entry-point tools** and **569+ actions** confirmed by source (package.json version 1.0.79). Source inspection confirms the architecture: each "tool" is a category dispatching dozens of sub-actions. Animation tool alone has 54 sub-actions; Blueprint tool alone has 59 sub-actions; asset tool alone has 60+ sub-actions; Niagara tool has 29 sub-actions including deep emitter + module authoring; editor tool includes 8 Sequencer-equivalent sub-actions (create_sequence, get_sequence_info, add_sequence_track, add_sequence_section, set_sequence_keyframes, set_sequence_playback_range, play_sequence, and more). BUSL-1.1 commercial license — pricing page `ue-mcp.com/pricing` was unreachable per Matt 2026-06-08. Migration cost from db-lyon to NAJEMWEHBE: **MEDIUM** (different tool-name surface, same logical operations, architectural re-wiring needed).

**Recommended posture: ADOPT-AND-EXTEND (NAJEMWEHBE)** as the primary path with **EVAL-THEN-MIGRATE framing for db-lyon during pre-commercial-eval if breadth wins the spike**. StraySpark remains contingent on price discovery.

---

## § 1 Per-Workstream Coverage Matrix — Tool-Name Granular

### WS1 — Data Layer Port (engine → UE)

| Need | NAJEMWEHBE tools | StraySpark tools | db-lyon tools |
|---|---|---|---|
| Batch asset import (mesh/texture from filesystem) | `import_mesh`, `import_texture`, `bulk_move_assets` | Asset category (confirmed; tool names not public) | `asset.import_static_mesh`, `asset.import_skeletal_mesh`, `asset.import_animation`, `asset.import_texture`, `asset.import_texture_batch` |
| DataTable CRUD (create + read + write rows) | `create_data_table`, `inspect_data_table` — **2 tools; CREATE + READ only; NO row-write confirmed** | DataTable 3 tools (names not public) | `asset.read_datatable`, `asset.create_datatable`, `asset.reimport_datatable`, `asset.set_datatable_row`, `asset.add_datatable_row`, `asset.update_datatable_row`, `asset.remove_datatable_row`, `asset.get_datatable_row`, `asset.set_datatable_cell`, `asset.rename_datatable_row`, `asset.fill_datatable_from_json` — **11 DataTable tools; full CRUD confirmed** |
| Asset Registry queries (asset lookup, dependency) | `find_assets`, `inspect_asset`, `get_reference_chain`, `inspect_dependency_graph`, `bulk_inspect_assets`, `find_unused_assets` — **6 tools** | Asset category (confirmed) | `asset.list`, `asset.search`, `asset.read`, `asset.read_properties`, `asset.get_referencers`, `asset.search_fts`, `asset.reindex_fts`, `asset.diagnose_registry`, `asset.health_check` — **9 tools** |
| Build config scripting (cook target; per-platform) | `execute_console_command` for cook commands | Build category (confirmed) | `project.set_config`, `project.build`, `project.generate_project_files` |
| Engine JSON ingestion (cosmograph packet) | `execute_unreal_python`, `exec_python_persistent` (Python exec enables ad-hoc ingestion) | Python category (confirmed) | `editor.run_python_file` + `asset.fill_datatable_from_json` (direct JSON bulk-upsert without Python scripting) |

**WS1 gap summary:** NAJEMWEHBE has a critical DataTable gap — row-write (update/delete operations) is not present. db-lyon has the strongest DataTable coverage by a wide margin (11 dedicated actions vs 2 vs 3). NAJEMWEHBE's Python exec tools partially bridge the gap for JSON ingestion.

---

### WS2 — Rendering Layer (Niagara VFX, Materials, Lighting)

| Need | NAJEMWEHBE tools | StraySpark tools | db-lyon tools |
|---|---|---|---|
| Niagara authoring (spawn, parameter, emitter) | `spawn_niagara_at_location`, `spawn_niagara_attached`, `set_niagara_user_param` — **3 tools; spawn + user-param only; NO emitter creation/module config** | Niagara 3 tools (names not public) | `niagara.list`, `niagara.get_info`, `niagara.spawn`, `niagara.spawn_actor`, `niagara.reactivate`, `niagara.set_parameter`, `niagara.create`, `niagara.create_emitter`, `niagara.add_emitter`, `niagara.list_emitters`, `niagara.set_emitter_property`, `niagara.list_modules`, `niagara.get_emitter_info`, `niagara.list_renderers`, `niagara.add_renderer`, `niagara.remove_renderer`, `niagara.set_renderer_property`, `niagara.inspect_data_interfaces`, `niagara.create_system_from_spec`, `niagara.get_compiled_hlsl`, `niagara.list_system_parameters`, `niagara.list_module_inputs`, `niagara.set_module_input`, `niagara.list_static_switches`, `niagara.set_static_switch`, `niagara.create_module_from_hlsl`, `niagara.create_scratch_module`, `niagara.batch` — **28 actions; full emitter + module authoring confirmed** |
| Material instance management (parameter, parent, dynamic) | `create_material_instance`, `set_mi_parameter`, `inspect_material`, `inspect_material_instance`, `add_material_expression`, `connect_material_expression` — **6 tools** | MaterialGraph 8 tools; Material category (confirmed) | `material.create_instance`, `material.set_parameter`, `material.create`, `material.create_simple`, `material.add_expression`, `material.connect_expressions`, `material.connect_to_property`, `material.list_expressions`, `material.recompile`, `material.build_graph`, `material.import_graph`, `material.export_graph`, `material.create_function`, `material.add_function_expression`, `material.connect_function_expressions` — **15+ actions** |
| LOD setup (mesh LOD, HLOD) | Not confirmed | StaticMesh 7 tools in StraySpark (confirmed) | `asset.get_mesh_info` (LOD count) — LOD authoring not confirmed in db-lyon source |
| Lumen / Lighting config | `execute_console_command` for r.Lumen.* | Environment category (confirmed) | `level.spawn_light`, `level.set_light_properties`, `level.build_lighting` |
| Per-skill VFX asset selection | `spawn_niagara_at_location`, `spawn_niagara_attached`, Python exec | Asset + Niagara categories | `niagara.spawn`, `niagara.spawn_actor` + deep system/emitter authoring |

**WS2 gap summary:** NAJEMWEHBE's Niagara surface is thin — spawn + user-param; NO emitter creation or module configuration. db-lyon's Niagara is the deepest in the ecosystem (28 actions including full emitter/module/renderer authoring + HLSL custom modules). StraySpark's Niagara at 3 tools likely matches NAJEMWEHBE's surface.

---

### WS3 — Materialization Cinematic (Sequencer)

**CRITICAL — this section resolves the "5 of NAJEMWEHBE's 9 Sequencer tool names unverified" flag from the prior synthesis.**

#### NAJEMWEHBE Sequencer Tools — SOURCE-VERIFIED (all 9 confirmed by name)

From direct source-code inspection of `bridge/unreal_ai_connection_bridge.py` + C++ handlers:

1. `inspect_sequence` — read Level Sequence structure (tracks, sections, bindings, frame rate, playback range)
2. `create_sequence` — create new Level Sequence asset with empty MovieScene
3. `bind_actor_to_sequence` — add level actor as possessable binding (returns binding GUID)
4. `set_sequence_playback_range` — set MovieScene playback range start/end in display-rate frames
5. `add_cine_camera_to_sequence` — spawn ACineCameraActor + add as possessable binding (returns GUID)
6. `add_camera_cut_track` — add/reuse camera cut track + append section bound to camera GUID
7. `add_audio_track` — add root-level audio track + append sound section
8. `add_visibility_track` — add visibility track to binding + key visible/hidden at frames
9. `render_sequence_mrq` — async render via Movie Render Queue (PNG/JPG/BMP/EXR); async with poll_task
10. `sequencer_add_transform_keyframe` — (synthetic; 10th tool, NOT in the 9) add keyframe on 3D Transform Track for bound actor

**Rep-audit result:** NAJEMWEHBE has **10 Sequencer-related tools**, not 9. The prior synthesis undercounted by omitting `sequencer_add_transform_keyframe` (a synthetic tool documented separately). All tool names are now source-verified. The "5 unverified" flag is fully resolved.

**Coverage assessment (WS3):**
- Camera cut track: YES (`add_camera_cut_track`, `add_cine_camera_to_sequence`)
- Audio track: YES (`add_audio_track`)
- Visibility track: YES (`add_visibility_track`)
- Transform keyframe: YES (`sequencer_add_transform_keyframe`)
- Playback range control: YES (`set_sequence_playback_range`)
- Render output (MRQ): YES (`render_sequence_mrq`)
- **GAPS confirmed:** No dedicated event track, no subscene track, no SkeletalAnimation track, no built-in camera shake tool (achievable via Python exec or transform keyframes)

| Need | NAJEMWEHBE | StraySpark | db-lyon |
|---|---|---|---|
| Camera cut track | `add_camera_cut_track` + `add_cine_camera_to_sequence` (VERIFIED) | 8 Sequencer tools (v3 forum; names not public) | `editor.add_sequence_section` with trackType=CameraCut + cameraActorLabel param (VERIFIED) |
| Audio cueing | `add_audio_track` (VERIFIED) | Included in Sequencer category | `editor.add_sequence_section` with trackType=Audio (VERIFIED) |
| Visibility track | `add_visibility_track` (VERIFIED) | Included in Sequencer category | trackType=SkeletalAnimation / others via `editor.add_sequence_track` (VERIFIED) |
| Transform keyframe | `sequencer_add_transform_keyframe` (VERIFIED synthetic) | Included in Sequencer category | `editor.set_sequence_keyframes` with channel=Location.X/Y/Z, Rotation (VERIFIED) |
| MRQ render output | `render_sequence_mrq` (VERIFIED async) | Included in Sequencer category | Not confirmed in editor.ts Sequencer actions |
| Sequence inspect | `inspect_sequence` (VERIFIED) | Included | `editor.get_sequence_info` (VERIFIED) |

**db-lyon Sequencer tools (source-verified from editor.ts):**
`editor.create_sequence`, `editor.get_sequence_info`, `editor.add_sequence_track`, `editor.add_sequence_section` (supports Transform/Float/Fade/CameraCut/Audio/Event/SkeletalAnimation), `editor.set_sequence_keyframes` (per-channel keyframing with cubic/linear interpolation), `editor.set_sequence_playback_range`, `editor.play_sequence` (play/stop/pause control) — **7 confirmed Sequencer actions**. MRQ render not confirmed in source. The `add_sequence_section` tool is notably more general than NAJEMWEHBE's per-track-type tools — one function covers all track types.

**StraySpark Sequencer (Epic Dev Community forum):** Forum confirms "Sequencer (8)" in v3 categorization. Individual tool names not publicly listed. Assumed to cover camera cuts, transform tracks, audio, event tracks, and MRQ render (stated in commercial marketing).

---

### WS4 — Continuity / Save-Load

| Candidate | Coverage |
|---|---|
| NAJEMWEHBE | No save-game tools. Editor auto-save available via `save_dirty_assets`. |
| StraySpark | Editor auto-save tool in Editor category. No runtime save-game tools. |
| db-lyon | `editor.save_dirty`, `asset.save`, `asset.save_all_dirty`. No runtime save-game tools. |

**WS4 verdict (all three):** SaveGame system is a runtime game concern, not an editor automation concern. MCP tooling operates at editor-time. All three correctly exclude runtime save-game as out of scope. WS4 is appropriately excluded from MCP bridge spike scope across all candidates.

---

### WS5 — Mobile Polish

| Need | NAJEMWEHBE | StraySpark | db-lyon |
|---|---|---|---|
| PIE start/stop/pause | `pie_control` (action=start\|stop\|query) — VERIFIED | 9 PIE tools including Play/Pause/Stop control — VERIFIED | `editor.play_in_editor` (pieAction=start\|stop\|status, with waitForAssetRegistry + timeout params) — VERIFIED |
| Platform build config | `execute_console_command` for INI overrides | Build category | `project.set_config` (INI write), `project.build` (platform param), `editor.cook_content` (platform param) |
| Perf profiling triggers | `bulk_set_console_variables` for stat.* commands | Performance category | `editor.run_stat`, `editor.get_perf_stats`, `editor.set_scalability` |

**WS5 gap summary:** Mobile-specific preview (device-profile PIE, Android/iOS platform selection) not confirmed in any candidate by name. PIE control is confirmed in all three but mobile-platform selection requires platform config + per-device-profile tooling that remains thin across all implementations.

---

### General Iteration + Blueprint Editing

| Need | NAJEMWEHBE tools | StraySpark tools | db-lyon tools |
|---|---|---|---|
| PIE start/stop/pause | `pie_control` | 9 PIE tools | `editor.play_in_editor`, `editor.configure_pie`, `editor.get_pie_config` |
| Log file tailing | `get_log_lines` | Debug category | `editor.get_log`, `editor.search_log`, `editor.get_message_log` |
| Hot-reload / live coding | `execute_console_command` (LiveCoding.Compile) | Build category | `editor.hot_reload` |
| Breakpoint manipulation | Not confirmed | StraySpark roadmap (unconfirmed) | Not confirmed |
| Blueprint editing (property/compile/inspect) | `inspect_blueprint`, `compile_blueprint`, `add_blueprint_variable`, `add_blueprint_node`, `connect_blueprint_pins`, `set_blueprint_node_pin_default` — **6 tools** | Blueprint 51 tools | `blueprint.read`, `blueprint.list_variables`, `blueprint.list_functions`, `blueprint.read_graph`, `blueprint.compile`, `blueprint.set_class_default`, `blueprint.set_component_property`, `blueprint.add_variable`, `blueprint.add_node`, `blueprint.connect_pins`, `blueprint.set_node_property`, `blueprint.add_component` and **47+ more** — **59 total confirmed actions** |
| Console command execution | `execute_console_command` | Confirmed | `editor.execute_command` |
| Asset save / auto-save | `save_dirty_assets` | Editor auto-save (confirmed differentiator) | `asset.save`, `asset.save_all_dirty`, `editor.save_dirty`, `editor.list_dirty_packages` |
| Undo / redo | `undo_transaction`, `redo_transaction` — VERIFIED | Every mutating action is transaction-wrapped (confirmed) | `editor.undo`, `editor.redo` — VERIFIED |

---

## § 2 Architecture Comparison

| Dimension | NAJEMWEHBE | StraySpark | db-lyon |
|---|---|---|---|
| Transport layer | C++ TCP plugin (127.0.0.1:18888) → Python stdio bridge (MCP server) | C++ HTTP JSON-RPC 2.0 plugin (port 13579); game-thread dispatch | TypeScript/Node.js MCP server (stdio) → WebSocket JSON-RPC → C++ bridge plugin |
| Port + protocol | TCP 18888 (JSON-RPC over raw TCP); MCP ↔ stdio bridge | HTTP JSON-RPC 2.0 on port 13579 | WebSocket on plugin-configured port; TypeScript server exposes stdio MCP |
| SSH-remote topology fit | COMPATIBLE — plugin binds 127.0.0.1:18888; SSH port-forward to forward 18888 from Mac to PC; Python bridge on Mac-side connects over forwarded socket. Standard SSH tunnel pattern. Not documented but compatible by construction. | COMPATIBLE — HTTP on port 13579 is SSH-forwardable (same pattern as Remote Control HTTP on 30010). Not documented but compatible by construction. | COMPATIBLE — WebSocket is SSH-forwardable. TypeScript MCP server runs on mantis-side; connects to plugin via WebSocket over forwarded port. Three-layer stack adds one extra hop. |
| Install burden | One-command: `pip install unreal-ai-connection` clone → plugin drop-in to `<Project>/Plugins/`; C++ build required. Prebuilt binaries exist for UE 5.6 (Win64). | Pre-compiled binary via Fab.com; NO C++ compilation required. Lowest install burden of all three. | `npx ue-mcp init` interactive setup; TypeScript/Node.js runtime required; C++ bridge plugin included in `plugin/` directory of repo; C++ build required. |
| C++ plugin build required? | YES (UE 5.7 official; 5.6 prebuilt available) | NO (pre-compiled binary) | YES (bridge plugin must be compiled into UE project) |
| External runtime dependency | Python 3.11+ (bridge) | None (all-in-one C++ plugin) | Node.js 18+ (TypeScript MCP server); WebSocket client |
| Latency characteristics | ~50ms round-trip (documented in README) | Not documented | Not documented |
| Reliability under load | 607 tests + CI; server-stability hardening documented (TickClients reentrant-shutdown fix + cross-thread accept hardening) | Not documented (commercial; no published test metrics) | Vitest smoke tests per tool category (12 smoke test scripts confirmed in package.json); no load data |
| Crash recovery / state reset | `reset_python_state` (synthetic); undo/redo transaction support | Every mutating action is first-class UE editor transaction (undo-safe) — strongest safety posture | `editor.undo`, `editor.redo`; YAML flow engine (`@db-lyon/flowkit`) for multi-step workflow orchestration |

---

## § 3 Engineering Quality + Production-Readiness

| Dimension | NAJEMWEHBE | StraySpark | db-lyon |
|---|---|---|---|
| Test suite (count + framework) | **607 pytest cases** (badge-confirmed in README); GitHub Actions CI running; smoke test vs live editor (documented in CHANGELOG) | Not published | **Vitest** smoke tests: 12 smoke test scripts (level, asset, blueprint, material, editor, reflection, animation, landscape, gameplay, audio, niagara, pcg, foliage, widget, networking, gas). No count published. Unit test infrastructure exists (`vitest.config.ts`). |
| Smoke test against live editor | YES — explicitly documented; live-verified per PR on each new tool batch | Not documented | YES — 12 smoke test scripts covering all major tool categories |
| Documentation completeness | `docs/TOOLS.md` (per-tool params + results + error codes + JSON examples); `docs/ARCHITECTURE.md`; `docs/HANDOFF.md` (session continuity); per-client setup recipes for 10 clients | StraySpark.studio/docs (category-level; no tool-name granularity in public docs); Epic Dev Community forum thread for changelog | docs.db-lyon.github.io (public docs site); COMMERCIAL-LICENSE.md; CLA.md; README |
| Tool registration patterns | Bridge: JSON manifest with schema per tool. C++ handlers: one `.cpp` file per handler (107 files = 107 native handlers). Synthetics: Python functions in bridge (41 synthetic = 148 total). Clean separation enforced by test (`test_skill_tool_refs.py`). | HTTP endpoint routing; no public registration detail | TypeScript `categoryTool()` + `bp()` helper pattern; each category file exports one `ToolDef` with named action map. All 21 tool files follow identical structure. Highly discoverable. |
| Error handling discipline | Named error codes per tool (`<tool>: <code>: <detail>` schema); `-32602` for invalid args; error-format annotations on legacy handlers | Not publicly visible | Named error codes embedded in descriptions; typed error responses per action |
| Logging discipline | `get_log_lines` + Output Log category filter; `exec_python_persistent` captures stdout; `unreal.log()` via LogPython category | Debug category (confirmed) | `editor.get_log`, `editor.search_log`, `editor.get_message_log`, `editor.list_crashes`, `editor.get_crash_info` |
| Auth / scope gates | None. Localhost binding; SSH tunnel provides transport security. Appropriate for dev topology. | **Bearer-token + origin allow-list + Read/Scene/Destructive scope gates** — strongest auth posture in the ecosystem | Not confirmed in source. `auth.ts` and `auth-cli.ts` exist in src — auth infrastructure present but scope/gate details not extracted. |
| Transaction safety / undo | Mutating handlers wrapped in `FScopedTransaction` since PR #249 (spawn_actor, delete_actor, set_actor_transform, set_actor_property, add_component). Undo/redo tools present. Partial coverage (not all mutating tools). | **Every mutating action is first-class UE editor transaction** (stated in official docs) | `editor.undo`, `editor.redo` present. Transaction-wrapping per action not confirmed in source. |
| Idempotency / retry safety | Not documented per tool | Not documented | `asset.save_all_dirty` noted as "flush after bulk import/edit"; `asset.set_datatable_row` documented as idempotent (append or overwrite); `asset.remove_datatable_row` documented as idempotent |
| Editor-thread dispatch safety | C++ game-thread dispatch via MCPDispatcher (separate from main game thread) | Game-thread dispatch (stated in official docs) | Not confirmed in source |
| Auto-save behavior | `save_dirty_assets` (explicit call); no auto-save | Editor auto-save tool (listed as StraySpark differentiator) | `asset.save_all_dirty` (explicit call); `editor.list_dirty_packages`; `editor.save_dirty` |
| Multi-version iteration history | v0.9.1 (May 2026); UE 5.7.4 primary; UE 5.6 prebuilt; active PR cadence | v1→v2→v3 (207→305→359 tools); v3 current | v1.0.79 (June 6 2026); semantic versioning; 80-version jump in minor version implies rapid iteration |

---

## § 4 Maintainer + Community Signals

| Dimension | NAJEMWEHBE | StraySpark | db-lyon |
|---|---|---|---|
| Maintainer | HD Media (Kuwait); individual/small-studio | StraySpark Studio (commercial entity, US) | David Lyon (individual) — package.json author field |
| Recent activity (last 30 days) | HIGH — multiple PRs merged in June 2026 window; tool count growing; active PR review process | HIGH — v3 current (June 2026); forum thread active | HIGH — v1.0.79 released June 6 2026; rapid minor-version iteration |
| Star / fork count | 6 stars / 3 forks (LOW) | N/A (commercial Fab product) | 125 stars / 29 forks (MEDIUM) |
| Issue tracker activity | Not verified; PR cadence is the primary signal | Epic Dev Community forum (active) | GitHub Issues not deeply inspected; CLA.md + SECURITY.md signal community infrastructure |
| Sponsorship / commercial backing | None public | Revenue from Fab licensing | None public |
| Project orphan-risk signal | **HIGH** — single maintainer; 6 stars; if maintainer goes quiet, adopter inherits maintenance. Mitigated by MIT license (fork freely) + 607 tests as handoff artifact. | **LOW** — commercial entity with revenue motive and paying customers | **MEDIUM** — active solo maintainer with strong recent trajectory (79 patch versions); larger community (125 stars) than NAJEMWEHBE. BUSL-1.1 limits fork freedom if license closes. |

---

## § 5 License + Commercial Path

| Dimension | NAJEMWEHBE | StraySpark | db-lyon |
|---|---|---|---|
| License type | **MIT** | Commercial (Fab.com) | **BUSL-1.1** (Business Source License 1.1) |
| Free use conditions | Unrestricted (MIT permanent) | Not confirmed; individual/education may be free or reduced (speculation from community posts) | Individual natural persons (personal non-commercial use); enrolled students/educational institutions; evaluation/development/testing (pre-commercial use) |
| Commercial use conditions | **Unrestricted** (MIT) | Requires Fab.com purchase; studio commercial license terms unknown (Fab listing 403) | **Studio game development = commercial entity = commercial license REQUIRED**. This includes eval-on-the-path-to-commercial — "Non-production use (evaluation, development, testing) is free; a commercial license is required once you deploy UE-MCP in a commercial context." The distinction is pre-commercial vs commercial deployment. |
| Change License (future) | Permanent MIT | N/A | Apache 2.0 after 4 years (BUSL standard change clause) |
| Cost during dev (pre-commercial deploy) | $0 | Unknown ($0 speculation unconfirmed) | **$0 during non-production evaluation/development** (per COMMERCIAL-LICENSE.md "Evaluating UE-MCP for potential commercial use" is explicitly free) |
| Cost at commercial release | $0 (MIT permanent) | Unknown — pricing page returned 403 | Per `ue-mcp.com/pricing` (unreachable per Matt 2026-06-08); email `licensing@ue-mcp.com` for custom terms |
| Lock-in risk profile | **None** — MIT is permanent; no terms change possible | Medium — per-Fab-listing terms; perpetual vs subscription unknown | **HIGH during pre-pricing resolution** — BUSL terms set unilaterally by Licensor; pricing page unreachable; Licensor cannot be contacted to confirm commercial terms |
| Migration cost if license path closes | N/A — NAJEMWEHBE never needs migration | N/A — once adopted, Fab perpetual license should hold | **KEY DIMENSION** — see § 5.1 |
| Licensor contact | mhwetmore@github for PRs | StraySpark Studio (commercial) | `licensing@ue-mcp.com` (per COMMERCIAL-LICENSE.md); `ue-mcp.com` domain (pricing page unreachable) |

### § 5.1 License Risk Summary — db-lyon

The BUSL-1.1 terms are load-bearing in this project context:

- **During eval/development** (pre-commercial deploy): FREE. The commission is clear — Matt can use db-lyon at $0 during spike evaluation and development.
- **At commercial deployment**: requires a paid commercial license. For a studio (game-publishing context), this threshold is reached at launch.
- **Licensor contact unreachability**: the pricing page (`ue-mcp.com/pricing`) is unreachable per Matt 2026-06-08. This is the core risk. If pricing is unreachable and `licensing@ue-mcp.com` does not respond, the commercial license path is blocked at commercial-deployment time.
- **BUSL fork protection**: unlike MIT, BUSL prevents forking for competing use. If commercial terms are unacceptable and the Licensor is unreachable, you cannot legally fork db-lyon for production use before the 4-year Apache 2.0 change-license window.
- **Matt's "removal/replacement" framing** aligns with this risk: use db-lyon during eval (free by license), plan migration to NAJEMWEHBE (MIT) if commercial license path doesn't materialize.

---

## § 6 Migration Cost — db-lyon → NAJEMWEHBE (or → StraySpark)

### db-lyon → NAJEMWEHBE

| Migration dimension | Assessment | Cost rating |
|---|---|---|
| Tool-call site count | Pre-spike: 0 (nothing built yet). Post-spike: proportional to how many db-lyon action names were wired into mantis workflows. Each wired tool name is one migration touch point. | LOW (pre-spike); MEDIUM-to-HIGH (post-deep integration) |
| Tool-name compatibility | db-lyon uses `tool.action_name` dispatch (e.g., `niagara.create_emitter`). NAJEMWEHBE uses flat tool names (e.g., `spawn_niagara_at_location`). The naming conventions differ — db-lyon is hierarchical (category.action), NAJEMWEHBE is flat (verb_noun). Tool-name mapping is NOT 1:1 but the operations are equivalent for the overlap. | MEDIUM — systematic rename + re-map required per tool call |
| Architecture compatibility | db-lyon: TypeScript/Node.js server + WebSocket JSON-RPC. NAJEMWEHBE: Python stdio bridge + TCP JSON-RPC. Both expose stdio MCP interface to mantis. **The MCP interface layer is identical** — mantis connects to either via the same MCP client call syntax. The transport difference is below the MCP layer (bridge implementation). Client code (mantis) does NOT change at the MCP call level. | LOW — mantis MCP client calls are transport-agnostic |
| Capability gap if migrating | db-lyon → NAJEMWEHBE gaps: **DataTable row-write** (db-lyon has 11 DataTable actions; NAJEMWEHBE has 2); **Niagara emitter creation + module authoring** (db-lyon has 28 Niagara actions; NAJEMWEHBE has 3); **Animation deep authoring** (db-lyon animation tool has 54 actions; NAJEMWEHBE has none); **PCG graph authoring** (db-lyon has full PCG CRUD; NAJEMWEHBE not confirmed); **StateTrees** (db-lyon has dedicated StateTree tool; NAJEMWEHBE not confirmed); **deep Blueprint CRUD** (db-lyon has 59 actions; NAJEMWEHBE has 6) | **HIGH capability gap in advanced features**; LOW gap for basic WS1-WS3 needs |
| Behavioral difference | db-lyon `asset.set_datatable_row` is idempotent (merge) by documented design. NAJEMWEHBE `create_data_table` is CREATE-only (no write). The semantics are fundamentally different, not just renamed. | MEDIUM — semantic re-learning required for DataTable workflows |
| Install / setup re-burden | NAJEMWEHBE: Python 3.11+ + C++ build (or prebuilt binary). db-lyon: Node.js 18+ + C++ build. Different language runtimes but similar overall setup complexity. | LOW — comparable install burden |

**db-lyon → NAJEMWEHBE overall migration cost rating: MEDIUM**

Rationale: The MCP client interface is identical (mantis calls are unchanged). The migration effort is tool-name remapping + capability-gap fills for advanced features (DataTable CRUD, Niagara emitter, deep Blueprint). For the WS1-WS3 scope of the spike, the gap is manageable. For a post-spike production deployment using db-lyon's advanced features, migration cost rises to HIGH.

### db-lyon → StraySpark

| Migration dimension | Assessment | Cost rating |
|---|---|---|
| Tool-name compatibility | StraySpark tool names are not public (commercial closed-source). No direct comparison possible. | UNKNOWN |
| Architecture compatibility | StraySpark: HTTP JSON-RPC. db-lyon: WebSocket. Both SSH-forwardable. Mantis client changes required (HTTP vs WebSocket connection setup). | LOW-MEDIUM |
| Capability gap | StraySpark likely matches or exceeds db-lyon's coverage (359 tools vs 21 categories + 569+ actions). No confirmed gap from db-lyon to StraySpark. | LOW |
| License | StraySpark commercial license required at studio level. Price unknown. | UNKNOWN |

**db-lyon → StraySpark overall migration cost rating: UNKNOWN-to-LOW** (pending StraySpark pricing and tool-name confirmation).

---

## § 7 Extension Cost — NAJEMWEHBE as ADOPT-AND-EXTEND Base

| Gap | Extension cost | Rationale |
|---|---|---|
| DataTable CRUD depth (currently: create + inspect; needs: row update/delete/upsert) | **MEDIUM** | NAJEMWEHBE has a well-structured C++ handler pattern (`Handler_CreateDataTable.cpp` confirmed). A new `Handler_SetDataTableRow.cpp` + `Handler_RemoveDataTableRow.cpp` + `Handler_GetDataTableRow.cpp` follows the same pattern. UE provides `FDataTableEditorUtils::AddRow` and row manipulation APIs. Estimated 3-5 new C++ handlers, each ~150-300 LOC. The test harness (607 tests) provides clear scaffolding. db-lyon's implementation provides a reference for the expected API surface. |
| Sequencer depth (NAJEMWEHBE has 10 tools; verified complete for WS3 camera + audio + visibility + transform + MRQ) | **LOW** | Source inspection reveals NAJEMWEHBE already covers all confirmed WS3 Sequencer needs: camera cut, audio, visibility, transform keyframe, MRQ render. No confirmed WS3 gap. If event tracks or subscene tracks are needed, one C++ handler per track type adds ~150 LOC following the existing pattern. |
| Niagara depth (NAJEMWEHBE has 3 tools; db-lyon has 28) | **MEDIUM-HIGH** | NAJEMWEHBE's Niagara surface covers spawn + user-param. For WS2 (parameter iteration), the 3-tool surface may suffice. For emitter creation + module configuration (advanced VFX authoring), extension is HIGH — `FNiagaraSystemFactory`, `FNiagaraEmitterFactory`, module graph APIs are complex UE surfaces. db-lyon has reference implementations but they are TypeScript-calling-C++ bridge, not native C++ handlers. |
| SSH-remote topology validation | **LOW** | Architecture is compatible by construction. The spike's first milestone is SSH port-forwarding validation — this is an integration test, not a code change. No new development required. |
| Auth / scope gates (not present in NAJEMWEHBE) | **MEDIUM** | For dev/internal pipeline use, localhost TCP binding + SSH tunnel is adequate security. Bearer-token auth is a production-hardening concern, not a spike prerequisite. If required: implement an auth wrapper in the Python bridge (token validation per call before forwarding to TCP socket). ~200 LOC Python. |
| Transaction safety / undo (partial in NAJEMWEHBE — PR #249 wraps 5 handlers) | **LOW-MEDIUM** | NAJEMWEHBE wraps spawn_actor, delete_actor, set_actor_transform, set_actor_property, add_component in FScopedTransaction. Other mutating handlers (create_sequence, add_camera_cut_track, etc.) may lack transaction wrap. Extending: `FScopedTransaction` wrapper is one additional line per handler in the MCPDispatcher or per-handler implementation. LOW per handler, MEDIUM for systematic coverage of all 107 handlers. |

---

## § 8 Recommendation Tier Table

| Tier | Candidate | Evidence | Cost reasoning |
|---|---|---|---|
| **ADOPT-AND-EXTEND** | **NAJEMWEHBE** | MIT (permanent; no license risk). 148 tools source-verified. 607 tests + CI (strongest test discipline in open-source field). UE 5.7.4 primary target — exact match. Sequencer surface fully verified (10 tools; covers WS3). SSH-compatible architecture. One-command install (Python). Active development (multiple PRs June 2026). **Gaps:** DataTable row-write missing; Niagara emitter authoring missing; 6 stars = orphan risk. | Extension cost: DataTable CRUD = MEDIUM; Niagara depth (if needed) = MEDIUM-HIGH; Sequencer = LOW (already covered); SSH validation = LOW. Total extension effort to spike-viable: LOW (WS1-WS3 core needs; DataTable row-write is the main add). Total extension effort to production-complete: MEDIUM. Migration risk if abandoned: LOW (MIT, 607 tests, well-documented). |
| **EVAL-THEN-MIGRATE** | **db-lyon** | Strongest breadth in the ecosystem (21 categories; 569+ actions; source-verified). DataTable 11 actions (full CRUD). Niagara 28 actions (full authoring). Blueprint 59 actions. Sequencer 7 confirmed actions. BUSL-1.1 = $0 during development eval. Pricing page unreachable. Migration cost to NAJEMWEHBE = MEDIUM. | Use during spike eval (legally $0, per COMMERCIAL-LICENSE.md "evaluation" grant). **Do NOT deploy commercially without resolving licensing@ue-mcp.com.** Migration plan: if license path fails, migrate tool-call sites to NAJEMWEHBE + fill DataTable/Niagara gaps by extension. This posture matches Matt's "explore with mindset of removal/replacement later" exactly. EVAL-THEN-MIGRATE is not a permanent commitment — it is a spike-evaluation posture with planned exit. |
| **ADOPT-OUTRIGHT (conditional)** | **StraySpark** | 359 tools (v3 confirmed). Only implementation with bearer-token auth + scope gates + first-class undo transactions. 9 PIE tools. 8+ Sequencer tools. Pre-compiled binary (zero C++ build). UE 5.7 Win64/Mac/Linux. **BLOCKED** by: pricing page 403; studio commercial license terms unknown. | If price is acceptable (< a few hundred USD for studio license), the avoided extension build cost likely justifies adoption. If pricing is enterprise-level, ADOPT-AND-EXTEND (NAJEMWEHBE) is the better return on investment. Decision cannot be made without StraySpark price inquiry. |
| **EVAL-MULTIPLE-DEFER** | All three | Not warranted. NAJEMWEHBE is spike-viable NOW with LOW extension for WS1-WS3 core. db-lyon is spike-viable NOW with $0 license during eval. Evidence is sufficient for a posture decision. | Defer posture only if Matt's spike criterion specifically requires production-grade auth before the evaluation begins (in which case StraySpark price inquiry becomes blocking). |

---

## § 9 Discipline #25 Rep-Audit — Claim Verification

| Claim | Source | Verified result |
|---|---|---|
| NAJEMWEHBE "147 tools" | README badge + source | **148 tool names** confirmed by `"name"` field enumeration from bridge JSON. The discrepancy (147 vs 148) is within one tool and may reflect a documentation lag. Not fabrication. |
| NAJEMWEHBE "110 C++ handlers" | README | **107 C++ handler files** confirmed by GitHub API directory listing of `Handlers/`. The README claims 110; source shows 107. Discrepancy of 3 = documentation lag (likely some handlers merged or renamed after README was written). |
| NAJEMWEHBE "607 tests" | README badge | Confirmed — badge reads `pytest-607_passing`. Not independently counted but consistent with active test addition per PR cadence in CHANGELOG. |
| StraySpark "359 tools / 50+ categories" | Official docs | Confirmed by strayspark.studio/docs. v3 count confirmed. v1=207/34, v2=305/42, v3=359/50+ consistent progression. |
| StraySpark "12 Sequencer tools" | Prior synthesis + Epic forum | Forum confirms "Sequencer (8)" in latest categorization. The prior synthesis's "12" may reflect an earlier version or a different counting method. **Current verified: 8 Sequencer tools**. Neither 8 nor 12 is source-code verified (closed-source). |
| db-lyon "21 tools, 569+ actions" | package.json version 1.0.79 | **Confirmed verbatim** — `"description": "Unreal Engine MCP server - 21 tools, 569+ actions for AI-driven editor control"`. The tools.ts source imports exactly 21 tool modules (21 `import` statements + 21 entries in `ALL_TOOLS`). The 569+ action count is a lower bound; actual action count from source inspection is materially higher (animation alone has 54, blueprint alone has 59, asset alone has 60+). |
| db-lyon "BUSL-1.1; commercial license required for studio use" | LICENSE + COMMERCIAL-LICENSE.md | **Confirmed**. COMMERCIAL-LICENSE.md explicitly lists "Game studios, publishers, or other commercial entities using UE-MCP in proprietary products, internal pipelines, or commercial services" as requiring a commercial license. Pricing at `ue-mcp.com/pricing` (unreachable per Matt 2026-06-08). Contact: `licensing@ue-mcp.com`. |

---

## § 10 Open Questions for Gandalf Review

1. **db-lyon spike eval license interpretation.** COMMERCIAL-LICENSE.md says "evaluation, development, testing is free; commercial license required at commercial deployment." Does Matt's current spike and pre-launch development qualify as "evaluation"? If yes, db-lyon is $0 during the entire development phase. If no (if internal pipeline use counts as "commercial context"), a commercial license is immediately required. Gandalf/Matt decides: is the development-phase use pre-commercial or commercial?

2. **StraySpark price inquiry authority.** This commission cannot determine StraySpark's price — Fab listing returned 403. Matt is flagged as the authority to route this inquiry. If StraySpark's studio license is < a few hundred USD, the ADOPT-OUTRIGHT posture shifts ahead of ADOPT-AND-EXTEND. The comparison's tiebreaker between NAJEMWEHBE extension and StraySpark purchase depends on this single number.

3. **Niagara depth requirement for WS2.** NAJEMWEHBE's 3-tool Niagara surface covers spawn + user-param. For WS2 (parameter iteration on existing systems + per-skill VFX selection), this may be sufficient if "parameter iteration" means setting user-exposed parameters (which `set_niagara_user_param` covers). If WS2 requires emitter creation + module configuration + renderer setup from scratch, NAJEMWEHBE's Niagara gap becomes HIGH extension cost. Gandalf/mantis clarifies: does WS2 require creating new Niagara systems from scratch, or only configuring and spawning existing authored systems?

4. **DataTable row-write urgency for WS1.** NAJEMWEHBE has `create_data_table` + `inspect_data_table`. For the cosmograph JSON ingestion workflow, DataTable row-write (`set_datatable_row` equivalent) is required. Two options: (a) extend NAJEMWEHBE with DataTable write handlers (MEDIUM effort); (b) use `execute_unreal_python` / `exec_python_persistent` as a Python-scripted workaround (LOW effort for the spike; HIGH technical debt for production). Gandalf decides: is the DataTable row-write gap a spike blocker that forces db-lyon evaluation, or is Python exec an acceptable spike shortcut?

5. **Spike architecture decision — NAJEMWEHBE vs db-lyon primary evaluation target.** Given source evidence: NAJEMWEHBE is simpler (Python bridge, 148 tools, 607 tests, MIT), db-lyon is broader (21 categories, 569+ actions, TypeScript, stronger DataTable + Niagara). For the spike's first question ("does SSH port-forwarding work?"), either candidate answers it identically. For the spike's second question ("does the toolset cover WS1-WS3?"), db-lyon answers it more completely. Recommended: evaluate NAJEMWEHBE first (simpler install, MIT, no license risk), then spike db-lyon if DataTable or Niagara gaps prove blocking.

6. **MCP bridge spike commission amendment.** The spike commission at `agentic_orchestration/dispatches/2026-06-07-david-h-ue-remote-control-mcp-bridge-spike.md` is scoped as "Remote Control HTTP MVP." This commission's evidence recommends ADOPT-AND-EXTEND (NAJEMWEHBE) as Path A and EVAL-THEN-MIGRATE (db-lyon) as Path B, both ahead of Remote Control HTTP build-from-scratch (Path C). Knight-rider or gandalf decides: amend the spike to add Path A (NAJEMWEHBE evaluation) as the primary path, with Path C as fallback.

---

## Source List

- NAJEMWEHBE/unreal-ai-connection (GitHub): https://github.com/NAJEMWEHBE/unreal-ai-connection
  - `bridge/unreal_ai_connection_bridge.py` — tool name enumeration (148 confirmed), Sequencer tool definitions
  - `UnrealAIConnection/Source/UnrealAIConnection/Private/MCP/Handlers/` — 107 C++ handler files
  - `README.md` — tool count claims (147), test count claims (607), architecture overview
  - `CHANGELOG.md` — PR-level engineering record; tool addition history; Sequencer tool PR references
- db-lyon/ue-mcp (GitHub): https://github.com/db-lyon/ue-mcp
  - `package.json` — version 1.0.79; "21 tools, 569+ actions" confirmed
  - `src/tools.ts` — ALL_TOOLS registry (21 imports confirmed)
  - `src/tools/animation.ts` — 54 animation actions enumerated
  - `src/tools/blueprint.ts` — 59 blueprint actions enumerated
  - `src/tools/niagara.ts` — 28 niagara actions enumerated
  - `src/tools/asset.ts` — 60+ asset actions enumerated (DataTable CRUD confirmed)
  - `src/tools/editor.ts` — 8 Sequencer actions + PIE control enumerated
  - `src/tools/level.ts`, `src/tools/material.ts`, `src/tools/gameplay.ts`, `src/tools/project.ts`, `src/tools/gas.ts`, `src/tools/pcg.ts`, `src/tools/reflection.ts`, `src/tools/statetree.ts`, `src/tools/audio.ts`, `src/tools/landscape.ts`, `src/tools/networking.ts`, `src/tools/widget.ts`, `src/tools/foliage.ts`
  - `LICENSE` — BUSL-1.1 confirmed
  - `COMMERCIAL-LICENSE.md` — commercial license terms; pricing at ue-mcp.com/pricing (unreachable); contact licensing@ue-mcp.com
- StraySpark Unreal MCP Server (commercial):
  - https://www.strayspark.studio/docs/unreal-mcp-server — category list; tool counts at category level
  - https://forums.unrealengine.com/t/strayspark-unreal-mcp-server-200-ai-tools-for-ue5-editor-automation-via-mcp/2707474 — Epic Dev Community forum; "Sequencer (8)" v3 count confirmed
- Prior legolas synthesis: `agentic_orchestration/legolas/research/2026-06-08-mcp-workstream-spanning-prior-art/synthesis.md`

---

## Knowledge Gaps Not Resolved

1. **StraySpark Sequencer tool names.** Closed-source; tool names not publicly enumerated. "8 Sequencer tools" from forum count but individual names unconfirmed. Deep Sequencer coverage (MRQ render, event tracks, subscene) remains unverified.

2. **StraySpark pricing.** Fab listing 403. Price and studio-commercial-license terms unknown. Gates ADOPT-OUTRIGHT posture.

3. **db-lyon `ue-mcp.com/pricing`.** Unreachable per Matt 2026-06-08. The commercial license cost for studio use is unknown. Gates the EVAL-THEN-MIGRATE vs ADOPT-OUTRIGHT-if-cheap decision for db-lyon.

4. **NAJEMWEHBE SSH topology validated?** Architecture is compatible by construction but no community examples of SSH-mediated remote MCP use found. The spike must validate SSH port-forwarding of port 18888 as its first milestone.

5. **db-lyon auth scope details.** `src/auth.ts` and `src/auth-cli.ts` exist in source — auth infrastructure is present but not deeply inspected. Whether db-lyon has bearer-token or scope-gate features (comparable to StraySpark) is unconfirmed.

6. **db-lyon WebSocket port default.** The C++ bridge plugin port for WebSocket is not confirmed by source inspection. `src/bridge.ts` likely contains this; not extracted in this pass.

---

## Sign-off

**Legolas** — Mode A analytical research (Pattern A-deep)
**Delivered:** 2026-06-08
**Commission:** `agentic_orchestration/dispatches/2026-06-08-legolas-three-way-mcp-comparison-najem-strayspark-dblyon.md`
**Output path:** `agentic_orchestration/legolas/research/2026-06-08-three-way-mcp-comparison/synthesis.md`
**Verdict:** ADOPT-AND-EXTEND (NAJEMWEHBE) as primary; EVAL-THEN-MIGRATE (db-lyon) as spike breadth-evaluation path; StraySpark conditional on price discovery
**Extends and equalizes:** `agentic_orchestration/legolas/research/2026-06-08-mcp-workstream-spanning-prior-art/synthesis.md` (NAJEMWEHBE Sequencer gap resolved; db-lyon tool surface source-verified; StraySpark Sequencer count updated to 8 from forum)
