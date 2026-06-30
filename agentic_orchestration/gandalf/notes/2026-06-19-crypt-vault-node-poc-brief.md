# Crypt-Vault Node — Vignette PoC Brief

**Status:** ACTIVE — first node-authoring PoC of the "From JSON to Seasons" pipeline
**Author:** gandalf (design steward), Pattern B dialogue with Matt, 2026-06-19
**Matt go:** given 2026-06-19 ("ok, let's give it a shot")
**Tool:** satelliteoflove/godot-mcp v4.0.1 — VALIDATED (see `legolas/research/2026-06-19-godot-mcp-comparison/smoke-test-result.md`)
**Cross-refs:** `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` (sim-invariant/presentation decoupling, annulus rule, 35/35 parity); `canonical/story/style-register.md` (cathedral register, lift recipe); `agentic_orchestration/gandalf/notes/2026-06-17-descent-runtogreen-log.md` (proven dual-gate loop)

---

## 1. What this PoC proves

That the **author-in-MCP, structure-first, three-gate method produces a coherent, composable NODE that passes Matt** — fixing the spatial-coherence failures that the prior open-loop snapshot-scoring loop shipped (overlapping crypts, half-hidden doors, floating/clipping floors, reasonless walls).

It is a **vertical slice of ONE node-type** (architected-dungeon clear-room). Passing it validates the method that the Template Library (Layer 2) will scale across node-types. **No second node-type, no multi-node stitching, no fight execution until this passes Matt.**

## 2. The unit — a NODE, not a one-off room

Per the Q1/Q2 convergence (whole-room-vs-camera-angle + Act-Graph-unit-of-space): the unit of authoring, judgment, AND the Act Graph schema is the **node**, defined precisely as:

> a **presentation-room sized to *contain* its fight footprint (sim-invariant), with sockets to stitch to neighbors.**

A pretty standalone room is NOT a node — it doesn't compose into an act. The PoC authors a real node so it proves the production unit.

## 3. PoC target spec — architected-dungeon CLEAR-ROOM node

- **Theme:** crypt-vault.
- **Node-type:** architected-dungeon **clear-room** (NOT boss-arena — clear-rooms are the act's most common node, so proving one generalizes furthest and exercises socket-stitching).
- **Register:** the **proven cathedral register held CONSTANT** (lift recipe baseline). Spatial coherence is the ONLY new variable under test; do not introduce band/register-laddering here.
- **Structure (GridMap, snap-to-grid):** walls, door, floor, and ONE stair-and-mezzanine vertical element. The door is a wall-variant cell on the shared grid (cannot be half-occluded by construction).
- **Large assets:** **3–4 grid-snapped sarcophagi**, deliberately placed — the direct rebuke to the ~50-overlapping-crypts failure. Large architectural pieces are STRUCTURE (grid-placed, few), NOT dressing.
- **Dressing (ProtonScatter):** small organic clutter only (rubble, candle-stubs) — where overlap doesn't read as wrong.
- **Sockets:** defined entrance + exit socket positions/orientations on the grid (proves composability even though the PoC connects to nothing).
- **Fight footprint:** sized around a **real non-boss clear-room shell from `reincarnated-godot/data/arena_scenarios.json`** — drax selects a representative clear-room scenario; preserve its playable footprint + spawn markers at parity (annulus rule per the decoupling doc). The fight need not RUN; the footprint + spawns must be preserved within the room.
- **Kit/grid:** Synty dungeon kit at its native grid (Dungeon Pack 5m / Build 2.0 2.5–3m). **Lock grid-per-kit BEFORE placing cells**; build the MeshLibrary from the kit at native grid.

## 4. Three-instrument judgment (in order)

**Gate 1 — Structural (camera-INDEPENDENT, deterministic, via MCP engine-truth).** The new, load-bearing gate — the one that would have caught every prior failure with no camera at all:
1. No structure-on-structure AABB overlaps (walls/door/floor/stair/sarcophagi) — via `godot_scene3d get_spatial_info` + interval-intersection.
2. All GridMap cells valid; door = wall-variant on shared grid.
3. A* passability: entrance socket → exit socket reachable on the floor.
4. Vertical navigability: mezzanine reachable via the stair; clearance passable (no mid-character floors).
5. Fight-spawn parity: chosen shell's spawns + footprint preserved (annulus rule).

**Gate 2 — Register (multi-angle CV, galadriel).** Holds the proven cathedral register across SEVERAL framings (not one hero shot). HFD/LMV/LDR/SAT/HLF within the band the cathedral hit.

**Gate 3 — Coherence (Matt).** Orbit render set + walk-through if feasible. NEVER a single camera angle (that is the trap that shipped the broken scene). Matt judges: walls reasoned, doors working, floors coherent, dressing non-repetitive, "a place a human built." **Matt's verdict + REASONS are calibration samples for the eventual automated coherence judge — this is the HITL investment that removes HITL later.**

Note: single camera angles are permitted ONLY as a fast inner-loop instrument for the register dimension during iteration — never as the acceptance unit.

## 5. Schema co-emergence (substrate-led)

Do NOT pre-write the Act Graph node schema. Author this node, and let **what it actually needs** define the first-draft node schema (node_type, footprint, fight_shell_ref, sockets[], meshlibrary_ref, register_preset, grid_size, vertical_layers, dressing_rules — confirm/extend from the real authored node). The PoC deliverable INCLUDES this first-draft schema, derived from the node, not imposed on it.

## 6. Build sequence (knight-rider sequences; seam roles)

1. **drax** — enable the MCP plugin in a DELIBERATE, diff-reviewed commit (friction #4: plugin-enable mutates project.godot and dropped an unrelated config block in the smoke-test — verify the diff). Build GridMap node + MeshLibrary; place fight footprint + spawns; author structure-first; place sarcophagi grid-snapped; scatter clutter. Run Gate 1 (he has the MCP engine-truth tools).
2. **galadriel** — Gate 2 multi-angle register CV. (Concurrency: MCP port 6550 is single-client — drax authors, THEN galadriel judges; or galadriel as sub-agent inheriting drax's connection. Friction #7.)
3. **gandalf** — rule to green across Gates 1+2; surface to Matt.
4. **Matt** — Gate 3 coherence. Iterate on his reasons. No scale until his pass.

## 7. Non-goals

- No second node-type; no multi-node stitching (that's the next PoC).
- No fight execution (footprint + spawns preserved, not run).
- No register/band-laddering (cathedral register held constant).
- Do NOT canonicalize the larger architecture (From JSON to Seasons + katabasis) until this PoC validates the method — recognition → validate → commit.

## 8. Operational friction carried from the smoke-test (load-bearing)

- Structure-first is **tool-enforced**: GridMap cells are base64 in the `.tscn` and cannot be hand-edited — ALL cell placement goes through `godot_gridmap_edit`. (Happy alignment.)
- GridMap orientation is an index 0-23 (24 orthogonal rotations), not Euler.
- `get_scene_tree` is unbounded — pass `max_depth`/`max_children`; prefer `godot_scene3d get_spatial_info` with filters for spatial work.
- Full friction list: `smoke-test-result.md` §"Setup friction".
