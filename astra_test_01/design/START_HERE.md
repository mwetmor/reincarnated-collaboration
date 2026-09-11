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
The [three-renderer browser review](experiments/E02P/review.html) and
[E02P report](experiments/E02P/REPORT.md) contain the completed Godot/Pixi/Phaser
placement foundations. Matt approved Phaser 4 as the third test candidate.
Use standalone HTML reviews: Matt reports Canvas links open as code. The saved
review works from disk; the live Phaser probe needs the server in its report.
[Renderer research](experiments/E02/RENDERER_RESEARCH.md) retains other alternatives.
Godot's recovered 3D camera remains a starting candidate only.
Compare native gameplay exemplars from Diablo II, Path of Exile 1, Grim Dawn and
Last Epoch before selecting painted-world projection and on-screen scale.
The four faction identities share one eventual visual/spatial contract.

Claude's chamber note is incorporated with explicit refinements in the plan.
The preferred hypothesis is layout data → blockout → painting → verified runtime
layers. Art is the visual deliverable; authored spatial data governs behavior.
The feasibility of that pipeline remains to be tested.

## Prompt for the next session

> Continue the painted-world test suite in
> `/Users/admin/Games/reincarnated-collaboration`. Read `AGENTS.md` and its charter
> routes, then `.agents/skills/painted-character-vfx/SKILL.md` and
> `astra_test_01/design/START_HERE.md`. Resume the next action in `PROGRESS.json`.
> Work autonomously within the recorded scope. Continue projection C and the
> shared Godot/Pixi/Phaser composition benchmark. E02P qualifies Phaser 4.2.1
> for placement/attachments/basic UI only; all three capture batches are used.
> Register E03 for C-conditioned painted floor/prop and actor-view controls next.
> Deliver browser HTML, not Canvas source links. E02/E02P are partial capability
> results, not painted-chamber passes. Keep E01
> native-motion gaps open and do not repeat exhausted searches. Preserve the original ASTRA TEST 01 results.
> Treat Godot camera settings and persistent-layer animation as hypotheses for
> this new suite, not inherited passes. No internal subagents. Update the durable
> evidence and handoff before ending.
