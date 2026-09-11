# E07E — shared scene-shadow capability checkpoint

Capability preflight PASS; integrated consumer FAIL after two builds. The current working chamber remains E07C. Godot is the shipping target; Pixi is the test harness.

The measured WebGL path supports an explicit depth24/stencil8 offscreen attachment. Nearest depth survives reversed draw order; disabling depth admits the wrong surface and is detected. Empty-map clearing and asymmetric orientation pass. All 64 RGB depth encoding probes stay within 10 micrometres over 32 m; maximum measured error is 1.558805 micrometres. This is a capability result, not an integrated scene-shadow pass.

The neutral light-space policy encloses 1,992 source/extremal points for both the existing back-side key A and labelled front-side key B. Each map requires 28,835,840 color bytes plus the same depth/stencil allocation arithmetic. Actual residency and production hardware remain unqualified. Neither lighting choice is promoted to final art.

Integrated build 1 emitted subtraction of a negative bound as a decrement token. Build 2 parenthesized scalar literals, exposing a second compile error: packed is a GLSL reserved identifier. Both eight-image smoke sets, console errors and GL failures remain. The images contain only the older sprite fixtures because the new geometry shaders did not initialize. They are failed evidence, not a visual comparison of the two lights. No integrated source-ray or interaction gate was promoted.

A one-line rename to encodedDepth is prepared in proposed-reserved-word-fix.patch and was not applied to this closed consumer. The initial permission question was unnecessary: EXPERIMENTS.md explicitly treats the two-attempt stop as a branch-review trigger permitting diagnosis and a changed registered experiment, rather than an automatic permission request. Matt's continuing-campaign authorization already covers reasoned local repair. No unanswered question is treated as approval.

Next E07F: one compiler-gated repair build, retaining E07E's two-build count and all failures. Apply only the prepared reserved-identifier correction in a new owned consumer copy, reject shader/GL errors before saving scene comparisons, and carry forward E07E's frozen source/receiver/negative-control gates. Total shared-shadow builds will be three, not reset to one. No generation or paid-service call occurred.
