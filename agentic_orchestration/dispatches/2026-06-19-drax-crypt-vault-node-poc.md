# Dispatch — 2026-06-19 — drax (then galadriel) — Crypt-Vault Node Vignette PoC

**From:** knight-rider
**To:** drax (authoring + Gate 1), then galadriel (Gate 2)
**Approved by:** Matt 2026-06-19 ("ok, let's give it a shot"); sequenced by knight-rider out of gandalf's Pattern B design dialogue
**Estimated effort:** multi-session (Pattern B — own session memory; structure-first authoring loop + dual-gate)
**Acceptance:** A coherent, composable crypt-vault **clear-room NODE** in `reincarnated-godot`, authored structure-first via the godot-mcp tool, that **passes Gate 1 (structural) and Gate 2 (register)**, delivered to Matt as a **multi-angle ORBIT render set** (never a single hero angle) for his Gate-3 coherence verdict — plus a **first-draft Act-Graph node schema DERIVED from what the node actually needed**.

---

## Context

This is the **first node-authoring PoC of the "From JSON to Seasons" map pipeline.** It proves that the **author-in-MCP, structure-first, three-gate method produces a coherent, composable NODE that passes Matt** — fixing the spatial-coherence failures the prior open-loop snapshot-scoring loop shipped (overlapping crypts, half-hidden doors, floating/clipping floors, reasonless walls). The single-camera-angle blindness that shipped the broken scene is exactly the failure mode this method exists to fix; that is why the acceptance unit is an orbit set, not a hero shot.

It is a **vertical slice of ONE node-type** (architected-dungeon clear-room). Passing it validates the method that the Template Library (Layer 2) will later scale across node-types. **Nothing scales to a second node-type, multi-node stitching, or fight execution until Matt passes THIS node** (brief §7 non-goals). The larger architecture (From JSON to Seasons + katabasis) is NOT canonicalized until this PoC validates the method — recognition → validate → commit.

The AUTHORITATIVE spec is gandalf's brief (required reading below). This dispatch sequences the build loop and encodes the operational refinements knight-rider verified against the live repo state.

## Required reading before starting

1. **`agentic_orchestration/gandalf/notes/2026-06-19-crypt-vault-node-poc-brief.md`** — the AUTHORITATIVE PoC spec (unit definition, target spec §3, three-gate method §4, schema co-emergence §5, build sequence §6, non-goals §7, carried friction §8). Everything binding is here; this dispatch defers to it on any conflict.
2. **`agentic_orchestration/legolas/research/2026-06-19-godot-mcp-comparison/smoke-test-result.md`** — the validated tool (satelliteoflove/godot-mcp v4.0.1, all 4 checks PASS) + the full setup-friction list the build MUST account for.
3. **`canonical/story/battle-room-presentation-decoupling-2026-06-15.md`** — the sim-invariant/presentation decoupling, the **annulus rule**, the single-wall-ring topology, the §2-bis architectural-grammar load-path test, and the **35/35 spawn parity** discipline. The node's fight footprint MUST honor the invariant; dressing lives in the annulus, not the pit.
4. **`canonical/story/style-register.md`** — the locked register (3D-Godot-2.5D-camera, A-holds, **cathedral register** at composite 5.00 on `Demo_Cathedral_01`) + the lift recipe. The PoC holds this register CONSTANT — spatial coherence is the ONLY new variable.

## Repo ground-state knight-rider verified (read before step 1 — these correct/extend brief §6)

- **The MCP addon is NOT currently installed.** `~/Games/reincarnated-godot/addons/` holds only `godot-sqlite` and `sidekick_creator`. The smoke-test fully reverted itself (removed `addons/godot_mcp/`), byte-identical to HEAD. So step 1 is broader than "enable the plugin" — you must **re-install the addon first**, THEN enable it, THEN wire `.mcp.json`. Brief §6 step 1 assumes the addon is present; it is not.
- **There is NO `.mcp.json`** in either `reincarnated-godot/` or `reincarnated-collaboration/`. You must create one so your interactive session picks up the MCP server (smoke-test friction #1: spawn `dist/cli.js`, not `dist/index.js`; the `npx @satelliteoflove/godot-mcp` form resolves correctly — prefer it).
- **`project.godot` currently enables ONLY `sidekick_creator`** (`[editor_plugins] enabled=PackedStringArray("res://addons/sidekick_creator/plugin.cfg")`) and has an `[addons] sidekick_creator/...` block (lines 11-14). Friction #4: enabling the MCP plugin rewrites `project.godot` (adds `MCPGameBridge` autoload + `[godot_mcp]` block) and in the smoke-test **silently dropped an unrelated config block**. You MUST verify the diff preserves the `sidekick_creator` autoload/`[addons]` block and only ADDS the MCP entries.
- **The clear-room shells live at `reincarnated-godot/data/arena_scenarios.json`** (6 scenarios). knight-rider's read of the non-boss clear-room candidates (you make the final call, but justify it):
  | scenario | shape | spawns (non-player) | clear-room fit for crypt-vault |
  |---|---|---|---|
  | `elite_pack` | 28×28 square | 3 (1 elite + 2 magic) | **knight-rider lean** — most "room"-like enclosed contained shell; modest spawn count; square reads as a vault chamber; `all_mobs_killed` clear-room win-condition |
  | `magic_pack` | 32.7×14 trash room | 4 (1 magic + 3 swarm) | viable alternate — explicitly a "trash room"; the most-common clear-room archetype; long-thin shape exercises socket placement on a corridor-ish footprint |
  | `chokepoint_corridor` | 10×50 corridor | 8 swarm | possible but corridor topology is a worse fit for a "vault chamber" read; defer |
  | `open_arena` | 50×50 reference | 8 swarm | reference baseline; large + open; a less representative clear-room |
  | `boss_with_adds`, `mini_boss` | — | — | **OUT** — boss / mini-boss, not clear-rooms (brief §3: NOT boss-arena) |
  Pick ONE representative non-boss clear-room; **preserve its playable footprint + all spawn markers at parity** (the annulus rule — dressing OUTSIDE the playable AABB; the pit stays clear + unwalled). Record which scenario and why in your AGENT_STATE + completion record.
- **galadriel's CV instruments are galadriel-owned** at `agentic_orchestration/galadriel/pipeline/` (`register-metrics.mjs`, `lifecycle-score.mjs`, `arch-grammar-band-probe.mjs`). Not your concern to run — galadriel runs Gate 2. Your job ends at Gate 1 + handing galadriel a capturable scene + an orbit render set.

## Math-before-code (Discipline #1)

Before placing any GridMap cells, document in your AGENT_STATE (math-note discipline, code-cited):
1. **Grid lock per kit (brief §3 / §8).** Lock grid-per-kit BEFORE placing cells. Synty dungeon kit native grid (Dungeon Pack 5m / Build 2.0 2.5–3m). State the chosen kit, its native cell size, and build the MeshLibrary from the kit at that native grid. GridMap orientation is an **index 0-23** (24 orthogonal rotations), NOT Euler (friction #5) — note the orientation indices you'll use for walls/door/stair.
2. **Footprint-to-grid mapping.** The chosen shell's playable footprint (e.g. elite_pack 28×28 m) mapped onto the locked grid → cell counts. The playable footprint is an **invisible sub-region** of a larger dressed floor (Layer 2 / annulus rule); state the outer/visual footprint extent and the annulus band `[playable-edge → outer wall]`. Tile the FULL footprint with the playable floor material (iter4 floor-tiling root cause — the playable footprint must NEVER be the only tiled region).
3. **Spawn parity arithmetic.** The shell's spawn markers `(x,0,y)` preserved exactly within the playable sub-region; state how you verify N-in == N-out (the 35/35-analog parity check for THIS shell's spawn count — e.g. elite_pack = 4 markers incl. player). Spawn POSITIONS are sim-invariant; facing/scale/dressing are presentation (Layer 1).
4. **Socket geometry.** Entrance + exit socket positions/orientations on the grid (proves composability even though the PoC connects to nothing). State their grid coordinates + orientation indices.
5. **Load-path one-test (§2-bis) for the stair+mezzanine + any arch.** Before placing the vertical element: "if this were stone and gravity were on, would it stand, and is it doing a job?" The mezzanine sits OUTSIDE the playable footprint (combatants never go up — annulus/backdrop). No orphan verticals; no floating spans.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)

Does this dispatch add, modify, rename, or remove any field on a telemetry schema table, a fight_log dict key, a loadout dict key, an export packet structure, or any other inter-seam fixture dict?

**NO.** This is a Godot-presentation-seam PoC. It authors a `.tscn` + MeshLibrary + GridMap and a first-draft node schema that is **explicitly NOT canonicalized** (brief §5 / §7 — substrate-led draft only, derived from the node, not imposed; no engine consumer wired). It does NOT touch the simulation→export telemetry boundary, fight_log, loadout dicts, or season-JSON export shape. The `arena_scenarios.json` shell is consumed READ-ONLY (footprint + spawns preserved at parity; nothing written back).

**Round-trip: not applicable — no cross-seam contract change in this dispatch.**

## Scope

### Phase 1 — drax: MCP enablement (DELIBERATE, diff-reviewed)
- [ ] Re-install the godot-mcp addon: `npx @satelliteoflove/godot-mcp --install-addon ~/Games/reincarnated-godot` (the addon is currently absent — verified by knight-rider)
- [ ] Create `.mcp.json` (godot repo root preferred) pointing at the `npx @satelliteoflove/godot-mcp` server (friction #1 — the npx form resolves `cli.js` correctly; do NOT hand-wire `index.js`)
- [ ] Open the Godot editor with the plugin enabled (Project Settings > Plugins > "Godot MCP"); gate the first real MCP call on a cheap `godot_project get_info` poll (friction #2 — lazy background connection with backoff)
- [ ] **Diff-review the `project.godot` mutation (friction #4):** confirm the enable ADDS `MCPGameBridge` autoload + `[godot_mcp]` block AND does NOT drop the existing `sidekick_creator` autoload / `[addons]` block (lines 11-14) / the `sidekick_creator/plugin.cfg` editor-plugin entry. If the editor silently drops anything, restore it before committing.
- [ ] Commit the enablement as its OWN deliberate commit with the reviewed diff (do NOT fold it into the node-authoring commit)

### Phase 2 — drax: author the crypt-vault clear-room NODE (structure-first)
- [ ] Select the representative non-boss clear-room shell from `arena_scenarios.json` (knight-rider leans `elite_pack`; you decide + justify)
- [ ] Lock grid-per-kit; build the GridMap node + MeshLibrary from the Synty dungeon kit at its native grid (file-first; cells go ONLY through `godot_gridmap_edit` — friction #8, tool-enforced structure-first)
- [ ] **STRUCTURE (GridMap, snap-to-grid):** walls, floor (full footprint tiled with playable-floor material), a **door as a wall-variant cell on the shared grid** (cannot be half-occluded by construction — the direct fix for half-hidden doors), and ONE **stair + mezzanine** vertical element (mezzanine outside the playable footprint)
- [ ] **LARGE ASSETS as STRUCTURE:** **3–4 grid-snapped sarcophagi**, deliberately placed (the direct rebuke to the ~50-overlapping-crypts failure — large architectural pieces are grid-placed + few, NOT scatter)
- [ ] **DRESSING (ProtonScatter):** small organic clutter ONLY (rubble, candle-stubs) where overlap doesn't read as wrong; group all impassable dressing under a clearly-named `nonpassable_dressing` group (decoupling doc §5 — cheap now, saves a manual sweep at the live-combat milestone)
- [ ] **SOCKETS:** defined entrance + exit socket positions/orientations on the grid
- [ ] **FIGHT FOOTPRINT:** preserve the chosen shell's playable footprint + ALL spawn markers at parity (annulus rule — dressing strictly OUTSIDE the playable AABB + readability margin; the pit stays clear and UNWALLED; single outer wall ring only)
- [ ] **REGISTER held CONSTANT:** apply the proven cathedral-register lift recipe baseline (the `lift_render.tscn` / cathedral recipe levers). Do NOT introduce band/register-laddering — spatial coherence is the only variable under test.

### Phase 3 — drax: Gate 1 (structural, camera-INDEPENDENT, via MCP engine-truth)
- [ ] No structure-on-structure AABB overlaps (walls/door/floor/stair/sarcophagi) — via `godot_scene3d get_spatial_info` (engine-computed `global_aabb`) + interval-intersection (friction #6 — pass `type_filter`/`within_aabb`/`max_results`; never an unbounded `get_scene_tree`)
- [ ] All GridMap cells valid; door = wall-variant on the shared grid
- [ ] A* passability: entrance socket → exit socket reachable on the floor
- [ ] Vertical navigability: mezzanine reachable via the stair; clearance passable (no mid-character floors)
- [ ] Fight-spawn parity: chosen shell's spawns + footprint preserved (N-in == N-out; annulus rule)
- [ ] Record Gate-1 results (PASS/FAIL per criterion, with the engine-truth evidence) in the completion record

### Phase 4 — drax: deliver the orbit render set for Gate 3
- [ ] Produce an **ORBIT render set** (multiple framings around the node — NEVER a single hero angle) + a **walk-through if feasible**. State the output directory path explicitly. This is the unit Matt judges at Gate 3.
- [ ] (Single camera angles are permitted ONLY as a fast inner-loop register-dimension instrument during iteration — never as the acceptance unit. Brief §4 note.)

### Phase 5 — drax: first-draft Act-Graph node schema (substrate-led)
- [ ] Author the first-draft node schema DERIVED from what THIS node actually needed (brief §5): confirm/extend `node_type, footprint, fight_shell_ref, sockets[], meshlibrary_ref, register_preset, grid_size, vertical_layers, dressing_rules`. Do NOT pre-impose — let the authored node define the fields. Deliver as a draft artifact (NOT canonicalized; explicitly marked PoC-draft).

### Phase 6 — galadriel: Gate 2 (register, multi-angle CV)
- [ ] Multi-angle register CV across SEVERAL framings (not one hero shot): HFD/LMV/LDR/SAT/HLF within the band the cathedral hit (composite ≥ 3.6 PASS; both mandatory gates lighting ≥ 4, VFX ≥ 4). Use galadriel's own instruments at `agentic_orchestration/galadriel/pipeline/`.
- [ ] **MCP single-client constraint (port 6550, hard singleton — friction #7):** drax authors + closes his MCP session FIRST, THEN galadriel judges; OR galadriel runs as a sub-agent inheriting drax's connection. Do NOT open a 2nd concurrent client (2nd is rejected, WS close 4001, 45s stale-takeover). Galadriel's CV scoring is on captured frames and does NOT require the MCP at all — preferred path: drax hands off captured frames + the orbit set, galadriel scores offline.
- [ ] Record Gate-2 register results (per-axis scores + composite + band-pass) in a galadriel report under `agentic_orchestration/galadriel/reports/`.

### Standing items
- [ ] AGENT_STATE.md updated at session end (drax: `~/Games/reincarnated-godot/AGENT_STATE.md`)
- [ ] Round-trip smoke (or not-applicable justification) per Principle 6 — **already declared N/A above**
- [ ] Tags: seam-prefixed per convention (e.g. `drax/v-crypt-vault-node-poc-1` for the node; a separate small tag/commit for the MCP enablement). Milestone (unprefixed) tags only on Matt approval.

## Acceptance criteria
- [ ] MCP plugin re-installed + enabled in a deliberate diff-reviewed commit that PRESERVES the `sidekick_creator` config (friction #4 verified)
- [ ] Crypt-vault clear-room NODE authored structure-first: grid-snapped walls/floor/door-as-wall-variant/one-stair+mezzanine; 3–4 grid-snapped sarcophagi; scatter clutter only; defined entrance+exit sockets; cathedral register held constant
- [ ] Fight footprint sized around a real non-boss clear-room shell with footprint + spawns preserved at parity (annulus rule; pit unwalled; single outer wall ring)
- [ ] **Gate 1 PASS** on all 5 structural criteria via MCP engine-truth (overlaps / cells / A* entrance→exit / vertical-nav / spawn-parity)
- [ ] **Gate 2 PASS** — multi-angle register CV in the cathedral band (composite ≥ 3.6; lighting ≥ 4; VFX ≥ 4)
- [ ] **ORBIT render set delivered** (+ walk-through if feasible) at a stated path — NEVER a single hero angle
- [ ] First-draft Act-Graph node schema delivered, derived from the authored node, explicitly marked PoC-draft (not canonicalized)
- [ ] Round-trip: not applicable — no cross-seam contract change in this dispatch
- [ ] AGENT_STATE.md updated; seam-prefixed tags

## Out of scope (explicit non-goals — brief §7)
- **No second node-type. No multi-node stitching.** (That is the NEXT PoC, and only after Matt passes this one.)
- **No fight execution.** Footprint + spawns are PRESERVED, not run. The fight need not initialize entity state.
- **No register/band-laddering.** Cathedral register held CONSTANT — spatial coherence is the only variable under test.
- **Do NOT canonicalize the larger architecture** (From JSON to Seasons + katabasis) — recognition → validate → commit; this PoC is the validation step.
- **Do NOT pre-write/impose the node schema** — it co-emerges from the authored node (§5).
- **No engine/telemetry/export changes** — `arena_scenarios.json` is consumed read-only.

## Open questions for the agent to resolve (document the decisions)
- Which `arena_scenarios.json` clear-room shell (knight-rider leans `elite_pack`; justify the pick)?
- Which Synty dungeon kit + native grid size (Dungeon Pack 5m vs Build 2.0 2.5–3m), and the chosen orientation indices for walls/door/stair?
- Outer/visual-footprint extent + annulus band dimensions vs the playable footprint?
- Entrance/exit socket grid coordinates + orientations?
- Final shape of the first-draft node schema (which §5 fields the node confirmed, which it extended, which proved unnecessary)?

## Process note — Gate-1 (pre-fire) disposition
knight-rider assessed jack-ryan DESIGN-MODE Gate-1 as **NOT required to publish this dispatch**: it authors no engine code, no telemetry/fixture-dict/decisions-log change, and the design-side review is already carried by gandalf's authoritative brief (gandalf is the requester + design steward). Per knight-rider OP, jack-ryan is invoked for ADR/decisions-log/cross-seam-schema/discipline-risk work — none present here. The node schema is an explicitly-non-canonical PoC draft. If gandalf or Matt wants jack-ryan's process eyes on the build loop regardless, that is a one-line add. Gate 2 (galadriel) and Gate 3 (Matt) are the binding gates for this PoC; jack-ryan's QA gate would attach later IF/WHEN the method graduates toward canonicalization.

## References
- gandalf brief: `agentic_orchestration/gandalf/notes/2026-06-19-crypt-vault-node-poc-brief.md` (AUTHORITATIVE)
- MCP smoke-test: `agentic_orchestration/legolas/research/2026-06-19-godot-mcp-comparison/smoke-test-result.md`
- Decoupling (annulus / parity / load-path): `canonical/story/battle-room-presentation-decoupling-2026-06-15.md`
- Register (cathedral / lift recipe): `canonical/story/style-register.md`
- Proven dual-gate loop precedent: `agentic_orchestration/gandalf/notes/2026-06-17-descent-runtogreen-log.md`
- Clear-room shells: `reincarnated-godot/data/arena_scenarios.json`
- galadriel CV instruments: `agentic_orchestration/galadriel/pipeline/{register-metrics,lifecycle-score,arch-grammar-band-probe}.mjs`
- cathedral recipe scene: `reincarnated-godot/scenes/dark_fantasy_cathedral.tscn`; lift recipe: `reincarnated-godot/scenes/lift_render.tscn`
