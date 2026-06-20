# Research — ARPG Room Sizing, Monster Density, Ravine Layouts, Procedural Methods — 2026-06-20

**Mode:** A (analytical)
**Commissioner:** gandalf (design steward)
**Commission context:** Replace arena-inherited 28×28 tile room size with genre-canonical evidence. Deliverable is a sizing+density table plus ravine/canyon layout conventions and a procedural-method survey. For the enchanted-forest-ravine combat zone (2×2 square tile map).
**Sources consulted:** lootcube.net zone pages, boristhebrave.com (D1 dungeon gen + WFC tips), d2mods.info Phrozen Keep, diablo2.io, theangrygm.com, book.leveldesignbook.com, gridbugs.org, purediablo.com, purediablo.com randomization article, runicgames.com TL2 Q&A, PoE ExileCon/Steam announcement, Wikipedia PoE procedural generation, research.library.northeastern.edu PCG thesis

---

## Section 1 — Sizing + Density Table (Q2 + Q3, load-bearing)

### 1a. Tile / dimension vocabulary first

Before numbers can be meaningful, the unit system must be established per game.

**Diablo 1 / 2 — tile grid units**
- A D2 "tile" (diamond-shaped isometric tile) = 160×80 px at original resolution. One tile subdivides into subtiles/cells of 36×18 px (5×5 subdivision grid per tile).
- The "grid unit" used in area-size databases (lootcube.net, Diablo Archive wiki) is this tile unit. So "80×80" means eighty tiles × eighty tiles in each axis.
- Real-world scale equivalent: no official statement found. Community modding discussion (Phrozen Keep) treats tiles as walkable position units; at a plausible character-height of ~1.8 m mapped to ~2 subtile footprint, one tile ≈ 2–3 m world-space. This is community-estimated, not Blizzard-documented. Use with caution.
- Characters and most monsters occupy an X-shaped footprint of 5 subtiles; elite packs occupy roughly that same scale per monster.

**Diablo 1 — absolute level grid**
- Every level fills a 40×40 tile master grid. Rooms are generated inside this grid.
- Cathedral spine rooms: ~10×10 tiles.
- Catacombs rooms: 4–9 tiles per side (min ~5×5, max ~12×14).
- Caves starting room: 2×2 tiles; recursive additions 3–4 tiles per side.
- Hell level rooms: 5–6 tiles per side; generated in a 20×20 sub-area then mirrored.
- Corridors in Catacombs: 1, 2, or 3 tiles wide (randomly chosen).
Source: boristhebrave.com primary analysis of D1 source code.

**Diablo 3 — tile = "chunk" or pre-designed room piece**
- D3 uses pre-authored "tile" pieces (rooms, corridors, transition connectors). The pieces are not a uniform grid cell; they are designer-sized chunks. Corridor connectors between room pieces run 3, 4, or 5 tiles wide. The tile units here are visual/spatial D3 units, not sub-tile walkability units.
- Exterior zones: static shell with "cut-out holes" of various shapes; multiple hand-authored pieces can fill each hole, chosen at runtime.
- D4 inherited this system but defaulted heavily to single-path tube layouts (player forum consensus: "big long 1-way tube with 1–2 junctions").
Source: purediablo.com randomization article; blizzard forum discussions.

**Path of Exile — zones are not grid-rooms**
- PoE does not use a room-grid like D1/D2. It uses pre-hand-designed tile pieces (walls, corridors, connectors, rivers) assembled semi-randomly per-zone via a layout grammar.
- The zone generation system (Rhys Abraham, ExileCon 2019) places hand-designed pieces and stitches them with procedural connectors. Rooms can overlap; custom rules resolve tile-key conflicts at seam edges. The system uses Wang-tile principles for ground textures (edge-color matching for seamless tiling), separate from the room layout grammar.
- No public tile-unit dimensional specification found. PoE's areas are perceived as larger than D2 equivalents and vary significantly by zone type.
Source: PoE Steam announcement (ExileCon dev diary), PoE forum procedural generation thread.

**Last Epoch**
- Dungeons: 3-level structure (2 combat zones + boss arena). Zone layouts procedurally generated; specific tile dimensions not publicly documented.

**Grim Dawn**
- "Passage"-type outdoor areas confirmed as design archetype (River Passage, The Flooded Passage). Specific tile dimensions not found in public technical documentation. Crate Entertainment has not published a level-design technical spec.

**Torchlight II**
- Outdoor areas fall into two types: Passes (linear connectors between overworld zones) and Overworld (larger open explorable areas). Passes are explicitly the narrow linear archetype. No specific tile dimensions documented publicly.
Source: runicgames.com Level Design Q&A.

---

### 1b. Diablo 2 zone sizing table — empirical from lootcube.net zone pages

All sizes in tile units (1 tile = 160×80 px isometric diamond; estimated ~2–3 m real-world but no official conversion found).

| Zone | Type | Map Size (tiles) | Elite Packs (Hell) | Est. Total Monsters (Hell) | Notes |
|---|---|---|---|---|---|
| Blood Moor | Outdoor open | 80×80 | 7–9 | ~37–65 | Act 1 connective area |
| Cold Plains | Outdoor open | 80×80 | 7–9 | ~35–49 | Act 1 open area |
| Stony Field | Outdoor open | 80×80 | 7–9 | ~28–61 | Act 1; low density perception per players |
| Spider Forest | Outdoor narrow corridor | 64×192 | 10–15 | ~90–163 | Act 3; 3:1 aspect ratio — canonical ARPG ravine/pass shape |
| Great Marsh | Outdoor narrow corridor | 64×192 | 10–15 | ~81–144 | Act 3; same shape as Spider Forest |
| Flayer Jungle | Outdoor narrow corridor | 64×192 | 10–15 | ~93–132 | Act 3; same shape as Spider Forest |
| Stony Tomb L1 | Indoor dungeon | 200×200 | 6–8 | ~205–376 | Acts 2; very large dungeon |

**Key pattern from the table:**
- D2 outdoor "open" areas: consistently 80×80 tiles.
- D2 outdoor "pass/corridor" areas: consistently 64×192 tiles — narrow (64 wide) and long (192). The 64 wide corridor accommodates the jungle tileset's 2-tile-wide river + alcoves on each side. This is the closest D2 has to a ravine/gorge archetype.
- The connective middle-ground zones (Blood Moor, Cold Plains) are NOT narrow; they are near-square open areas.
- Dungeon areas (Stony Tomb) run much larger (200×200) with more packed monster counts but similar or slightly lower elite-pack counts.

**Monster density per tile-area (approximation):**
- Outdoor 80×80 open zone: ~37–65 monsters / 6,400 tiles ≈ 0.006–0.010 monsters/tile
- Outdoor 64×192 corridor zone: ~90–163 monsters / 12,288 tiles ≈ 0.007–0.013 monsters/tile
- Dungeon 200×200 zone: ~205–376 monsters / 40,000 tiles ≈ 0.005–0.009 monsters/tile

Note: Not all tile space is walkable; open-area densities are similar across types because corridors concentrate walkable area differently from open squares.

---

### 1c. Per-game synthesis for "middle-room" sizing (Q2)

**Diablo 1:**
A typical non-boss catacomb room: 4–9 tiles per side (most commonly ~6×6 to 8×8). Hallways between rooms: 1–3 tiles wide. The entire dungeon level fits within 40×40 tiles.

**Diablo 2:**
No concept of "room" in outdoor areas — they are tile-grid zones placed by the engine. Indoor dungeon rooms ("maze tiles"): each room is uniform within its dungeon type, exact DS1 file dimensions not publicly documented (requires file inspection), but community understanding is ~10–20 tiles per side for catacomb-style rooms. Connective outdoor areas: 80×80. Pass/corridor zones: 64×192.

**Diablo 3:**
Room-sized pre-authored pieces. Connective corridors: 3–5 visual tiles wide. Room "nodes" where combat occurs: designer-sized but perceived as significantly larger than D1/D2 rooms — D3 expanded encounter spaces to allow more AoE combat with higher density trash.

**Diablo 4:**
Heavy tube layout tendency. Community consensus: dungeons feel like single-width corridors with occasional side branches. Width: 1-room wide (variable, but always linear). No documented tile-unit dimensions.

**Path of Exile:**
Open areas vary significantly — maps can feel quite large for endgame content. Campaign zones: moderate, semi-linear with branching. No documented tile-unit dimensions for rooms.

**Last Epoch:**
No documented room dimensions. Perceived as similar density to PoE.

**Grim Dawn / Torchlight II / Torchlight I:**
No public tile-unit room dimensions found. Grim Dawn outdoor passages (River Passage, Flooded Passage) function as linear corridor connectors — conceptually the same as D2's Spider Forest archetype. Torchlight II "Passes" are explicitly narrow linear zones.

---

### 1d. Monster archetype composition (Q3)

**Diablo 2 archetype taxonomy:**
- Normal (trash): forms in packs of 1–4 monsters per "group." Multiple groups per zone. These are the bulk of the monster count.
- Champion pack: 3–5 monsters of the same type with champion modifiers (health, speed, damage bonuses). Grouped under "elite packs" in game files.
- Unique pack (boss pack): 1 unique boss + 3–5 minions with inherited modifiers. Grouped with champions under MonUMin/MonUMax in game files.
- The MonUMin/MonUMax values in D2's game files = total elite+unique pack spawns, not just unique bosses. For most mid-game outdoor areas, MonUMin/MonUMax(Hell) = 7–9. The game also has a "MonDen" density value that gates whether the theoretical max is reached.

**D2 pack composition per zone encounter (mid-game outdoor, Hell difficulty):**
- Per zone (80×80): 7–9 elite packs (mix of champion + unique) + substantial trash filling ~37–65 total monsters
- A single encounter "pull" for the player: typically 1–3 trash groups (3–12 monsters) + incidentally 0–1 elite packs, depending on zone navigation
- Elite pack when encountered: 3–5 champion monsters OR 1 unique + 3–5 minions

**D2 pass/corridor zone (64×192), Hell:**
- 10–15 elite packs + ~90–163 total monsters across the whole corridor
- Higher absolute pack count because the corridor is 3× longer; density per walkable tile is similar
- Encounter rhythm: player moves linearly through the corridor, encountering clusters of trash with elite packs interspersed roughly every 10–20 tiles of travel distance

**Diablo 3 monster density — documented design intent:**
- D3 deliberately increased trash density vs D2. Trash packs of 8–20 monsters are common in dungeon rooms.
- Elite ("yellow") packs: typically 3–4 monsters with affixes. 2–5 per room in dungeon content.
- In Nephalem/Greater Rifts, the monster density algorithm was reworked specifically to eliminate empty rooms — every tile gets populated.
- Connective room sized encounter: ~15–30 trash + 2–4 yellow packs is the D3 standard for a medium room traversal.

**Path of Exile density:**
- PoE players and community consistently describe PoE density as lower than Diablo — "Diablo has ten times more density and action." This is subjective but consistent across sources.
- PoE endgame (endgame maps with density juicing) approaches D3 levels but base campaign zones feel sparse by comparison.
- PoE 2 further reduced base density vs PoE 1 (per 2024–2025 patch discussions); player feedback on restoration of density reflects that the genre expectation is high density.

---

## Section 2 — Ravine / Canyon / Gorge Floor Plan Conventions (Q1)

### 2a. How the genre handles "canyon floor, walls bound you"

No ARPG appears to use literal terrain-modeled ravine geometry as its PRIMARY zone-defining mechanic (i.e., a 3D ravine with actual variable-height rock walls). Instead, the genre converges on these approaches:

**Approach A — Narrow tile corridor with decorative walls (D2 Act 3 jungle/spider forest):**
The 64×192 layout is the clearest genre example. Width is intentionally constrained (2 map-tiles = approximately 64 tile-units wide). Navigation is linear north-south. Side alcoves (3 per zone) branch off the main spine but dead-end back. Wall-like boundaries are implied by the tileset art (dense jungle, stone pillars at alcove entrances) rather than explicit collision geometry. The constraint is achieved purely by the tile layout — there is no traversable path except the defined spine.

**Approach B — Static exterior shell with procedural interior fill (D3):**
D3 outdoor zones use a fixed outer perimeter (the "shell") that communicates environmental constraints thematically. Inside the shell, procedural chunks fill the space. The canyon/ravine *feel* comes from art direction (rock walls, cliff edges) rather than mechanical geometry.

**Approach C — Linear corridor maps with environmental dressing (D4):**
D4 outdoor zones described by players as "corridors with outdoor tileset." Width is ~1 room's worth of space; walls are implicit from non-traversable terrain edges. This is the "tube" pattern — functionally equivalent to an indoor corridor but with sky/foliage art.

**Approach D — Hand-authored pass zones with loading barriers (Torchlight II):**
Passes in TL2 explicitly function as narrow connective zones between larger open areas. The pass geometry was not documented dimensionally but the design intent is corridor-shaped.

### 2b. Natural-wall bounding conventions

Sources converge on a key principle: natural obstacles (cliff faces, water, dense foliage) communicate impassability without prompting or invisible walls because players draw on real-world intuition. The canyon/gorge archetype works because height differential or dense vegetation naturally signals "can't pass." (Source: gamedeveloper.com obstacle design article.)

For a fantasy ravine specifically:
- Height: cliff walls above player height (at least 2× player character height visible above the playfield) signal impassability.
- Density: dense undergrowth, root masses, or rock walls function as collision without explicit invisible barriers.
- Linear sightline: the corridor should have visible "end" — either a gate, a path curve, or foliage occluder. This keeps the player oriented and prevents the emptiness-detection that kills linear zones.

### 2c. Corridor width conventions for a "ravine floor" zone

From the D2 Spider Forest data: 64 tile-units wide accommodates comfortable two-character-width navigation plus side alcoves. In D1 terms, 4–6 tiles wide is the minimum comfortable combat corridor (Catacombs corridors: 1–3 tiles wide, which is very tight — too tight for ARPG combat). D3's connective corridors: 3–5 visual tiles wide.

**Practical range from evidence:**
- Minimum functional combat corridor (D1): 3–4 tiles (very cramped, single-player viable but no AoE room)
- Comfortable ARPG combat corridor: 6–10 tiles wide (D2 Spider Forest at 64 tile-units accommodates this; D3 connectors at 3–5 "chunk tiles" which represent larger world-space than D1/D2 tiles)
- Open outdoor zone: 64–80 tiles wide (D2 outdoor zone standard)

---

## Section 3 — Procedural Tile-Layout Methods (Q4)

### 3a. Per-game method survey

**Diablo 1:**
Two-stage generation. Stage 1: predungeon walkability blueprint built by recursive room budding (place spine rooms on a 40×40 grid, bud child rooms off the spine using L-shaped subdivision). Stage 2: "marching squares" or custom pattern-matching converts the walkability blueprint into visual tiles per-stage tileset. This is a fully algorithmic approach — no pre-authored rooms, just walkability rules. Corridor widths emerge from the generation rules (1–3 tiles wide in Catacombs). Rooms are defined by the walkability boundary, not pre-authored chunks.
Source: boristhebrave.com D1 dungeon generation analysis.

**Diablo 2:**
Pre-authored DS1 "room" files (maze tiles) that the engine assembles on a grid. Each DS1 file defines a fixed room shape with defined entry/exit points. The engine places rooms on a grid using entry/exit socket matching — any room can attach to any room that has a compatible exit point. This is a socket-adjacency system: rooms carry labeled edge sockets (entry/exit positions on their boundary tiles), and the assembler pairs compatible sockets. Outdoor "overworld" areas are generated differently — they use a distinct terrain generation pass.
Source: d2mods.info Phrozen Keep forum, maxroll.gg map reading guide, diablo2.io.

**Diablo 3:**
Pre-authored "tile" chunks (rooms, corridors, set-pieces) with procedural runtime assembly. Corridors of 3–5 tile widths connect room nodes. Exterior zones use a static shell with procedurally-filled "holes" (multiple artist-authored pieces per hole shape, one chosen randomly at runtime). Chunks that don't connect cleanly are "glued" by procedurally generated floor+wall fill.
Source: purediablo.com randomization article, pcg.wikidot.com D3 entry (redirect; content from PCG wiki).

**Path of Exile:**
Hand-designed tile pieces (corridors, rooms, rivers, connectors) assembled semi-randomly per zone via a layout grammar. The generation uses Wang-tile principles for ground texture seaming (16 tiles with matched edge-colors; any blue-edge tile mates with any other blue-edge tile). Room-scale piece layout uses overlap capability — rooms can overlap at seam edges with rules to resolve conflicts. The system also incorporates "pre-placed" mandatory pieces (boss room, entrance, exits) with the grammar filling in the connective tissue. Full technical spec is in Rhys Abraham's ExileCon 2019 talk (YouTube: https://www.youtube.com/watch?v=EXnoHTqO7TE — not directly accessible for text extraction, but summarized in GGG's Steam announcement).
Source: PoE Steam/forum announcements, Wikipedia PoE procedural generation entry, PoE forum procedural gen thread.

**Last Epoch:**
Procedurally generated zones per dungeon run. Technical specifics not publicly documented.

**Grim Dawn / Torchlight:**
Hand-authored zones with randomized monster placement. No documented procedural room-assembly system. Grim Dawn outdoor passages feel authored (fixed topology, randomized enemy placement).

### 3b. Wave Function Collapse — analysis for small-scale (N=4 tiles)

**What WFC is:**
A constraint-propagation algorithm that fills a grid by collapsing cell possibilities (each cell starts as superposition of all tile types; collapse propagates adjacency constraints outward). Comes in two modes:
- Simple Tiled Model: tiles defined with explicit adjacency rules (socket system: each tile edge labeled; matching labels can be adjacent, mismatched cannot).
- Overlapping Model (exemplar-inference): learns adjacency rules automatically from a small input example (16×16 is sufficient as a training input) by enumerating all N×N pixel patches.
Source: gridbugs.org WFC article, boristhebrave.com WFC tips.

**Known weakness — global structure:**
WFC's core failure mode is global structural incoherence. The algorithm "only makes the output look like the input locally — when viewing small rectangles of output at a time." Applied to dungeon generation without additional constraints, WFC will create rooms that look locally like a dungeon but globally may produce disconnected spaces, dead-end corridors with no exit, or monotonous repetition at scale.

Specific failure modes documented:
1. Connectivity: without an explicit "path constraint" post-process, WFC can generate entirely disconnected rooms. The path constraint is a standard bolt-on solution (find connected components, verify a traversable path exists, otherwise resample).
2. Repetition at scale: "if you generate a large map with it, it starts to look very samey." Caves of Qud addresses this by subdividing maps into biomes and running WFC separately per biome.
3. Contradiction failure: with tight constraints and small tilesets, the propagation can corner itself into an unsolvable state. Backtracking or rule loosening is required.
Source: boristhebrave.com WFC tips and tricks, gridbugs.org WFC.

**WFC at N=4 tiles specifically:**
- For N=4 (4 tile types), a minimal "rooms" WFC config can generate square rooms: "a 4 tile combo (one tile is empty) easily generates square rooms" per boristhebrave.com.
- At N=4, the WFC algorithm is functionally equivalent to a very simple hand-authored adjacency table — the constraint set is small enough that a human can enumerate all valid adjacencies manually in minutes. WFC's overhead (implementation complexity, contradiction handling, backtracking) is not justified at this scale.
- WFC earns its complexity at medium-to-large scale with diverse tilesets where manual adjacency enumeration becomes intractable — approximately 10+ tile types with multiple possible adjacencies each.
Source: boristhebrave.com WFC tips, go-wfc GitHub.

**WFC vs hand-authored edge-socket contract at N=4:**
At N=4 tiles (or a 2×2 map of pre-authored tile chunks), the correct choice is a **hand-authored edge-socket adjacency contract**, not WFC. Reasons:
1. The adjacency table is small (4 tile types × 4 edges = 16 entries maximum, most will be simple pass/no-pass decisions).
2. WFC's complexity budget (contradiction handling, backtracking, exemplar creation) buys nothing at this scale — the constraint space is not diverse enough to need it.
3. WFC cannot provide global composition guarantees without add-ons (path constraints, biome subdivisions). A hand-authored socket contract *is* the global composition guarantee.
4. For "feels authored" quality (gandalf's framing), hand-authored sockets enforce design intent directly; WFC requires designing the exemplar AND the constraint rules AND the global post-process on top.

**At what tile count does WFC start earning its keep:**
The inflection point from the evidence:
- 4–8 tile types: hand-authored adjacency is simpler and more controllable.
- 10–20 tile types: WFC begins to pay off if the design intent is "local coherence with infinite variation."
- 20+ tile types or multiple tilesets: WFC or similar constraint solvers become clearly superior to manual enumeration.
- For 2D dungeon generation with biomes or theme-variation across a large map: WFC + hierarchical structure (global layout first, local fill second) is the current research-recommended approach.
Source: boristhebrave.com; arxiv 2308.07307 (hierarchical WFC for large-scale content).

---

## Summary (4 sentences)

D2's outdoor "connective middle" zones are consistently **80×80 tiles** (near-square, open); outdoor pass/ravine zones are **64×192 tiles** (3:1 aspect, 64 wide), with 10–15 elite packs and 90–163 total monsters per corridor zone. A genre-canonical single-room encounter (not a whole zone) in a D2-style dungeon spans roughly 6–10 tiles across the combat dimension, holding 1–3 trash groups (3–12 monsters) plus 0–1 elite packs at a time; in D3's denser paradigm, a traversal room holds 15–30 trash and 2–4 yellow packs. Ravine/canyon zones in the ARPG genre are universally achieved by narrow tile corridors (not modeled terrain geometry), with width of 4–10 tiles accommodating combat, natural-wall art direction communicating impassability, and a 2–4:1 length-to-width ratio giving the "corridor through terrain" feel. WFC is not warranted for a 2×2 tile map; at N=4 tiles, a hand-authored edge-socket adjacency contract is the correct tool — WFC earns complexity overhead only at ~10+ tile types where manual adjacency enumeration becomes intractable.

---

## Knowledge Gaps Not Resolved

1. **Real-world meter scale for D2 tiles:** No official Blizzard documentation found. Community estimate (~2–3 m per tile) is plausible but unverified. The D1/D2 tile (160×80 px) subtile (36×18 px) system was designed for isometric presentation, not world-scale accuracy.
2. **D3 room "chunk" pixel/unit dimensions:** The D3 room pieces have no publicly documented tile-unit sizes. The "3–5 tiles wide corridor" reference treats D3's visual tile as the unit, which is a larger world-space unit than D1/D2 tiles. No meter conversion found.
3. **PoE room/piece dimensions:** The ExileCon talk (Rhys Abraham, 2019) was not accessible as text; its full technical detail on piece sizing is video-only. No community text summary with numeric dimensions was found.
4. **Grim Dawn and Last Epoch room dimensions:** Neither Crate Entertainment nor Eleventh Hour Games has published technical level-design specs. Community wikis document zone names and topology without numeric dimensions.
5. **D2 indoor dungeon room DS1 dimensions:** The DS1 format encodes per-room dimensions, and the Phrozen Keep forums reference this, but extracting specific room tile counts per dungeon type would require direct file inspection (outside web research scope).
6. **Elite pack vs champion pack split in D2:** The MonUMin/MonUMax values cover both types together. The per-zone split between champion packs and unique+minion boss packs is not cleanly documented in accessible community sources.

---

## Source List

| Source | URL | Type | Access |
|---|---|---|---|
| Diablo 1 dungeon generation analysis | https://www.boristhebrave.com/2019/07/14/dungeon-generation-in-diablo-1/ | Primary (code analysis) | 2026-06-20 |
| WFC tips and tricks | https://www.boristhebrave.com/2020/02/08/wave-function-collapse-tips-and-tricks/ | Primary (practitioner) | 2026-06-20 |
| D2 tile size (Phrozen Keep) | https://d2mods.info/forum/viewtopic.php?t=46249 | Community technical | 2026-06-20 |
| D2 Stony Field zone data | https://lootcube.net/en/zones/stony-field | Community database | 2026-06-20 |
| D2 Blood Moor zone data | https://lootcube.net/en/zones/blood-moor | Community database | 2026-06-20 |
| D2 Cold Plains zone data | https://lootcube.net/en/zones/cold-plains | Community database | 2026-06-20 |
| D2 Spider Forest zone data | https://lootcube.net/en/zones/spider-forest | Community database | 2026-06-20 |
| D2 Great Marsh zone data | https://lootcube.net/en/zones/great-marsh | Community database | 2026-06-20 |
| D2 Flayer Jungle zone data | https://lootcube.net/en/zones/flayer-jungle | Community database | 2026-06-20 |
| D2 Stony Tomb L1 zone data | https://lootcube.net/en/zones/stony-tomb-level-1 | Community database | 2026-06-20 |
| D2 map reading (tile grid explanation) | https://maxroll.gg/d2/resources/map-reading | Community guide | 2026-06-20 |
| D2 elite pack spawn accuracy discussion | https://diablo2.io/post4029000.html | Community forum | 2026-06-20 |
| D3 randomization and level design | https://www.purediablo.com/randomization-and-level-design-in-the-future-of-diablo-3 | Secondary analysis | 2026-06-20 |
| D4 tube dungeon player discussion | https://us.forums.blizzard.com/en/d4/t/why-is-every-dungeon-in-d4-a-tube-layout-dungeon/57746 | Community forum | 2026-06-20 |
| PoE procedural world generation (Steam) | https://store.steampowered.com/news/app/238960/view/1688222120326067330 | Developer announcement | 2026-06-20 |
| PoE ExileCon Rhys Abraham talk (video) | https://www.youtube.com/watch?v=EXnoHTqO7TE | Primary developer | 2026-06-20 (not text-extracted) |
| PoE dev diary: tile texture maps | https://www.pathofexile.com/forum/view-thread/55091 | Developer (art) | 2026-06-20 |
| WFC gridbugs.org | https://www.gridbugs.org/wave-function-collapse/ | Practitioner analysis | 2026-06-20 |
| Level Design Book — corridor typology | https://book.leveldesignbook.com/process/layout/typology | Educational | 2026-06-20 |
| Level Design Book — encounter design | https://book.leveldesignbook.com/process/combat/encounter | Educational | 2026-06-20 |
| Angry GM — encounter space sizing | https://theangrygm.com/mapsturbation-and-the-size-of-encounters/ | Practitioner | 2026-06-20 |
| Torchlight II level design Q&A | https://www.runicgames.com/blog/2011/05/20/level-design-q-a/ | Developer primary | 2026-06-20 |
| Gamedeveloper.com — credible obstacles | https://www.gamedeveloper.com/design/defining-boundaries-creating-credible-obstacles-in-games | Design theory | 2026-06-20 |
| arxiv 2308.07307 — hierarchical WFC | https://arxiv.org/abs/2308.07307 | Academic | 2026-06-20 |
