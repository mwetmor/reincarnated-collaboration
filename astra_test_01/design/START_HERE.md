# Painted-world test suite — start here

This is the continuation entrypoint for the user-authorized painted 2D world
experiment. The product under test includes floors/environments, characters,
monsters, modular equipment, interactive objects, and animated VFX.

Read the repository charter first, then:

1. [Progress](PROGRESS.json): current milestone, next action, unresolved decisions.
2. [Architecture plan](ARCHITECTURE_PLAN.md): contracts, floor production,
   interaction proof, validation matrix and scale strategy.
3. [Experiments and gates](EXPERIMENTS.md): falsifiable hypotheses and what evidence
   permits the next investment.
4. [Session protocol](SESSION_PROTOCOL.md): resumption, records, budgets, improvement.
5. Read only the supporting sources needed for the current task:
   [faction key](FACTION_KEY.md), [Godot camera evidence](CAMERA_BASELINE.md),
   [source intake](SOURCE_INTAKE.md).

The original ASTRA TEST 01 and its runs remain historical tests with unchanged
criteria. The working name **ASTRA TEST 02** refers to the new painted-world
suite; it has no passing production result yet. Its first environment milestone
is one interactive painted chamber, not a claim that the full suite is complete.

The [E01 comparison packet](experiments/E01/comparison.html) now contains inspected
native stills, [findings](experiments/E01/REPORT.md), a three-candidate geometry
study, and logical chamber preparation. G1 remains incomplete because native
uncut HUD motion is missing. Follow PROGRESS.json for the precise next action;
do not repeat the exhausted source searches. Matt has since selected C for testing;
final visual approval remains separate.

Latest user direction: use C to test perspective compatibility, and compare agent
scene/character/VFX composition in Godot, Pixi.js and researched alternatives.
The [painted three-renderer checkpoint](experiments/E03/review.html) and
[E03 report](experiments/E03/REPORT.md) record completed Godot/Pixi/Phaser tests.
**Codex-selected-winner: Pixi.js 8.20.1**, at Matt's explicit request. Continue
chamber interactions, then bounded gear and VFX proofs in Pixi only. Matt reserves
later VFX tests in the other regimes. Native generated alpha failed; a separately
registered static runtime-mask alternative was tested, without erasing that failure.
Use standalone browser HTML reviews; Canvas source links opened as code for Matt.
Godot's recovered 3D camera remains a starting candidate only.
Compare native gameplay exemplars from Diablo II, Path of Exile 1, Grim Dawn and
Last Epoch before selecting painted-world projection and on-screen scale.
The four faction identities share one eventual visual/spatial contract.

Claude's chamber note is incorporated with explicit refinements in the plan.
The preferred hypothesis is layout data → blockout → painting → verified runtime
layers. Art is the visual deliverable; authored spatial data governs behavior.
The feasibility of that pipeline remains to be tested.

Latest completed milestone: [E04 browser review](experiments/E04/review.html) and
[report](experiments/E04/REPORT.md). Chamber fixture logic, JSON boundary and
neutral manifests passed scoped checks. Matt's sharpness/edge/lighting feedback
is now recorded: fresh rasterization improves characters, source floor detail is
limited, current contours have visible defects, and shared lighting remains
unqualified. **Godot is the shipping target; Pixi is the test harness.** The
[four portability constraints](experiments/E04/NEUTRAL_CONTRACT.md) apply to all
subsequent work. Follow [the exact next test](experiments/E04/NEXT_TEST.md) before
continuing motion/gear and VFX; do not treat technical passes as visual approval.

Current autonomous continuation: [E04M2 contour repair](experiments/E04M2/review.html)
and [E04L lighting](experiments/E04L/review.html) have scoped component results.
[E05P motion review](experiments/E05P/review.html) rejects the cutout gait despite passing geometry. [E06D](experiments/E06D/REPORT.md) prepares the neutral VFX boundary only; [E01M](experiments/E01M/review.html) recovers native promotional motion without closing ordinary-HUD gates. [Progress](PROGRESS.json) records E05K pose-key contact failure. [E05B](experiments/E05B/review.html) establishes explicit rig/mesh contact control and Pixi frame delivery, with garment/style limits. [E07V](experiments/E07V/review.html) now presents four faction boards and a mixed scene with Matt’s [selected working target](VISUAL_TARGET.md): F04 clarity and F03 environment detail/light. [E08A](experiments/E08A/review.html) passes scoped neutral atlas packing; [E08D](experiments/E08D/review.html) makes inventory/capacity assumptions explicit. [E05C](experiments/E05C/review.html) now proves scoped garment visibility; [E05T](experiments/E05T/review.html) improves painted texture boundaries. [E04S](experiments/E04S/review.html) adds clean geometry-owned floor materials and measured floor/wall light response. [E05M](experiments/E05M/review.html) now proves one-view idle/walk/cast mechanisms and a measured release socket. [E01Y](experiments/E01Y/review.html) recovers PoE1/GD native footage; [E01D](experiments/E01D/review.html) now recovers original D2 LoD traversal/combat. [E05G](experiments/E05G/review.html) passes sparse gear composition/fit controls. [E06F](experiments/E06F/review.html) now verifies the first painted frost release/travel/impact mechanism with bright-background material limitations. [E07R](experiments/E07R/review.html) tests the delegated distinct strongholds: doorway semantics improve, but full-scene geometry/content fails; its3-call branch is closed. [E07S](experiments/E07S/review.html) preserves exact doorway/collision/light behavior using painted materials on typed geometry; complete chamber art still fails (plain structure/props and actor shading). [E05V](experiments/E05V/review.html) stops eight-view expansion on art failure; [E05H](experiments/E05H/review.html) repairs the exposed rear scalp while leaving full pilot/gear art unqualified. [E07D](experiments/E07D/review.html) proves prop-state mechanisms while exposing surface-detail ordering failure; [E07Z](experiments/E07Z/review.html) now repairs21/21 opaque part-depth witnesses, while actor/translucent-effect depth and full art remain open. [E09I](experiments/E09I/review.html) preserves actual pipeline content through a23-check neutral import, with full combat/event/footprint binding still open. Follow [Matt’s further faction, doorway and blood-impact feedback](experiments/E07V/FEEDBACK_2026-09-11.md). Continue PROGRESS.json; full-pilot/gear/VFX/scale gates remain incomplete. Both failed animation methods and their exhausted call limits remain frozen. Continue across bounded experiment
checkpoints while authorized work remains; Matt requested the entire architecture
be pursued autonomously. Keep all original thresholds and failures, including
E04L's recorded storage-limit deviation.

## Prompt for the next session

> Continue the painted-world test suite in
> `/Users/admin/Games/reincarnated-collaboration`. Read `AGENTS.md` and its charter
> routes, then `.agents/skills/painted-character-vfx/SKILL.md` and
> `astra_test_01/design/START_HERE.md`. Resume the next action in `PROGRESS.json`.
> Work autonomously within the recorded scope. Continue projection C and the
> painted checkpoint. E03/E03M completed in all three; read its report. Pixi.js is
> the codex-selected-winner. Continue E04 chamber interactions, then separately
> registered gear and VFX tests there only. E04 logical checkpoint is now complete;
> E04M2/E04L now have scoped contour/lighting results. E05P cutout gait failed; follow PROGRESS for the changed pose-key test, preserving all failures.
> Godot is the shipping target; Pixi is the test harness. Other-regime VFX is Matt's later call.
> Preserve the native-alpha failures and unapproved visual style. Do not repeat
> exhausted E03 capture batches. Deliver browser HTML, not Canvas source links.
> Keep E01
> native-motion gaps open and do not repeat exhausted searches. Preserve the original ASTRA TEST 01 results.
> Treat Godot camera settings and persistent-layer animation as hypotheses for
> this new suite, not inherited passes. No internal subagents. Update the durable
> evidence and handoff before ending.

E05A checkpoint: [fitted gear and failed layer transfer](experiments/E05A/review.html), [report](experiments/E05A/REPORT.md).47/96fail; body/actions unchanged. Next: E05O layer source diagnosis; full art still unqualified.

E05O [coverage review](experiments/E05O/review.html) and [report](experiments/E05O/REPORT.md): all3methods fail full matrix; independent-RGBA branch stopped. Next: E05J depth-bearing geometry capability/gear probe in Pixi. Full painted pilot stays open.

E05J [shared rig / gear review](experiments/E05J/review.html) and [report](experiments/E05J/REPORT.md): depth-bearing source representation passes288sparse comparisons and corrected exact depth ordering in Pixi. Full art/sampling/animation still open. Next E05Q native sampling/clarity comparison.

E05Q [native clarity review](experiments/E05Q/review.html) and [report](experiments/E05Q/REPORT.md): BMSAA/mips selected8/8; fresh3×reference retained, old clipped strip preserved. Current exact next action: E07K pilot/chamber depth/light integration.

E07K [pilot/chamber review](experiments/E07K/review.html) and [report](experiments/E07K/REPORT.md): 372 occlusion witnesses, light controls and 38 interaction checks pass. Full art and contact shadows remain open. Next E07N connects the unused internal door to geometry/state.

E07N [internal-door review](experiments/E07N/review.html) and [report](experiments/E07N/REPORT.md): committed geometry/state, timed persistence, path invalidation and light blocking pass; smooth panel motion/final door art remain open. Next E07L pilot floor shadow.

E07L [floor-shadow review](experiments/E07L/review.html) and [report](experiments/E07L/REPORT.md):320CPU witnesses pass; grounded/raised/translated shadow controls improve attachment. Full character/chamber art and other shadow receivers remain open. Next E05U returns to full pilot/gear art before animation or roster expansion.

E05U [painted-gear comparison](experiments/E05U/review.html) and [report](experiments/E05U/REPORT.md): fitted part-specific gear and source transfer improve; full pilot art still FAIL against size-matched F04style crops. Next E05W base outfit material separation/hair silhouette, preserving rig/actions/gear.

E05W [static pilot review](experiments/E05W/review.html) and [report](experiments/E05W/REPORT.md): Codex scoped working-turnaround PASS under F04direction after material/hair repair. Full motion/turns/gear fit and production style remain open. Next E05Y complete existing clip palette transfer and eight-view playback.

E05Y full existing clips: [review](experiments/E05Y/review.html), [report](experiments/E05Y/REPORT.md). Walk art FAIL despite contact/core mechanisms; six cast raster failures retained. Exact next action is in PROGRESS.json.

E05Z [corrected gait review](experiments/E05Z/review.html): controlled stance-duration bug repair passes; old E05M/E05Y failures retained, cast-normal and complete pilot work open. PROGRESS.json carries exact next action.

E05N [normal agreement review](experiments/E05N/review.html):1296/1296comparisons pass after neutral deformation-normal correction; preserves repairedwalk. Measured16.736MB normaldata requires later scalequalification. Nextturncontacts per PROGRESS.json.

E05I [planted-foot turns](experiments/E05I/review.html): left/right45° idle transitions pass; sourcev1endpointfailure preserved and repaired. Locomotion/action transitions remain next per PROGRESS.json.

E05L [stop preflight failure](experiments/E05L/review.html):46/48sourcephasespass, two exceedjoint-stepbar; two-revisionlimitheld, no rasterexpansion. Separate timing study next per PROGRESS.json.

E05D [timing source comparison](experiments/E05D/review.html): .8s candidatepasses48/48sourcephases; exporthits35MBnormalguard. Representation/playback remainopen; perclipcodec recovery next in PROGRESS.json.

E08N [lossless transition review](experiments/E08N/review.html):294source and1152raster checks pass; missing-normal visual control insensitive and preserved. Six representative clips play, full locomotion remains open. E07T chamber door continuation next per PROGRESS.json.

E07T [continuous door review](experiments/E07T/review.html): partial collision/geometry pass; live playback and F01 pocket finish fail. Lintel exposes monster-height incompatibility. E07U renderer batching next per PROGRESS.json.

E07U [batched door review](experiments/E07U/review.html):64pixel-exact source images and local smooth motion pass after preserving the first batching failure. E07A current painted-pilot/chamber integration next per PROGRESS.json.

E07A [current pilot/chamber review](experiments/E07A/review.html):864source and sampleddepth checks pass; runtimewalk contact FAIL3.260cm versus2cm. Captureguardfailure preserved andmissingcases recoveredlosslessly. E05E fractional sampling preflight next per PROGRESS.json.

E05E [fractional sampler preflight](experiments/E05E/review.html): both source-agreement failures retained; actual Bézier source also penetrates between keys. E05F explicit interpolation contract next per PROGRESS.json.

E05F [fractional motion review](experiments/E05F/review.html): explicit source interpolation preserves keys and integer poses; 312 source and 864 raster checks pass, recorded walk contact ≤0.507 mm. Normal ablation remains insensitive. E07B current-pilot floor shadow next per PROGRESS.json.

E07B [current-pilot shadow review](experiments/E07B/review.html): 640 source witnesses pass, but the crate approach exceeds the old floor-sized mask and fails rendering. E07C padded allocation domain next; failed UI/encoder receipts retained.

E07C [padded shadow-domain review](experiments/E07C/review.html): preserves 640 interior witnesses; new boundary/mask and actual UI checks pass. West-apron positive camera samples remain unavailable behind the wall; direct mask proof passes. Current working chamber uses E07C with E05F fractional motion. E07E shared scene shadows next.

E07E [shared-shadow capability checkpoint](experiments/E07E/review.html): offscreen depth/encoding passes; two integrated builds fail shader compilation. E07F compiler-gated local repair is authorized by the continuing-campaign protocol. Original counters/failures retained; E07C remains the working chamber.

E07F [shared-shadow source comparison](experiments/E07F/review.html): compiler gate and864floor/vertical samples pass; two native pilot samples still fail. Strict source guard repair and original failures retained. E07G receiver-plane lookup next; E07C remains the working chamber.

E07G [receiver-plane review](experiments/E07G/review.html): GLSL3 derivative capability passes; corrected lookup exchanges two native failures for two fresh3× armor failures. E07H tests source-diagnosed map density next. E07C remains the working chamber.

E07H [denser raw lookup review](experiments/E07H/review.html): raw mode passes all1,302 source witnesses and controls; receiver-plane mode retains two failures. E07J neutral selection and actual interaction/playback next. Allocation arithmetic230.7MB, production residency unqualified.

E07J [selected shared-shadow chamber](experiments/E07J/review.html): all1,302 available source witnesses, actual controls and3outfit walks pass. Working chamber now E07J;21intermediate door states, local compositionp95 20.4ms. Next E07O selective player visibility; full art/self-shadow/performance remain open.

E07O [visibility capability checkpoint](experiments/E07O/review.html): two failed builds preserved. Matching multisample depth fixes mask pixels; custom uColor collision still fails GL. E07P namespace repair and source visibility proof next. E07J remains working chamber.
