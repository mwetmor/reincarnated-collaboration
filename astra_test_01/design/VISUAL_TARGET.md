# Working visual target — Matt, 2026-09-11

> I like the themes of all four scene images, but the cleanest style for gameplay is F04 rather than the shared style. My favorite scene is F03 for detail and theme, and I also REALLY like the way the lighting glows on the floor/walls. F01 and F02 seem to show too many brush strokes or pixels or something.

This supersedes Codex's mixed-scene recommendation. **F04 is the gameplay clarity/style anchor. F03 is the preferred environmental detail/theme and local light-spill reference.** All four faction themes remain liked. F01/F02's conspicuous brush/pixel texture is not the target.

Use clean material planes and readable small silhouettes, restrained surface texture and clear floor/navigation regions. Preserve F03's architectural richness and localized glow on receiving floors/walls. These are implementation interpretations to test against the referenced images, not additional user rulings. F03's industrial theme remains F03's faction vocabulary; do not convert all four factions into foundries.

The user identified a visual texture problem, without diagnosing whether it is brush marks, pixelation or resampling. Do not claim a technical cause from this preference. Keep native-size/fresh-render controls. Do not blur the assets to hide texture, sharpen them indiscriminately or bake universal white rims. Local illumination must follow source/receiver/occlusion state; drawn glow in a concept board is not that proof.

References: [F04](experiments/E07V/art/F04.png), [F03](experiments/E07V/art/F03.png), [all boards](experiments/E07V/review.html). Projection C remains the authorized test camera. Godot is the shipping target; Pixi is the test harness.

Scope: shared working scene direction is now selected. Actual painted character/material transfer, runtime light response, layout agreement and final production style remain to be proved. The response does not explicitly delegate every future visual decision (D07). Existing authorization continues bounded technical and art tests under this chosen direction; do not ask again to use it.

Further binding review guidance: [faction separation and reversed doorway evidence](experiments/E07V/FEEDBACK_2026-09-11.md). Differentiate F01/F02 stronghold construction, not just palettes or banners. Subsequent painted exits must prove interior/exterior side agreement with layout data.

Blood impacts: Matt prefers the splatter accompanying F01’s fire VFX. See [the recorded reference and scope](experiments/E07V/FEEDBACK_2026-09-11.md#preferred-blood-hit-reference); element rendering and target blood response remain separate data.
