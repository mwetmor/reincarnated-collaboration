# E04L — lighting mechanism proof, style still provisional

Godot is the shipping target; Pixi is the test harness. Recommend B as the neutral lighting test baseline, with restrained warm/cool fixtures supplied as scene data. Original paintings and C framing remain unchanged; E04M2 v3 contours are consumed from neutral manifests.

## Evidence and limits

12/12 final browser checks cover unchanged sim state across light variants, body lift with fixed ground contact, detached-contact rejection, object-owned cast-shadow changes and overlap compositing. 12/12 headless geometry/boundary checks cover height-aware light blocking, open-gate transmission, declared shadow displacement and test-only elevation state. 6/6 actual receiver/playback checks and 8/8 standalone review checks passed. The receiver test samples a source-registered mage chest pixel: closed gate B/warm both [42,30,22,255]; open gate B [42,30,22,255], warm [45,31,23,255]. These are actual rendered pixels, not only state assertions.

Opaque caster silhouettes are combined before their shared alpha is applied. The isolated GPU control retains equal single/overlap darkness; the deliberately wrong per-shape alpha becomes darker and is rejected. The mage's body moves upward at a 1m elevation fixture while its contact ellipse anchor remains in ground space. Open gate and broken crate stop owning solid caster pieces; other owners remain. A source-review issue in the E04 demo selector is also fixed here: the displayed selection now matches the internally selected mage.

The first point-light implementation did not occlude entity tint. Its source and batch-01 renders remain preserved. Final entity/ground receivers use geometry/height rays; structural faces additionally use their actual plane normal. A first numerical visibility probe at the very edge of the light radius expected a visible 8-bit colour change below quantization; that invalid instrument failed 11/12. It was preserved and moved to an interior probe before the final run, without weakening the unchanged visibility criterion.

Actual playback remains a frozen-pose mechanical fixture. Observed frame p50/p95 ~16.7/16.8ms; composition CPU p50/p95 ~2.8/3.1ms at 2880×1920 backing resolution, isolated Chrome/ANGLE Metal Apple M2. This is not an approved crowd/shipping performance budget. Recordings include explicit fixture placements and a real-time demonstration.

## Visual assessment

Inspected A/B/warm/cool high-resolution captures, the corrected receiver cases, lifted-body state, shadow controls and saved review. Grounding and a shared light response improve upon the painted-only assembly. B is a useful neutral baseline; warm/cool lighting changes a local area while closed geometry blocks the tested receivers. None of this removes baked mortar/bevel highlights or repeated stone face borders. The floor's native 1536×1024 detail ceiling also persists.

Actor cast shadows approximate an upright painted card; actor light response is a flat approximation, not a generated normal map or reconstructed anatomy. Only the ground receives cast silhouettes in this implementation; wall receiving shadows and detailed materials remain unqualified. Full four-faction cohesion, moving-gait integration and final visual target are still open. Agent recommendation is not fabricated Matt approval.

## Recorded storage failure and correction

The high-resolution browser PNG encodings exceeded the registered 100MB ceiling after batch 03: observed peak at least 107,089,050 bytes. This is a real limit deviation. No capture was deleted and no criterion lowered. Codec-only lossless PNG repacking reduced retained evidence to about 67MB, with original/new encoded hashes and exact decoded-pixel equality recorded in `evidence/lossless-packaging.json`. Generated source images and historical experiments were untouched. Four of four capture batches and zero imagegen/paid calls were used. Do not describe this run as having stayed within its original storage ceiling.

Continue E05P limited-view persistent-layer motion/gear proof under its separately registered criteria. Four-faction and final style decisions remain tracked; independent preparation proceeds while the asynchronous visual-delegation question is pending.
