# Painted-world architecture and qualification plan

Version: 0.2, 2026-09-11. Status: qualification plan; implementation state is in PROGRESS.
User direction governs this experiment; production canon is reconciled separately
if the trial succeeds. Entry and current action: [START_HERE](START_HERE.md).

## 1. Product and decisions

Produce one coherent painted 2D world with four visually distinct factions,
100+ individually recognizable characters, modular gear progression, monsters,
24 reusable animated VFX archetypes, and floors/objects that support real play.
Validate ten finished characters before scaling. Keep starter clothing and
complete uncovered heads/hair in the requirements; hide-helmet is cosmetic.
See [faction key](FACTION_KEY.md) for names and scope; do not duplicate its lore.

Five workstreams remain: visual agreement; reusable contracts; representative
test matrix; layered acceptance suite; production cost/scale model. Floors and
interaction are part of every relevant workstream, not a background added last.

Open decisions: projection and gameplay scale; shared paint/material/lighting
response; starter inclusion in the three tiers; uniques as items versus sets;
target hardware and runtime budgets; minimum animation inventory. See progress
for who resolves each. These do not block reference intake or contract design.

## 2. Projection first, without inheriting a 3D camera

The [Godot evidence](CAMERA_BASELINE.md) supplies candidate framing and known
fixtures. Its metres/FOV/pitch are not automatically meaningful controls for a
flat Sprite2D painting. For a 2D camera, the apparent elevation is largely drawn
into the art; zoom scales it without changing its depicted viewpoint.

Research native gameplay for each source game: quiet traversal, busy combat,
and stronghold/interactable scenes. Separate original Diablo II from D2R;
PoE2 is optional, not a substitute for PoE1. Compare player body screen fraction,
ground foreshortening, near/far scale change, exposed top surfaces, prop overlap,
HUD obstruction and motion readability. Preserve native framing and uncertainties.
Do not infer exact FOV/distance from an uncalibrated screenshot.

Compare a source-informed fixed 2D affine/dimetric projection against the
recovered Godot framing as a candidate. Test at most three explicitly labelled
variants using matched layout/body sizes before choosing. The old ASTRA 45-degree
description is a historical comparator, not the default winner. All artwork in
a comparison cell must use that cell's projection; moving only its camera is
not a fair painted-asset comparison.

Start feasibility work with a 2D runtime. Hidden height/depth data is compatible
with painted artwork. A 2.5D renderer is a research fallback only if documented
occlusion/perspective tests justify it; production 3D character rigs are not a
prerequisite. Camera, paint style and runtime representation are separate choices.

Matt selected projection C for the next feasibility tests, then requested the same
scene/character/VFX composition in **Godot and Pixi.js**, with alternatives researched.
Compare the agent's ability to assemble, inspect and revise the painted presentation;
keep combat/content JSON from the serial pipeline as shared input. Do not select a
renderer for unrelated built-in combat features. The [shared benchmark](experiments/E02/RENDERER_BENCHMARK.md)
defines the comparison; [primary-source research](experiments/E02/RENDERER_RESEARCH.md)
recommends Phaser 4 as the third test. No production renderer or final painted target
is approved by the foundation probe.

## 3. World data and representation contracts

Author spatial truth once. Generate navigation, collision, overlays and blockout
guides from it; validate them against each other and the rendered picture.
Do not let a generated wall silently close a data-defined doorway. Repair the
picture or explicitly version the layout and all dependants.

Use distinct coordinates with explicit transforms:

- Logical ground `(u, v)` in declared world units; elevation/layer `h` where needed.
- Chamber image/mask `(x, y)` in native pixels, with origin and dimensions.
- Navigation cell `(i, j)` with declared cell size and clearance class.
- Screen coordinates after projection/camera transform, and local asset/sockets.

Store forward/inverse mappings and exercise round-trip probes. Path lengths,
speed, hit ranges and movement costs use logical space; diagonal projection must
not make diagonal motion faster or melee range depend on screenshot resolution.

Draft contract fields (formal schemas and validators land at G2):

| Record | Required responsibilities |
|---|---|
| `world_style` | version, approved anchors, projection ID, native review resolutions, palette/material/light rules, faction allowances, alpha/filter policy |
| `chamber` | stable ID/version/seed, layout source, world origin/units/transforms, art/layer hashes, static geometry, zones, exits/links, spawns, objects, lights, runtime state version |
| `surface` | walkability, movement cost, material/footstep/impact response, elevation/layer, hazard tags, decal/light receiving policy |
| `character` | identity/faction, stature and footprint, rig family, directional views, persistent layers, hidden-region completion, sockets, motion/gear compatibility |
| `gear` | item/set/slot IDs, fit family, rigid/deformable policy, anchors, visibility exclusions, view/keypose alternates, allowed materials |
| `motion` | time-based phases, logical displacement, foot contacts, pose tracks, action events, socket tracks, loop/cancel/interrupt behavior |
| `object` | stable ID, type, ground footprint, interaction approach region, sort anchors/split layers, state machine, collision/nav/occlusion changes, loot/event references |
| `effect` | archetype and binding version, lifecycle, world/actor/weapon attachment, layer/height, element/style parameters, terrain response, collision/LOS contract, budget |
| `build_receipt` | input/content hashes, tool/runtime versions, prompts/control availability, output mappings, tests and raw verdicts, costs, rejected attempts |

Masks are useful exchange/inspection artifacts, not a requirement that every
system use a same-resolution PNG internally. For the first chamber, aligned
same-size masks simplify inspection; later resolutions require explicit mapping.
Label masks use integer IDs, lossless storage and nearest sampling, not blended
colours. Zones may overlap: use separate channels/lists instead of one colour
trying to mean mud + hazard + trigger simultaneously.

Separate walkability, light occlusion, visual occlusion, physical height and
projectile blocking. One wall mask cannot reliably encode all five, especially
for arches, overhead objects or bridges. A single height per cell cannot represent
both a bridge and passage beneath it; layered surfaces/links are a later gate.

## 4. Floor and environment art production

Preferred experiment:

1. Author a small deterministic chamber layout with two exits, a narrow passage,
   a tall occluder, prop sockets, a surface transition and empty interactive slots.
   Validate dimensions/connectivity/clearance before requesting art.
2. Export projection-matched blockout guides and semantic masks from that layout.
   Generate one approved floor/material sample and a style anchor first.
3. Generate painted floor and structural layers conditioned on the guide. Keep
   movable/breakable/openable/lootable objects out of the background painting.
   Include clean floor beneath them and hidden artwork exposed by opening/breakage.
4. Compare painting to an overlay of required walls, door widths, edges and
   anchors. Conditioning is probabilistic: the blockout is not proof the image
   obeyed it. Preserve original art; repair/reject local geometry drift.
5. Assemble back walls, floor, static paint details, sortable vertical pieces,
   foreground/canopy and overlays as explicit layers. Generate separate prop
   states with matching perspective, light and occupied footprint.
6. Check world-size brush/detail consistency, footprint alignment, transparent
   edges, scale and material transitions in the actual gameplay view.
7. Prove expansion with two adjoining chunks and a second chamber. Shared edge
   guides/overlap margins, matching lighting and authored transition strips must
   avoid seams. Art may be non-tiled even when logical data uses a grid. Do not
   rotate/mirror lit texture variants without testing their lighting consequences.

Compare non-repeating painted chamber plates and reusable material/transition
patches on measured cost and repetition. Neither visible tiling nor a giant single
texture is imposed in advance. Record native generation size, texel density,
maximum texture size, chunk memory and camera-scroll/streaming costs before scaling.

Layered generation and post-hoc segmentation remain alternate methods. Floor
alpha is not walkability: rugs, grates, canopies and walkable painted margins
break that inference. Segmentation needs manual/agent annotation plus runtime
validation. Data-first generation is preferred, not claimed to be the only viable
procedural method.

## 5. Interactions on the painted floor

### Movement, collisions and dynamic navigation

Use a logical grid as the first navigation candidate, with conservative occupied
cells and actor-radius clearance. Test at least a small humanoid and a larger
monster. Grid size is derived from the narrowest valid corridor/footprint and
the projection; "32 art pixels" is not a world-scale contract.

Keep collision and navigation as distinct runtime consumers of the same spatial
model. Grid pathfinding alone does not prevent penetration or fast movement
tunnelling. Verify actual movement/shape sweeps and corner cutting. A navmesh is
an alternate smoother route representation, not a required second implementation.
Flow fields/local avoidance enter only after crowd profiling justifies them.

Doors expose separate locked, closed, opening, open and closing states. Unlocking
does not necessarily open the door. An authoritative transition updates sprite,
physical blocking, nav topology and relevant occlusion at a defined event/time;
invalidate cached routes. Retain blocker ownership/refcounts so removing a crate
does not clear a wall or another blocker occupying the same cells. Handle a
creature in the doorway and fail/retry closing according to a declared policy.

Connectivity expectations are state-specific graphs. An intentionally locked
room or island is not automatically a defect. Test permitted reachability and
forbidden paths in closed/open/broken states, not "one component" unconditionally.
Path to a chest's valid interaction approach region, not its blocked centre.

### Feet, props, elevation and shadows

The character root lives on the logical ground. Planted feet compensate for root
motion in world space; feet/weapon tips are not inferred from padded image bounds.
Shadows follow ground support while airborne bodies move above it. Sort by ground
anchor plus explicit rules, not the current animation silhouette or jump height.

Tall walls, archways, long props and tree canopies may need multiple draw pieces,
occlusion masks and height-aware ordering. A single y-sort pivot is insufficient
for every overlap. Light occluders and visual occluders are separate. Test both
front/behind crossings, two actors on opposing sides, and loot behind a prop.

Loot containers emit one authoritative reward event; repeated clicks/reloads
cannot duplicate it. Breakage updates blockers at its event, leaves the intended
debris state, and reveals clean underlying floor. Persist door/object/loot state
across exit/re-entry. An NPC receives symbolic room/object/state data; an optional
LLM does not infer collision from artwork at runtime.

### VFX and surface response

Keep the sealed [24-archetype binding spec](../../agentic_orchestration/gandalf/notes/2026-08-24-vfx-archetype-binding-spec-DRAFT.md)
as the semantic source: including held cases and PAYLOAD/TRAIL/FIELD distinctions.
Ground effects use projected footprints, trails follow time-stamped sockets,
projectiles declare height/LOS/hit behavior, and impacts bind to the hit surface.
Rendering does not alter ability range or simulation outcomes.

Material tags drive dust/scuffs, chips, splashes and impact/decal choices. Test
stone versus soil first. Ice/fire/physical variants may change authored texture,
particle shape and timing within the archetype contract, not merely tint; they
must preserve recognizable element meaning and delivery behavior. Gameplay
slow/freeze/hazard changes require gameplay data, not a colour inference.

Damage footprints, warning telegraphs, decorative smoke and lingering decals
have separate lifetimes and bounds. Test effects behind/in front of props,
on terrain transitions, on monsters with different sockets, and near screen/HUD
edges. Limit overlapping effects by measured screen area/layers, memory and
frame time; particle count alone is insufficient.

### Light response

Select shared baked ambient/directional cues, contact shadow treatment, and
dynamic spell-light policy through comparison. Test unlit painted assets plus
controlled overlays against restrained 2D lights/normal maps. Normal maps and
emissive masks are optional derived assets requiring their own QA; neither
recovers physically correct geometry automatically. Avoid painting a cast shadow
under a movable object into the permanent floor and then casting it again.

## 6. Character and gear pipeline

Persistent painted layers + reusable motion + rigid accessory attachments are the
leading hypothesis from [the supplied pipeline note](/Users/admin/Downloads/astra_claude_painted_2d_animation_pipeline.md).
Prove torso/bag stability, opposite leg leads, contacts and occlusion transitions
before adopting it. Texture persistence can still stretch a chest or create a
paper-puppet look. Hidden-region completion and new view/keypose drawings are
explicit production work, not assumed to come free with decomposition.

Start with one character, starter outfit and advanced outfit, uncovered head,
idle/walk/cast and turn transitions. Then run/attack/channel/spin as required by
the pilot; cover all eight declared views for final pilot acceptance. A limited
S/E probe qualifies only those views. Reuse motions by compatible rig families,
with fit constraints and bounded pose-specific corrections.

Keep modular source assets. Compare runtime composition with selective baking
and a content-addressed loadout cache. Do not bake the entire gear Cartesian
product. Record unsupported combinations and regeneration/repair work explicitly.

## 7. First environment proof: ASTRA TEST 02 chamber

One painted chamber, two exits, a mage, a larger monster, an NPC, one door, one
breakable crate, one lootable chest, a tall pillar/arch and stone/soil surfaces.
Use diagnostic stand-ins only for validating data/code; clearly label them and
replace them with painted candidates before any visual pass.

Scripted demonstration and assertions:

1. Spawn; walk the permitted perimeter in both directions; path to both exits
   and each reachable interaction approach point for both footprint classes.
2. Walk in front of/behind the tall object; cross near/far and chunk boundaries;
   verify feet, shadows and ordering. Exercise a small step/elevation fixture
   separately before claiming elevation support.
3. Attempt the locked door; unlock, open, traverse, close and replan. Verify
   blocked states physically and logically, including an occupied doorway.
4. Break the crate; check its footprint policy, debris, clean revealed floor,
   impact timing and NPC route changes.
5. Open the chest; spawn loot once; pick it up once; leave/re-enter and verify
   object and loot state. Reject duplicate events and inaccessible drops.
6. Cast a projectile/impact, ground field and weapon trail across the surfaces
   and occluder. Verify contacts, layer ordering, actual hit/visual correspondence
   and disappearance. Run a physical/ice/fire whirlwind comparison after its
   character spin motion is qualified.
7. Record normal-speed playback, debug overlays separately, event log and
   live runtime profile. Saved 60 fps video does not establish 60 fps performance.

Require zero failures in the discrete event/topology assertions. Numerical
contact/edge/performance bands and visual rubrics are frozen before the pilot
render, using the calibration process in [EXPERIMENTS](EXPERIMENTS.md).

## 8. Expansion and acceptance

After the chamber proof, transfer to a second chamber and another actor before
scaling. Produce four faction boards (people, starter/advanced gear, floor,
architecture, objects and matching VFX) and a mixed-faction scene. Review at
gameplay scale and close-up; the final ten-character batch covers all factions.
Proposed distribution 3/3/2/2, chosen for difficult silhouettes/gear, with two
characters held out from workflow tuning. Final selection is registered at G4.

Cover all 24 active VFX base behaviors once, then a risk-based variation matrix:
player/monster transfer on compatible fixtures; multiple elements and faction
styles; small/large actors; burst/sustained/trail/field; clutter/light/dark venues.
Do not require meaningless combinations or pretend a few whirlwind recolours
qualify the other archetypes. Totem bodies and summons require model/sprite assets
in addition to their attack effects.

Hard structural/semantic failures cannot be averaged away by an aesthetic score.
Maintain separate identity, gait, environment interaction, VFX behavior/style,
faction distinction, world cohesion and performance verdicts. Validate evaluators
with intentional bad examples. Missing evidence is UNVERIFIED, never PASS.

Before 100-character production: review a broad 100-concept identity matrix,
nearest-neighbour confusion sets and a gear catalog plan; measure ten finished
characters including held-out transfer. Distinct silhouettes/material construction
and costume motifs must support identity without colour alone. These are scale
evidence, not a mathematical guarantee of 100 unique successful final assets.
Count authored pieces, complete sets and runtime combinations separately.

Budget generation, decomposition, repair, review, texture memory, animation
storage, compositing, navigation and overdraw. Record p50/p95 cost/time and failure
rates where samples support them; give ranges and assumptions with small samples.
Stop broad production on an unproven transfer mechanism or unbounded repair cost.

## 9. Source checks behind Claude-note refinements

Verified 2026-09-10 against official stable documentation; pin the installed Godot
version during implementation. These APIs support a prototype, not a quality pass.

- [AStarGrid2D](https://docs.godotengine.org/en/stable/classes/class_astargrid2d.html):
  grid pathfinding, solidity and movement-cost weights are available. Select a
  diagonal policy explicitly. `update()` clears point solidity/weight data;
  individual solid/weight changes do not require it. Rebuilds must restore static
  and dynamic data. Do not assume the grid supplies actor clearance or collision.
- [CanvasItem](https://docs.godotengine.org/en/stable/classes/class_canvasitem.html):
  y-sort orders nodes by Y; it does not segment paintings or derive occlusion.
- [2D lights and shadows](https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html):
  normal/specular maps can affect 2D lighting. Additive sprite effects do not cast
  shadows or respond to those maps like lights. Choose and test the intended mode.

Navigation does not inherently require a grid; a grid is the initial candidate.
The note's specific claim about Hades' internal implementation remains unverified
and is not used as an architectural premise.

### Renderer test update — 2026-09-11

Matt selected Phaser 4 for the third comparison adapter. [E02P](experiments/E02P/REPORT.md) verifies its C projection placement/root/socket/basic UI foundation alongside preserved Godot/Pixi evidence. Carry the same accepted E03 painted assets and layout/state contracts into all three. This does not qualify masks, occlusion, animation, gear, VFX, combat JSON integration or performance. No renderer winner is selected.
