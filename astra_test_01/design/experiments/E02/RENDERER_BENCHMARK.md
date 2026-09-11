# Shared scene-composition benchmark

User direction recorded 2026-09-11 UTC. Renderer adapters: Godot and Pixi.js required;
Phaser 4 recommended next from primary research. The comparison concerns agent
composition ability. It does not reopen combat design or replace pipeline output.

## One portable input contract

Keep original combat JSON and its hash intact. At the boundary, present each
renderer with the same logical entity snapshots and timestamped visual events.
The exact adapter must be derived from a real current pipeline output before
integration; E02's chamber JSON is a diagnostic fixture, not that output schema.

Keep engine-independent: projection C parameters, logical metres/heights, chamber
geometry/state, source image bytes, pivots, directional/frame rectangles, socket
coordinates, material tags, light policy, event IDs/times and effect lifecycle.
Keep engine-specific: texture import, scene nodes, masking/sorting implementation,
shader/blend bindings and screenshot/performance capture. Gameplay outcomes must
not depend on the rendering choice.

## Staged common fixtures

1. E02 foundation: same C projection and PNG, fixed/following camera, nine positions,
   true ground circle, source-root/socket transforms, known bad controls. Implemented
   in Godot and Pixi; final per-component results are in validation.json.
2. One source-conditioned painted chamber floor plus split tall prop; cross in
   front/behind it and expose previously covered floor. Preserve layout constraints.
3. One actor with starter/advanced gear attached to the same qualified motion;
   idle/walk/cast, including hidden-head toggle. Use the identical frame/time data.
4. Projectile/impact, ground field and weapon trail with identical spawn/stop times,
   socket paths and stone/soil transitions. Same painted textures and lifetimes.
5. Door/crate/chest state transitions and reward events from the same scripted
   event trace. Keep the original chamber's required assertions and negative controls.

These stages remain gated by the suite plan; existing failed animations cannot
silently become passing benchmark inputs. Diagnostic use must carry their failure
status. Do not create different art for each renderer to hide assembly differences.

## Scoring and required evidence

Record visible defects before any aggregate score: art/data edge disagreement,
foot/socket errors, wrong ordering, mask seams, alpha fringe, double shadows,
effect clipping, lifecycle mistakes and nondeterministic replay. Existing frozen
tolerances remain binding; preregister missing motion/state/performance thresholds
with detectable bad controls before that stage is rendered.

For composition capability, measure completed requested edits, manual interventions,
failed attempts, verified repairs, capture reproducibility and artifact portability.
Use the same edit tasks: move a doorway, replace a prop state, swap gear, retime an
impact, change a surface response. Counterbalance which renderer is edited first.
Report authoring and inspection time separately from generation/tool wait time.
Do not count engine-generated stand-ins as successful painted deliverables.

For performance, fix viewport/hardware, texture bytes, actor/effect count and
overdraw. Capture live p50/p95 frame time and memory under the same replay. A saved
video's frame rate is not a performance result. Startup/setup cost is a separate
one-time item. Numeric scores are not yet assigned because only foundation data exists.

## Exact next experiment

Register E03 with a C-matched floor/material anchor and a single painted tall prop
from the draft chamber, plus the smallest view-conditioned actor control needed to
remove E02's legacy-camera confound. Freeze art/data and alpha tolerances and the
generation ceiling before calling imagegen. Load the same accepted bytes in Godot
and Pixi; add Phaser's foundation adapter before comparing its richer effects.
Use a new experiment registration for representation changes such as projected
painted planes; do not relax E02 controls or silently relabel its results.
