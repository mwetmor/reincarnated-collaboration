# E07H — denser raw lookup is the selected candidate

At doubled map density, raw depth lookup passes all 1,302 available source witnesses. The receiver-plane configuration still fails two shoulder-armor samples. Both results are retained; E07C remains the working chamber until the selected raw configuration is installed and tested through actual interactions. Godot is the shipping target; Pixi is the test harness.

One consumer build changed only map dimensions to 5,632×5,120 and pitch to 3.90625 mm. World bounds, geometry, lights, 2 mm normal offset, 5 mm compare bias, source guard and 2 RGB tolerance are unchanged. Cumulative shared-shadow builds: five.

The primary corrected matrix passes 1,300/1,302, with the same two fresh 3× armor samples at green 128. Its raw mode records zero failures. The separately recorded raw-mode matrix tests all 24 states plus missing scene, missing pilot, stale root and reversed-order controls. All 1,302 raw-mode witnesses pass, all three negative controls are detected, reversed order is invariant, and no sampled Jacobian or GL/browser error occurs. The primary failure is not overwritten.

The CPU geometric-plane density prediction did not predict the GPU derivative result. It is insufficient evidence for that correction on small curved armor triangles. The denser raw lookup is therefore selected for the next test. This selection uses an already exposed mode; E07H does not add a second consumer build merely to make it the default.

Each active RGBA8+D24S8 map accounts for 230,686,720 bytes by format arithmetic, four times the previous allocation. Dimensions are below the measured 16,384 texture limit, and all captured shader paths render without GL errors. Whole-app GPU residency, minimum hardware and production-scale performance remain unmeasured.

Groups without six lit and six shadow samples remain unavailable. A sampled matrix pass is not full self-shadow qualification, soft-shadow proof or final lighting/style acceptance. Interaction/video expansion is deferred to E07J, which will express the selected raw mode in neutral JSON, assert the renderer applies it, and test chamber controls/playback. No generation or paid-service call occurred.
