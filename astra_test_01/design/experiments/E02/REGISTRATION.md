# E02 — C perspective painted-sprite transfer probe

Registered before candidate runtime rendering, 2026-09-11 UTC. Open Codex lane.
User chose: “Let's test the problem by using "C" and see if it's a real issue.”
This selects C for a test, not a final art/camera approval.
Prior E01 G1 evidence gaps remain; this authorized probe does not erase them.

## Claim and controls

H01: determine whether a single painted character image, reused in C's perspective
field, produces visible floor/body disagreement. H06 secondary; G2 partial capability.
C parameters and layout are immutable E01 snapshots in INPUTS.json. B is a matched
parallel-projection diagnostic control only, not a competing priority.
Start with the original ASTRA S idle frame (existing alpha; immutable bytes). Its
historical depicted camera is NOT qualified for C. This first stage can isolate
position-dependent changes relative to the center, not qualify absolute center
viewpoint or a final painted floor. Diagnostic geometric floors remain labelled.
No animation qualification: translate a frozen pose; never call that walking.

Two camera policies: stationary room camera; exact ground tracking keeping the
actor at the original center anchor. Sample center, depth +/-3m, lateral +/-3m,
and four diagonals at +/-2m in camera ground coordinates; retained chamber limits
are checked. Use 2m actor and central projected vertical stature 9.5% of 405px.
Legacy root=(256.25,399.5), upper hood=(256.25,176), source axis=223.5px.
These are registration proxies, not measured anatomy or a recovered camera.
Sprite representation: upright screen-facing Sprite2D with one uniform scale
per world position from the projected 2m vertical extent. No local limb edits,
no per-position generated drawings. This source-plane approximation is explicit.
Known-volume reference: 0.6m x 0.4m x 2m cuboid, same root and C projection;
compare true corners against its center image translated/uniformly scaled.
This bounds only the chosen cuboid, not hidden character anatomy.

Freeze before render: root/attachment arithmetic tolerance <=0.5 px at 720x405;
projection independent matrix agreement <=1e-8px; alpha border=0, actual transparent
and opaque pixels present; scale-only cuboid corner residual >2px flags a material
geometric approximation for review (not automatic art rejection). Negative controls:
root shifted 8px, socket shifted8px, scale multiplied1.25, frozen center ground
circle used off-center. Each relevant instrument must reject its planted fault;
otherwise its verdict is INVALID. Ground circle true projection residual <=0.5 px.
Record apparent viewing angles and projected body width/height variations, without
inferring source anatomy. Report full sample range, not only the center.

Visual rubric at native720x405 plus explicitly enlarged diagnostic views: do feet
float, do bodies lean against vertical props, do exposed shoulders/hood look pasted
on, do edge placements feel different from center? Compare with B using identical
art. Agent inspection is provisional; final perceptual acceptance needs Matt review.
Existing legacy camera mismatch is a confound, not a rejection of C.

## Tools, limits, stop conditions

Godot installed version probe; use Node2D/Sprite2D and explicit projection of layout
vertices, no production 3D rigs. Preserve PNG alpha via normal runtime loading.
Inspect renderer output; headless dummy-renderer success is not visual proof.
Python may calculate geometry, validate/hash/read images and write code/records;
it does not edit paintings. Runtime texture transforms are the tested renderer.

Maximum 2 built-in imagegen calls (0 initially, at most one new C-conditioned
source plus one targeted alpha/viewpoint repair if needed); no CLI/API fallback,
no invented seed/mask/paid account. Register exact prompt and inputs before any call.
Maximum 45min work, 200MB owned artifacts, 6 render batches (<=5min each), at most
2 fixes per repeated identical failure. Compile fixes are separately recorded.
No new paid-service spend authorized. Built-in call cost, if used, is UNKNOWN
unless exposed. Preserve every failed candidate; no old-run repair loop.

PASS only the measured component supported by evidence. Overall H01 remains
INDETERMINATE without C-qualified art/painted environment and perceptual review.
If clear positional failure: test a changed sprite mapping under a new registration.
If small/no visible failure: continue C chamber pilot; do not switch to B on theory.
If capture unavailable: retain runnable project, mark playback UNVERIFIED.
