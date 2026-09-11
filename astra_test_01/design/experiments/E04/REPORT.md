# E04 findings — logical interaction proof, unresolved visual integration

Godot is the shipping target; Pixi is the test harness. The E03 codex-selected-winner selects the test workflow only. E04 exercised the C-projected painted chamber through actual Pixi 8.20.1 / Chrome 152 / WebGL ANGLE Metal on Apple M2.

## What passed, with scope

- 82/82 headless chamber checks: conservative clearance for 0.35m/0.65m actors, swept collision, permitted approaches/exits, perimeter directions, corner controls, door ownership/state, crate ownership, single chest reward/pickup and persistence. This is a chamber fixture, not an integration of the serial combat pipeline.
- 17/17 JSON boundary checks: deterministic state in/out, no input mutation, sim-owned movement and event/effect clocks, serialization, finite-JSON and fixture-mode controls, no rendering imports/DOM in sim, adapter consumes only the public boundary.
- 14/14 manifest checks: eight actual runtime-consumed source manifests plus six corrupt controls. PNG hashes/dimensions, atlas bounds, pivots, still timing and engine-neutral fields verified. This does not pass the artwork or qualify missing animation/emissive data.
- Final actual browser replay: 39/39 checks, zero browser errors. Both actor sizes traversed via actual canvas clicks and swept simulation movement. Occupied closing was rejected, crate/chest/loot state changed, reload retained exactly-once events. Static front/behind-pillar frames were inspected; full H06 airborne/loot/crossing motion coverage is still incomplete.
- Flash/tint declarations changed 960 actor pixels each, bounding box [467,246,496,301]; flash expiry restored the exact baseline. Real idle-time expiry tested. Unsupported glow is explicitly reported; glow/outline implementation remains unqualified. This is not reusable animated VFX qualification.
- Standalone saved HTML review: 25/25 checks, including six resolution/filter choices, 17 scene choices and recorded video decoding. The file review works without a dev server; live interaction requires the documented local server.

The final approximately 12s live demo within the 15.12s capture used explicit fixture teleports for selected cases. Observed p50/p95 frame interval ~16.7/16.7ms and composition CPU ~0.5/0.7ms. No target hardware/crowd/resolution budget was approved; these numbers are not a shipping performance PASS. The prototype reconstructs view objects on changed frames and is not a production rendering optimization.

## Sharpness control — Matt's question

[Registered control](RESOLUTION_CONTROL.md), [raw results](evidence/batch-02-resolution/resolution.json), [labelled comparison](review.html).

Same original textures, projection, logical 960×640 framing and exact JSON state; backing buffers 960×640 versus 2880×1920. 4/4 instrumentation checks passed. The mage is visibly sharper when freshly rasterized at the higher dimensions. Smoothing an already rendered 50px-ish actor to 150px blurs it; nearest-neighbor makes the small pixel grid conspicuous instead. Fresh sampling uses available source pixels rather than enlarging that 50px raster.

The 1536×1024 floor remains visibly softer in the high buffer: its source detail is already exceeded. Higher display resolution cannot invent painting detail. Fullscreen therefore does not inherently require blurry characters, but stretching the low buffer would retain the blur. Final output size, aspect ratio/framing, texture/mipmap policy and floor/chunk texel density require a separate target-resolution qualification. Native game exemplars are not resolution/coverage/sampling-matched to these diagnostic crops; no source-game sharpness ranking is supported.

## Pale edges and lighting — explicit defects/gaps

Matt reports that assets separate from one another/background through white or translucent-looking edges and lack lighting/shading cohesion. That feedback prevents visual acceptance; it is not erased by the numerical interaction pass.

The [dark/light/blue mask board](evidence/batch-02-resolution/current-mask-backgrounds.png) confirms obvious pale background retention at portions of the mage coat contour. Its original RGB has a baked checkerboard. Correctly clipping outside a polygon does not guarantee clean pixels inside its traced boundary. E03's outside-mask pixel checks cannot establish this wider art-quality claim, and a ≤1-native-pixel contour allowance does not override rejected cohesion at the intended display scale. The high-resolution control exposes rather than cures this failure.

The NPC hand area initially looked like another pale contamination patch. Inspection of its dark-background original shows real pale skin; its current polygon takes an incorrect route through the hand/coat region. The issue there includes lost anatomy/incorrect contour, not proven white source-background leakage. Do not apply a blanket colour-removal operation to both failures. Monster outer contour looks less contaminated in this board, but that is not a production alpha pass.

Bright wall/pillar edges include painted mortar/bevel highlights, repeated source face borders and strong top/side material contrast. Texture mapping repeats/stretches those features across procedural face quads. The exact contribution of sampling seams versus baked highlights has not been isolated. No claim that all pale edges have one cause is justified.

There IS baked painted shading and a simple procedural actor contact ellipse. There is NO qualified shared light response, structural cast/contact shadow system, actor/environment illumination agreement or coloured-light material response. These H08/G3 tasks must be tested explicitly; animation, gear, resolution or VFX does not automatically repair them. Neutral effect declarations provide a portable control surface, not a lighting solution. Loot remains a gold diagnostic dot; sliding poses remain frozen.

## Preserved implementation/measurement failures

The first JSON movement test failed at x=0.3: an approximately 1e-17 floating-point remainder entered another movement iteration, then looked like no movement and erased the route. Fix: stop consuming budgets below 1e-9. Original 16/17 result and source retained beside the corrected 17/17 result.

Source review found that view ticking depended on the selected actor's route and ignored idle effects. It now ticks while any returned route/effect is active. Original adapter retained; the final browser test proves idle flash expiry. No pre-fix browser failure is invented.

Source review also corrected a manifest naming error: E03's [890,489] socket is a staff grip, not the top. E04 now distinguishes staff_grip from a separately annotated still staff_tip [917,155] ±6 source px. No release animation attachment is qualified.

## Next action

First finish bounded source-coordinate contour repair/control review (mage coat and NPC hand), preserving current masks and source pixels. Then separately register/test the shared light/shadow/material response at an explicit output resolution. See [next test preparation](NEXT_TEST.md). Keep Matt's visual target decision pending; the workflow agreement was not visual approval.

Then resume the planned separate pilot motion/modular gear and reusable animated VFX tests in Pixi. Motion/gear remain hypotheses: a frozen sprite or a clean mask cannot pass gait, hidden regions or reuse. VFX expansion still requires the relevant qualified attachment/release mechanism. Do not restart old ASTRA generation, repeat exhausted E03 batches, broaden into other-renderer VFX or invent paid-service authority.
