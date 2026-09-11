# Hypotheses, research gates and experiment records

Version 0.1, 2026-09-10. All hypotheses below are OPEN. The plan is not evidence
that any of them pass. Current gate status lives only in [PROGRESS](PROGRESS.json).
Original ASTRA TEST 01 criteria are unaffected.

## Hypothesis register

| ID | Testable claim | Smallest useful evidence | Falsifier / response |
|---|---|---|---|
| H01 | One source-informed painted projection supports all four factions | Native four-game comparison, matched floor/actor/prop projection variants | Floor and actor views disagree or one faction requires a different projection; revise shared projection before production |
| H02 | Painting conditioned on layout preserves playable geometry | One painted two-exit blockout with boundary overlays and actual traversal | Painted obstruction/door width disagrees with data; repair/reject art and measure repair cost |
| H03 | Persistent layers reduce identity drift without unacceptable puppet motion | Same character idle/walk/cast, rigid bag, opposite leg leads, original source comparison | Chest stretches, repeated leading foot, paper joints or expensive per-frame repairs; alternate key drawings/rig family |
| H04 | Gear swaps reuse qualified motion economically | Starter/advanced outfits, exposed hair, helmet hidden, all pilot motions/views | Rebuilding motion or most frames per outfit; change fit contract or reject scale claim |
| H05 | Shared spatial data keeps collision, navigation and visible ground aligned | Perimeter/corner/door tests with two actor sizes and dynamic blockers | Any forbidden passage, tunnelling, corner cut or inaccessible required target; correct clearance/transforms/state mapping |
| H06 | Explicit sorting and ground anchors support painted occlusion | Front/back crossings, tall prop, two actors, raised body and loot | Body-wide order pops, shadow follows airborne body, loot impossible to see/reach; split layers/height-aware ordering |
| H07 | Objects can change state without corrupting the chamber | Door, crate, chest, loot, exit/re-entry event tests | Duplicate reward, stale path, ghost blocker or baked prop/shadow remains; revise state/data/art separation |
| H08 | One light/material policy unifies actors, floor, props and effects | Four boards plus mixed scene, neutral and coloured-light controls | Pasted-on actors, double shadows, unreadable spells or faction art disconnect; revise material/lighting contract |
| H09 | VFX behavior transfers across actors/elements/styles | 24-base-behavior matrix plus selected player/monster and physical/ice/fire variants | Attachment/terrain mismatch, lifecycle drift, changed damage footprint or lost element meaning; repair archetype/adapter |
| H10 | Non-tiled painted environments can extend without visible seams | Two chunks, two chambers, camera traversal and surface transitions | Repetition/seams/scale changes or unacceptable texture costs; revise chunk/material strategy |
| H11 | The production model can support 100+ distinct characters and gear | Broad concept matrix, ten finished characters, two held out, confusion review | Repeated silhouettes, recolour-only tiers or transfer cost explosion; revise identity/faction/gear design space |
| H12 | The complete scene fits runtime and authoring budgets | Live representative crowd/VFX/streaming profile and production receipts | Frame/memory/retry budget exceeded; target the measured cost source before scaling |

## Gate sequence and outputs

| Gate | Work and deliverable | Advance condition |
|---|---|---|
| G0 — scope and durable plan | This document set, source inventory, state and restart prompt | Links resolve; old/new suite separated; next task actionable |
| G1 — source and projection research | Four-game native reference packet, measured framing/uncertainties, matched candidate comparison design | Evidence supports the shortlist; missing editions/provenance identified; visual choices presented to Matt |
| G2 — capability and data proof | Small installed-runtime/tool probes; versioned profile/chamber/asset schema; blockout, logical navigation/collision/state tests; declared budget | Reproducible imports/alpha/attachments and data transitions; no unsupported controls assumed; numerical gates frozen |
| G3 — visual target and painted chamber | Faction direction boards plus candidate projection/light comparison; painted chamber art/data alignment | Matt chooses the shared visual target from concrete artifacts; all relevant geometry/alpha gates pass |
| G4 — motion, gear and interactions | One complete pilot actor + two outfits, larger monster/NPC fixtures, full scripted chamber proof | Identity/gait, objects, contacts, ordering and integration pass in actual playback |
| G5 — reusable VFX | 24-base behavior checks and registered cross-element/actor/style cases | All mandatory cells pass; held cases remain held; controls catch known bad effects |
| G6 — transfer and cohesion | Second chamber/chunk, ten characters across four factions, two held out, mixed combat scene | No per-character exceptions masking systemic failures; distinctiveness/cohesion and interaction tests pass |
| G7 — production readiness | 100-concept coverage, gear inventory model, observed costs and runtime profile | Supported scale estimate, explicit capacity limits and reproducible package; production decision remains scoped |

Gates organize dependencies, not one-session quotas. G1 research and G2 data-schema
drafts may proceed together. Final art generation depends on a registered projection
candidate; roster generation depends on a passing pilot. Expand VFX only after
the relevant motion/attachment mechanism is ready. Read-only research and failure
analysis continue while a visual decision is pending.

## First registered experiment: E01 native source comparison

Purpose: challenge automatic transfer of the recovered Godot camera into a painted
2D world. H01 primary; H08/H10 secondary. No art production in this experiment.

Inputs: [SOURCE_INTAKE](SOURCE_INTAKE.md), four-game native gameplay references,
[Godot evidence](CAMERA_BASELINE.md), [faction key](FACTION_KEY.md).

Sampling plan: for each game, acquire at least one quiet traversal segment, one
combat segment and one stronghold/interactable view. Aim for 5–10 seconds of
uncut motion in each motion category; select at least three useful native frames
per game. A still-only row may inform style but cannot pass a motion/perspective
claim. Use HUD-equipped ordinary gameplay, record edition/version when known,
and exclude cinematic cameras, photo mode, trailers with cuts and zoom mods from
camera measurements. Do not pool original D2 and D2R.

For each source record: source ID, exact URL/path, publisher/capture owner,
edition, dimensions/FPS, native content rectangle, timestamps/frame indices,
hash for local media, evidence role, acquisition date, inspection scope and
confidence. Copies/crops are derived artifacts linked to the native original.

Measurements: tight body height / active viewport height (equipment/FX excluded
and separately annotated), foot anchor fraction, visible ground top/bottom scale
when measurable, ground-plane edge directions, exposed roof/shoulder proportions,
object occlusion examples, readable VFX footprints, HUD-covered area. Report
annotation uncertainty and sample variation. Separate measured image quantities
from inferred camera parameters and design preferences. Absolute metres/FOV are
UNIDENTIFIED without independent calibration; no false decimal precision.

Outputs: labelled visual reference comparison, source manifest, measurement table
with caveats, and a shortlist of no more than three projection/scale candidates
for a painted blockout test. Include Godot as a comparison column labelled
PROJECT REPLICA, never as native Grim Dawn footage.

Completion: all four games have provenance-checked, actually inspected native
evidence for the claims made; unsupported measurements are marked indeterminate;
the proposed test varies projection/framing while controlling body/layout scale.
Do not treat the four games' apparent camera angles as values to average.

Research stop rule: one targeted local search and up to two focused primary-source
search passes per missing category. If blocked, record the missing source and
the precise decision it prevents; continue unaffected work rather than cycling
through unverified thumbnails. Never imply a paid resource was inspected from
its marketing page. No account purchase or upload of project art is implied.

## Numerical and perceptual acceptance contract

At G2, preregister tolerances before rendering the candidate being judged. Use
known-size probes and intentionally corrupted controls to choose detectable,
visually meaningful bands. Thresholds are engineering proposals until frozen;
they are not automatically inherited from original ASTRA or old 3D scoring.

Record at least: projection round-trip error; art/data boundary deviation in
world units and screen pixels; planted-foot drift during a declared contact;
rigid-part size/attachment residual; actor clearance/corner behavior; seam and
temporal phase continuity; VFX spawn/contact timing; object-state latency;
texture memory, live p95 frame time, crowd/effect counts and viewport/hardware.
Dimensions that legitimately change with pose need reference trajectories or
pose-conditioned bounds, not a constant silhouette-height test.

Discrete gates: zero duplicate loot/reward events; zero forbidden paths; every
required approach point reachable in its permitted state; no lost object state;
all declared lifecycle transitions occur; incompatible gear rejected explicitly.

Register a visual rubric with anchored examples for painted quality, anatomy,
gait, faction recognition, individual identity, world cohesion and combat
readability. Review motion at native gameplay scale plus a diagnostic close-up.
The generator's own assessment cannot be the sole perceptual evidence. Use Matt
and, where available, a separate reviewing session given unlabelled candidates
and controls. No internal subagent tree is required or permitted.

Bad controls must include: swelling bag, repeated leading leg, sliding planted
foot, shifted wall mask, corner-cut path, opened door with stale collision,
double loot event, incorrect y-order, detached weapon trail, stuck channel and
wrong-scale ground effect. A metric that passes its known-bad control is invalid;
repair the metric and rerun, not the threshold to rescue a candidate.

## Record for every later experiment

Before execution: ID, gate/hypothesis, exact claim, immutable inputs/control,
independent variable, held constants, method/tool capabilities, sample matrix,
predicted result, pass/fail/indeterminate rules, generation/time/disk ceiling,
allowed repair class and next action for each outcome.

After execution: actual settings, hashes, commands, raw outputs and inspected
frames, observed metrics/verdict, visual review, costs, deviations, falsifiers,
affected hypotheses, dependency invalidations and next action. Distinguish
PLANNED / RUNNING / PASS / FAIL / INDETERMINATE / BLOCKED. A tool success or
complete file inventory is not an art pass.

After two attempts that reproduce the same failure without improvement, stop
that branch, diagnose and register a changed experiment or alternate method.
Do not reset attempt counters or regenerate unchanged inputs indefinitely.
This is a branch-review trigger, not an automatic request for user permission.

## Later experiment records

- [E02 registration](experiments/E02/REGISTRATION.md): user-selected C projection,
  painted-source transfer and component controls.
- [E02 renderer addendum](experiments/E02/RENDERER_ADDENDUM.md): user-requested
  Godot/Pixi comparison and alternatives research, with added limits.
- [E02 receipt](experiments/E02/RECEIPT.json): actual runs, limitations and next action.
- [Shared composition benchmark](experiments/E02/RENDERER_BENCHMARK.md): next
  fixtures and the contract for comparing agent composition capability.

## E02P — third renderer foundation (2026-09-11)

Matt approved Phaser 4 as a test candidate. [Registration](experiments/E02P/REGISTRATION.md) and [report](experiments/E02P/REPORT.md) record the three-batch, zero-generation extension using immutable E02 inputs. Phaser 4.2.1 passed projection/root/socket/basic UI controls; batch-01 capture-size failures remain preserved. G2 remains PARTIAL. Next is E03 painted asset/data agreement across Godot, Pixi and Phaser; no renderer winner or style lock.
