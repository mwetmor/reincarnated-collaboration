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

Latest user direction: Godot's recovered 3D camera is a starting candidate only.
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
> Work autonomously within the recorded scope. Start with the four-game native
> exemplar comparison and camera/projection research gate, including painted
> floor and sprite compatibility. Preserve the original ASTRA TEST 01 results.
> Treat Godot camera settings and persistent-layer animation as hypotheses for
> this new suite, not inherited passes. No internal subagents. Update the durable
> evidence and handoff before ending.
