# ASTRA workstream routing

Current work: the painted-world suite and its cross-session plan. Read
[START_HERE](../../../../astra_test_01/design/START_HERE.md), then its progress
record. The next task is native four-game exemplar research, not old-run repairs.
The camera is provisional for painted 2D; floor production and environment
interactions are now part of the test suite.

## Original ASTRA TEST 01 — historical campaign scope

Brief: `codex-3d-modeling/ASTRA TEST 01 painted character vfx.md` at repo root.
Last production work: `astra_test_01/run_03/`; `STATE.json` and `REPORT.md` there
record that campaign, not the current suite's next action.
Historical runs 01/02 are immutable evidence, not inputs to overwrite.

Next-suite visual planning: [four-faction key](../../../../astra_test_01/design/FACTION_KEY.md)
records the user's agreed working labels and subsequent scale/cohesion requirements.
It does not change the original ASTRA run contract or establish a production renderer.
The [Godot camera evidence](../../../../astra_test_01/design/CAMERA_BASELINE.md)
records the supplied 3D references and a proposed camera for the next suite.
Preserve its distinction between the original dimetric test and Godot perspective.

The user's earlier campaign instruction authorized creating this skill, wiring AGENTS.md,
updating the process from evidence and running autonomously toward passing all
character/animation and VFX/animation tests. This authorizes a continuing campaign
after the prior two-failure stop. Preserve failed attempts; retain every art
threshold and prerequisite. Continue measured repairs without per-attempt re-asking.
It does not authorize remote pushes, external messages or internal subagents.

Start by reusing run-02 painted art and correcting registration. Do not regenerate
a master merely to reset a run. Character: 8 directions in S/SW/W/NW/N/NE/E/SE order;
idle 8, walk 8, cast 12 per direction. VFX: cast 8, travel 6, impact 10. Read the brief
for exact dimensions, timing and gates; it remains the parameter source.

For moving poses, record two concepts explicitly: the fixed character ground/root
anchor and the visible sole contacts. The brief's contact wording is ambiguous for
walking; do not claim a literal sole-contact pass from atlas pivot metadata alone.
Measure and report both rather than silently redefining the test.

Generation: built-in imagegen with references. No seed or explicit mask is exposed.
Python matting/registration/packing is authorized in the preceding process request.
Use generation for pose changes; do not silently substitute procedural deformation
for a generated-animation test. VFX extraction must preserve detached particles.
