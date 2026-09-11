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
[E05P motion review](experiments/E05P/review.html) rejects the cutout gait despite passing geometry. [E06D](experiments/E06D/REPORT.md) prepares the neutral VFX boundary only; [E01M](experiments/E01M/review.html) recovers native promotional motion without closing ordinary-HUD gates. [Progress](PROGRESS.json) records E05K pose-key contact failure. [E05B](experiments/E05B/review.html) establishes explicit rig/mesh contact control and Pixi frame delivery, with garment/style limits. [E07V](experiments/E07V/review.html) now presents four faction boards and a mixed scene with Matt’s [selected working target](VISUAL_TARGET.md): F04 clarity and F03 environment detail/light. [E08A](experiments/E08A/review.html) passes scoped neutral atlas packing; [E08D](experiments/E08D/review.html) makes inventory/capacity assumptions explicit. [E05C](experiments/E05C/review.html) now proves scoped garment visibility; [E05T](experiments/E05T/review.html) improves painted texture boundaries. [E04S](experiments/E04S/review.html) adds clean geometry-owned floor materials and measured floor/wall light response. [E05M](experiments/E05M/review.html) now proves one-view idle/walk/cast mechanisms and a measured release socket. [E01Y](experiments/E01Y/review.html) recovers PoE1/GD native footage and identifies originalD2 candidates. Continue PROGRESS.json; full-pilot/gear/VFX/scale gates remain incomplete. Both failed animation methods and their exhausted call limits remain frozen. Continue across bounded experiment
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
