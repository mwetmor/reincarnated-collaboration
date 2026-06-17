# Research — Modular Procedural Dungeon/Biome Assembly for Godot

**Authored by:** legolas (Mode A — analytical research)
**Persisted by:** gandalf (commissioner) — legolas delivered as text per the subagent-returns-text OP rule; persisted here so the research record survives.
**Date:** 2026-06-17
**Commission brief:** `agentic_orchestration/gandalf/notes/2026-06-17-legolas-modular-procgen-godot-research-brief.md`
**Companion:** `canonical/story/battle-room-presentation-decoupling-2026-06-15.md`
**Sources:** 30+ URLs accessed 2026-06-17; listed in §6.

---

## 1. The governing frame (for downstream readers)

Two layers, never conflated:

- **FIGHT layer** — spawn positions, playable footprint, damage geometry. Owned by reincarnated-engine (rocket). Not a procurement target here.
- **PRESENTATION-ASSEMBLY layer** — given a footprint spec handed down by the engine, assemble and dress a visually varied modular world around that fixed fight. This is the target.

**The disqualifying pattern:** any tool that insists on generating its own layout and cannot be driven by an external spec recreates a two-sources-of-truth conflict with engine authority. Every option below is evaluated against: *"Which layer does it serve, and can it subordinate layout authority to the engine's spec?"*

---

## 2. Summary (5 sentences)

The Godot 4 open-source ecosystem has at least three strong candidates for the PRESENTATION-ASSEMBLY layer that do not seize layout authority: the native GridMap `set_cell_item()` API (the purest engine-authority-respecting substrate — zero layout logic of its own), SimpleDungeons (room-prefab placement via DOOR-annotated scenes, architecture compatible with externally-constrained room selection, CC0 licensed), and godot-constraint-solving WFC (a constraint-satisfaction solver with a Preconditions API that accepts pre-populated cells as hard invariants). The third-party commercial market for Godot-native dungeon generators is thin and currently dominated by layout-owning tools: the most-visible paid generator (Fast Dungeon Generator) disqualifies on engine-authority grounds — it cannot consume an external footprint. Synty's Godot coverage has matured: Dungeon Pack (Godot 4.5.1+), Dark Fantasy (Godot 4.6.2+), and Fantasy Kingdom (Godot 4.5.1+) all ship native Godot projects with true modular building systems on a 2.5m/5m grid, giving strong dungeon-biome asset coverage; outdoor Nature Biomes packs mostly lack native Godot support and require FBX + community converter. Genre prior art (Dead Cells, Spelunky, Diablo 1) uniformly validates the hybrid model — hand-authored room templates, externally-specified graph, algorithm selects and places — which maps directly onto the engine-authority architecture, with Dead Cells being the closest structural analog for a spec-driven ARPG.

---

## 3. Options matrix

### Category 1 — Godot generation frameworks and codebases

| Option | Layer served | What it actually does | Godot 4.x compat | License | Cost | Integration path to external spec | Engine-authority-fit verdict |
|---|---|---|---|---|---|---|---|
| **godot-constraint-solving** (AlexeyBond/godot-constraint-solving) | PRESENTATION-ASSEMBLY (tile placement) | WFC + generic CSP solver. Populates TileMapLayer or GridMap by adjacency rules learned from sample maps. Backtracking, multithreading. **Preconditions API accepts pre-populated cells as hard constraints.** v1.7, Oct 2024. | Godot 4 confirmed | MIT | Free | Pre-populate GridMap cells from engine spec; WFC fills remainder respecting hard constraints. Direct injection of engine-specified invariant cells. | **PASS — strong.** Hard-constraint API is the exact mechanism needed. Layout authority is shareable. Note: documentation conflict on 3D GridMap status ("not yet implemented" in one field vs GridMap listed as target node) — requires one integration test against v1.7 to resolve. |
| **Fast WFC (C++ port)** (Asset Library #4149) | PRESENTATION-ASSEMBLY (tile placement) | C++ port of mxgmn's WFC. Tiling + overlapping modes. Fastest WFC in Godot 4. Updated Mar 2026. Godot 4.4+. | Godot 4.4+ | MIT | Free | No documented preconditions/constraint-injection API. Tile-choice authority is internal. | **CONDITIONAL.** Best pure performance. Viable only if external spec seeds the MeshLibrary pool but not cell positions. Lower engine-authority confidence than godot-constraint-solving. |
| **WFC 2D/3D Generator (C#)** (Asset Library #2473) | PRESENTATION-ASSEMBLY (tile placement) | C# WFC; TileMap + GridMap; multi-threaded; fail correction. Dec 2024. Godot 4.2+. | Godot 4.2+ | MIT | Free | Sample-driven; no documented external constraint injection API. | **CONDITIONAL.** Requires C# in project. Sample map could be procedurally authored from engine spec — indirect path. No preconditions API documented. |
| **SimpleDungeons** (majikayogames/SimpleDungeons) | PRESENTATION-ASSEMBLY (room placement) | Prefab-room 3D dungeon generator. Rooms = Godot scenes with DOOR-prefixed Node3Ds as connection points. Algorithm places and connects rooms. V2: define individual rooms (no "dungeon kit" abstraction). GDScript. CC0. | Godot 4 confirmed | CC0 (public domain) | Free | Room pool = the control point. Engine spec constrains which room scenes are eligible per graph node. Whether DungeonGenerator accepts pre-ordered external graph is unconfirmed — requires wiki/source review. CC0 means any fork is unrestricted. | **CONDITIONAL — strong candidate.** Room-pool architecture is compatible with engine authority. Gap: confirmation of external-graph-driven mode needed. CC0 removes all IP risk. |
| **godot-procedural3d** (RodZill4) | FIGHT+ASSEMBLY overlap (disqualify) | Generates 3D dungeon scenes autonomously from modular assets. "Generate/Stop/Clean" UI. Internal layout authority. MIT. | Godot version unclear (likely 3.x lineage) | MIT | Free | No external spec path found. Autonomous generation. | **DISQUALIFY.** Owns layout. Engine version unclear. |
| **GDQuest procedural gen demos** (gdquest-demos/godot-4-procedural-generation) | PRESENTATION-ASSEMBLY (reference) | RandomWalker (chunk placement), BSP rooms, WorldMap, ModularWeapons, Infinite World. Godot 3 + 4 branches. | Godot 4 branch exists | Not confirmed (LICENSE file present) | Free | RandomWalker demo places hand-designed chunks on a random walk — closest illustration of the hybrid model. Not a library; reference implementations only. | **REFERENCE ONLY.** Not deployable framework. RandomWalker is the clearest Godot 4 illustration of the engine-spec + chunk-placement pattern. |
| **Cyclic dungeon generation / Ludoscope** (Dormans/Unexplored) | FIGHT layer (layout/mission-graph generation) | Grammar-rule transformational system for cyclic dungeon mission graphs. Generates layout topology, not visual assembly. Proprietary academic tool. No Godot port found. | None | Proprietary | N/A | Academic concept only. | **OUT OF SCOPE (FIGHT layer) + unavailable.** Generates layout — engine's domain. No Godot implementation exists in the open-source ecosystem. Conceptually valuable for understanding cyclic graph design but not a procurement option. |

### Category 2 — Purchasable Godot procedural packs

| Option | Layer served | What it actually does | Godot version | License / commercial | Cost | Integration path to external spec | Engine-authority-fit verdict |
|---|---|---|---|---|---|---|---|
| **Canopy Games Dungeon Kit** (canopygames.itch.io) | PRESENTATION-ASSEMBLY (art + pre-built GridMap) | 18 GridMap-ready room pieces + 61 props (.tscn files). Pre-configured GridMap scene included. | Godot 4 (sub-version unconfirmed); user reports Godot 4.5 compat issues ~146 days before research | Commercial terms NOT SPECIFIED on page | $10 USD minimum | GridMap API: external code calls `set_cell_item()` with engine spec. Clean path once in MeshLibrary. | **CONDITIONAL.** GridMap-ready is the right form. But: (a) Godot 4.5 compat unresolved, (b) commercial license unknown — must confirm, (c) visual register NOT Synty POLYGON — mixing would break register cohesion. Only viable if used as standalone, not alongside Synty packs. |
| **Fast Dungeon Generator** (creative-core-studio.itch.io) | FIGHT+ASSEMBLY overlap (disqualify) | Room-and-corridor placement algorithm generating full 3D geometry. Emits `map_generated` signal with grid data post-generation. MultiMesh, lighting, collision. | Godot 4.x | Commercial terms NOT confirmed | Not confirmed | Cannot consume external footprint. Owns layout fully. Grid data emitted as output after generation — not injectable. | **DISQUALIFY.** Layout ownership is total. `map_generated` signal is output, not input. Cannot be driven by engine spec. |
| **Dungeon Modular** (loafbrr.itch.io) | PRESENTATION-ASSEMBLY (art assets) | Brick dungeon modular pieces on 0.25m grid. Godot + Unity + Blender. Sep 2025 Godot release. | Godot (exact version unconfirmed) | Not confirmed | $9 USD+ | Geometry pieces; external code drives placement via GridMap or scene instancing. | **NEEDS VERIFICATION.** 0.25m grid is very fine — likely does not align with Synty's 2.5m/5m grid. Register compatibility with Synty POLYGON unknown. Low priority to investigate unless non-Synty path chosen. |

### Category 3 — Synty POLYGON modular packs across biomes

#### Godot support status (2026-06-17)

Synty now ships native Godot project files for 16 packs at syntystore.com/collections/godot-asset-packs. All require Godot 4.5.1+ or 4.6.2+ depending on the pack. A community converter (DeniedWorks/synty-godot-converter, v2.4 Feb 2026) converts `.unitypackage` to Godot 4.6 for packs without native Godot projects. A community import guide (tctimmeh/synty-in-godot, tested Godot 4.2) covers Dungeon Pack, Fantasy Kingdom, Dungeon Realms, Dungeon Map. A CC0 tree shader for Synty Biomes in Godot exists (godotshaders.com, xtarsia, Mar/Dec 2024) — trees only, not the full Biomes material set.

#### Biome modularity classification

**Synty's Build 2.0 grid system:** 2.5m horizontal / 3m vertical for Build 2.0 packs. Dungeon-specific packs use 5m × 5m. Note: gamedevbits.com spec page notes "Currently Unity only" for Build 2.0 shader — the grid dimensions are geometry-based and transfer to Godot, but shaders require porting.

| Pack | Price | Biome/Theme | Modular building coverage | Godot native | Modular type | Notes |
|---|---|---|---|---|---|---|
| **POLYGON Dungeon Pack** | $149.99 | Fantasy dungeon interior (castle, cave, goblin camp, basement, sewer — 5 interior types) | 770 assets: 17 floor types, 7 stair types, 10 doors, 23 pillars, raised rock platforms, modular interior sets per theme | Yes (Godot 4.5.1+, v1.0.1) | True modular tiling (5m grid) | Widest interior biome variety per pack. Dark Fantasy-adjacent register. Community import scripts tested. |
| **POLYGON Dungeon Realms** | $199.99 | Multi-area dungeon (Hell, Forge, Dunes — 3 distinct areas) | 1,118+ prefabs: walls, towers, tiles, stairs, pillars, bridges, arches, tents, fully modular | No native Godot (FBX + community converter required) | True modular tiling | Greater breadth than Dungeon Pack. No native Godot project — gap in the pipeline. |
| **POLYGON Dark Fantasy** | $199.99 | Gothic/dark fantasy (exterior + interior, nightmarish register) | 600+ prefabs: walls, windows, floors, doors, pillars, ruins, trims, roofs, stairs, alcoves, buttresses, spires, archways, railings, bridges, beams | Yes (Godot 4.6.2+) | True modular building system | Team's validated register-2 reference (boss-arena scorecard). Primary aesthetic anchor. |
| **POLYGON Fantasy Kingdom** | $349.99 | Medieval fantasy (castle exterior + enterable interiors) | 2,100+ prefabs: 600+ modular castle/house pieces (walls, windows, doors, staircases, pillars/beams, battlements, floors, roofs, spires, archways, chimneys, destroyed pieces) | Yes (Godot 4.5.1+, v1.0.0) | True modular building system (Build 2.0) | Widest piece count. Highest cost. Non-dungeon biome (above-ground castle). |
| **POLYGON Apocalypse Pack** | $349.99 | Post-apocalyptic | Semi-modular building chunks (not individual wall pieces) | Yes (Godot native, version unconfirmed) | Semi-modular (chunks) | Not a true wall-by-wall modular kit — assembly granularity is coarser. |
| **POLYGON Shops Pack** | $199.99 | Commercial/retail interior | Build 2.0 fully modular (2.5m/3m grid) | Yes (Godot native) | True modular (Build 2.0) | Urban interior; non-fantasy register. Cross-biome mixing with Dark Fantasy would require register gap analysis. |

**Outdoor/Nature Biomes — different modularity model.** These are prop/environment collections for terrain scatter, NOT grid-modular wall kits.

| Pack | Price | Biome | Godot native | Notes |
|---|---|---|---|---|
| POLYGON Meadow Forest | $54.99 | Woodland | No (Unity + Unreal only) | 79 env assets, 27 terrain materials. No grid snap. Prop scatter model. |
| POLYGON Tropical Jungle | Not confirmed | Jungle | Unconfirmed | Same model. |
| POLYGON Swamp Marshland | Not confirmed | Swamp | Unconfirmed | Same model. |
| POLYGON Alpine Mountain | Not confirmed | Alpine | Unconfirmed | Same model. |
| POLYGON Nature Biomes Season Two | Not confirmed | Arid Desert, Enchanted Forest, + 1 | Unconfirmed | Same model. |

**Key gap:** Synty outdoor/nature biomes mostly lack Godot native support. The outdoor-zone architecture path (for seasonal biome variety) requires either FBX import + DeniedWorks converter or a decision to use different outdoor asset sources for Godot.

#### Synty commercial licensing (summary)

One-Time Purchase grants perpetual rights to purchased packs. 5 seats per single-quantity purchase. Royalty-free for commercial release (standard for the Synty EULA — but the full text at syntystore.com/pages/one-time-purchase-licence MUST be read before any commercial release, especially to verify engine-portability terms now that Godot is a native target).

### Category 4 — Native Godot assembly substrate and integration patterns

#### GridMap + MeshLibrary

Godot's built-in 3D tiling system. A sparse octant-based grid where each cell holds a MeshLibrary integer index + an orientation (0–23, covering all 24 discrete rotations). The critical runtime API:

```gdscript
gridmap.set_cell_item(
    Vector3i(x, y, z),  # grid coordinates
    item_index,          # MeshLibrary integer index; -1 clears cell
    orientation          # 0–23
)
```

This is the direct engine-authority integration point: the engine emits a room footprint as a JSON/dict of (grid_x, grid_y, grid_z, tile_type, orientation); Godot code maps tile_type to a MeshLibrary index and calls set_cell_item for each cell. The GridMap has zero layout logic — it is a pure assembly substrate. MeshLibrary must be pre-populated with Synty modular pieces (editor work: drag MeshInstance3D nodes into the library). cell_size must match the Synty pack's grid (set to Vector3(2.5, 3.0, 2.5) for Build 2.0 packs; Vector3(5.0, ..., 5.0) for Dungeon Pack — verify against actual geometry). Built-in: collision (StaticBody3D per MeshLibrary item), navigation mesh (NavigationRegion3D per item), octant-based rendering optimization.

**The hybrid stamp pattern in Godot** (Dead Cells model): rooms are `.tscn` scenes pre-built with full GridMap tiles + props + lighting + nav. Assembly code places scenes at world offsets computed from door positions. Engine graph spec drives scene selection. Short corridor stamps connect rooms at door seams. Optional WFC pass (godot-constraint-solving) fills tile-variation at seams.

#### ProtonScatter (organic prop dressing)

HungryProton/scatter, MIT, Godot 4.x (completely rewritten for v4). Modifier-stack (Blender-style) scatter system: Box, Sphere, Path shapes. Places prop instances within defined areas. Standard Godot 4 answer for organic dressing density — rubble, foliage, rock scatter. Not a layout generator; places within a defined area, respects collision. Integration with the annulus dressing model (`canonical/story/battle-room-presentation-decoupling-2026-06-15.md §2`): ProtonScatter fills the annulus ring using a Path or Box shape bounded by the engine's playable footprint edge and the visual footprint outer edge. Zero layout authority.

#### Terrain3D (outdoor biome substrate)

TokisanGames/Terrain3D, MIT, Godot 4 C++ GDExtension, v1.0.2-stable (May 2026). Heightmap import from Gaea, World Creator, World Machine, Unity, Unreal, HTerrain. Programmatically accessible from GDScript, C#, any Godot-supported language. Separates terrain sculpting from foliage instancing (10 LOD levels for both). Engine can provide heightmap data; Terrain3D renders the terrain surface. For outdoor zones: engine provides biome type + zone boundary + optional heightmap seed → Terrain3D sculpts base terrain → ProtonScatter/Terrain3D foliage places props. Playable footprint remains the engine's specification. Engine-authority fit: **PASS**.

### Category 5 — Genre / design prior art

#### Module granularity comparison

| Game | Granularity | Hand-authored elements | Procedural elements | Key lesson |
|---|---|---|---|---|
| **Diablo 1** | 40×40 tile floor plan; minisets (typically 3×3); set-pieces (verbatim pastes) | Set pieces (quest rooms); miniset patterns; theme room object arrangements; 4 distinct per-zone algorithms | Room topology (recursive per zone type); corridor paths; tile substitutions | Two-stage pipeline: predungeon (walkability map, purely algorithmic) then dungeon (tile + visual selection). Separation lets you tinker floor plan independently from tile choice. Pattern-matching find/replace (minisets) handles seams, fixups, erosion, and authored content with one mechanism. |
| **Spelunky** | 4×4 grid of 10×8 tile rooms; chunk zones within rooms marking randomizable sub-regions | All room templates (10×8 char maps); chunk options per zone | Solution path through 4×4 grid; chunk selection within marked zones; path direction algorithm | Fixed grid topology ensures solvability; variation is within rooms not between them. The 4×4 grid IS the external spec — every run has the same grid structure, different room fills. |
| **Dead Cells** | Room-sized templates (variable per biome) | Room templates (biome-specific); level graph (biome-specific pacing spec: length, special rooms, labyrinth density, entrance/exit spacing) | Room selection per graph node; enemy quantity + type combos; loot distribution | Six-step process. The level graph is a "set of instructions to the algorithm" — exactly the engine-spec model. Both room templates AND graph are biome-specific, enabling strong biome identity. Biome-exclusive rooms are the design principle preventing cross-biome visual leakage. |
| **Hades** | Room-sized scenes (per biome pool) | Full room scenes (art + encounter, fully hand-crafted); world topology; narrative beat rooms; boon/shop positioning | Run sequence and room selection from pool | Extreme authored end of the spectrum. Procedural = sequencing only. The "hybrid" here is structural (authored rooms) + procedural (order). High per-room polish possible because room count is bounded. |
| **Unexplored** | Mission-graph nodes (Ludoscope grammar rules) | 5,000+ find/replace grammar rules; cyclic loop topology structure | Graph transformation (dungeon-whole and per-level floor plan); specific graph instantiation | The algorithm is the rules, not the output. High authored investment in rule design; the generation is powerful but opaque to players. Not a practical model for small teams without Dormans-level research investment. |

**Granularity fit for a spec-driven ARPG (our context):** Dead Cells is the closest model. The engine spec IS the level graph. Room templates are the authored layer (Drax's work). The algorithm selects and places — SimpleDungeons is the architectural analog.

#### Named anti-patterns

**Diablo IV "cookie cutter" dungeons:** Blizzard used templates with randomized attachment locations and hallway lengths. Critical reception: layouts read as rotated/resized instances of the same template. Root cause: variation confined to parameterization of fixed templates (length, attachment point) rather than topological variety. Players recognize the algorithm. Lesson: variation must occur at topology level, not just within a template's parameters. A larger pool of distinct room templates + graph-level variety (not just room-level) prevents this.

**No Man's Sky launch (2016) — technically infinite, experientially empty:** 10 variations × 6 parameters = technically distinct per combination but experientially indistinct because the authored layer was shallow. Players recognize the pattern space rather than discovering a world. Root cause: procedural surface masking a shallow authored substrate. Lesson: authored anchors (set pieces, biome-defining structures, named locations) break pattern recognition. The procedural layer must have something authored to assemble *around* — not just vary in isolation. Hello Games later partially addressed this with biome-themed world types.

**Pure-noise soullessness:** when no authored anchor exists, players recognize the algorithm not the world. Set pieces, boss chambers, authored rooms, narrative beats are the anchors. The authored element is what makes random structure feel discovered.

#### Outdoor biome vs enclosed dungeon — different problem shapes

Enclosed dungeon: topology (which rooms connect) + seam integrity (doors align, corridors span). Playable footprint is fixed, small, bounded. GridMap is the natural substrate. Assembly algorithm is graph-driven.

Outdoor zone: no hard topology constraint. Challenge is density, visual identity, navigability across continuous space. Substrate shifts to Terrain3D (heightmap base) + ProtonScatter (prop density). The "room" concept dissolves into zones and waypoints. Engine's footprint spec becomes a spatial zone boundary + heightmap seed, not a cell grid.

Both exist in the seasonal-journey structure. They require different substrates but the same engine-authority principle: engine specifies invariant; Godot dresses around it.

---

## 4. Top-3 candidates with reasoning

### Candidate 1 — Native GridMap + `set_cell_item()` (primary assembly substrate)

**What it is:** Godot's built-in 3D tiling system. Not a framework — the substrate itself.

**Why top-3:** It is the only option with zero layout authority of its own. The engine emits a cell-grid spec (tile type, position, orientation per cell); GDScript calls `set_cell_item()` to populate the GridMap. No intermediary owns layout decisions. A clean JSON → GDScript → GridMap pipeline is a few hundred lines of straightforward code. Built-in collision, navigation mesh, and octant-based performance optimization are included at no additional cost.

**Key setup requirements:** Synty modular pieces must be registered as MeshLibrary items (editor work — one-time per pack). Cell_size must match the pack's grid (approximately 2.5m for Build 2.0 packs; 5m for Dungeon Pack — verify against actual piece geometry). Once the MeshLibrary is populated, runtime assembly is fully code-driven.

**Limitation:** GridMap is structural — it does not handle organic prop dressing (ProtonScatter is the complement) or outdoor terrain (Terrain3D). A complete pipeline requires all three layers.

**Engine-authority verdict: PASS — strongest possible.** The GridMap is a pure receiver of external spec. No generation logic to bypass or override.

### Candidate 2 — SimpleDungeons (room-prefab assembly, CC0)

**What it is:** Godot 4 addon (GDScript, CC0) that places user-defined room scenes (.tscn) by matching DOOR-annotated Node3Ds at connection points. V2 API: define individual rooms; DungeonGenerator places and connects them.

**Why top-3:** The room-prefab architecture is the correct granularity for a Hades/Dead Cells-class ARPG. Each room scene is hand-authored (Drax or a level designer) with full visual dressing, lighting, and nav. The algorithm selects from the scene pool and places rooms by door matching. The pool is the control point: the engine's graph spec constrains which room types are eligible at each node position, which is how engine authority flows in — even if the internal graph growth is currently SimpleDungeons-owned.

**Gap to address:** whether DungeonGenerator can accept a pre-ordered list of room types (from an external engine graph) rather than growing the graph internally requires reading the v2 API wiki (github.com/majikayogames/SimpleDungeons/wiki — requires cloning the repo). If not natively supported, CC0 license means any fork or wrapper is unrestricted. Architectural compatibility with engine authority is clear; API confirmation is a short code review.

**Engine-authority verdict: CONDITIONAL — strong candidate.** Architecture is compatible; API confirmation is the one open question. CC0 removes all licensing risk.

### Candidate 3 — godot-constraint-solving WFC (AlexeyBond) as seam-filling complement

**What it is:** WFC + constraint-satisfaction solver for Godot 4 (MIT, v1.7 Oct 2024). Populates GridMap or TileMapLayer. Key differentiator: **Preconditions API accepts pre-populated cells as hard constraints** — the solver fills around them.

**Why top-3:** This is not a layout generator in the disqualifying sense — it is a constraint-satisfying *dressing* tool. The engine spec locks structural tiles (walls, floor, door seams, spawn-adjacent cells) as hard constraints; the WFC fills the remainder with tile variations that respect adjacency rules. This maps directly onto the Diablo 1 miniset pattern: authored elements are invariant anchors; the algorithm handles the seams and transitions between them, preventing the "same tile repeated" read at connection points.

**Primary use:** corridor seam filling and tile-variation pass after GridMap structural assembly. A secondary use is generating tile-dressing variation within the annulus region (the impassable ring around the playable footprint per the decoupling canonical doc).

**Limitation to test:** documentation conflict on 3D GridMap support ("not yet implemented" in one field vs GridMap listed as target node type). Requires one integration test against v1.7 to resolve — a short check, not a research question.

**Engine-authority verdict: PASS.** Preconditions API is the exact mechanism that lets engine spec cells be invariant anchors. The WFC defers to those anchors.

---

## 5. Knowledge gaps not resolved (cheap spikes, NOT research questions)

1. **SimpleDungeons v2 external-graph API:** whether DungeonGenerator accepts a pre-ordered external graph (room type sequence) rather than growing one internally. Requires cloning the repo and reading the v2 wiki.
2. **godot-constraint-solving 3D GridMap support in v1.7:** the documentation conflict. One integration test resolves this.
3. **Synty outdoor Nature Biomes Godot native support:** Meadow Forest confirmed Unity/Unreal only. Jungle, Swamp, Alpine, Desert, Enchanted Forest native Godot status unconfirmed. DeniedWorks converter likely covers them but unconfirmed on the Biomes series.
4. **Synty POLYGON Dungeon Pack cell_size in Godot project:** the 5m grid is Unity-sourced; the Godot project's actual cell geometry needs verification on import.
5. **Synty Dark Fantasy grid dimensions:** modular building confirmed but grid spec not extracted. Required for GridMap cell_size matching.
6. **Synty EULA full commercial terms:** not fetched (landing page redirected). Must be read before any commercial release — especially the engine-portability clause now that Godot is a native target.
7. **Canopy Games Dungeon Kit commercial license:** itch.io page did not specify commercial use terms.

---

## 6. Source list

All accessed 2026-06-17.

**Godot frameworks / addons:**
- godot-constraint-solving: https://github.com/AlexeyBond/godot-constraint-solving
- Fast WFC (Asset Library #4149): https://godotengine.org/asset-library/asset/4149
- WFC 2D/3D Generator (Asset Library #2473): https://godotengine.org/asset-library/asset/2473
- SimpleDungeons: https://github.com/majikayogames/SimpleDungeons
- godot-procedural3d: https://github.com/RodZill4/godot-procedural3d
- GDQuest procedural gen demos: https://github.com/gdquest-demos/godot-4-procedural-generation
- ProtonScatter: https://github.com/HungryProton/scatter
- Terrain3D: https://github.com/TokisanGames/Terrain3D
- GridMap API (Godot 4.4 docs): https://docs.godotengine.org/en/4.4/classes/class_gridmap.html
- GridMap tutorial (Godot stable): https://docs.godotengine.org/en/stable/tutorials/3d/using_gridmaps.html

**Purchasable packs:**
- Canopy Games Dungeon Kit: https://canopygames.itch.io/dungeon-it
- Fast Dungeon Generator: https://creative-core-studio.itch.io/godot-4-fast-dungeon-generator

**Synty POLYGON:**
- Godot collection: https://syntystore.com/collections/godot-asset-packs
- Dungeon Pack: https://syntystore.com/products/polygon-dungeon-pack
- Dungeon Realms: https://syntystore.com/products/polygon-dungeon-realms
- Dark Fantasy: https://syntystore.com/products/polygon-dark-fantasy
- Fantasy Kingdom: https://syntystore.com/products/polygon-fantasy-kingdom
- Meadow Forest: https://syntystore.com/products/polygon-meadow-forest-nature-biome
- Licenses overview: https://syntystore.com/pages/licences-overview
- Build 2.0 grid specs: https://gamedevbits.com/syntyspecs/
- synty-in-godot: https://github.com/tctimmeh/synty-in-godot
- synty-godot-converter: https://github.com/DeniedWorks/synty-godot-converter
- Synty Biomes tree shader: https://godotshaders.com/shader/synty-biomes-tree-compatible-shader/

**Genre prior art:**
- Diablo 1 dungeon generation: https://www.boristhebrave.com/2019/07/14/dungeon-generation-in-diablo-1/
- Dead Cells hybrid approach: https://deepnight.net/tutorial/the-level-design-of-dead-cells-a-hybrid-approach/
- Dead Cells / Edgar (Unity example): https://ondrejnepozitek.github.io/Edgar-Unity/docs/examples/dead-cells/
- Spelunky PCG Wiki: https://procedural-content-generation.fandom.com/wiki/Spelunky
- Unexplored cyclic generation: https://www.gamedeveloper.com/design/unexplored-s-secret-cyclic-dungeon-generation-
- Unexplored generation (BorisTheBrave): https://www.boristhebrave.com/2021/04/10/dungeon-generation-in-unexplored/
- Diablo IV dungeon criticism: https://www.pcgamesn.com/diablo-4/repetitive-dungeons-beta-blizzard-rpg-game
- No Man's Sky procedural gen analysis: https://www.davideaversa.it/blog/procedural-generation-post-no-mans-sky-era/

---

**Commission complete.** Options + fit, with the engine-authority layering verdict explicit per option. NOT an adoption call — the team decides.
