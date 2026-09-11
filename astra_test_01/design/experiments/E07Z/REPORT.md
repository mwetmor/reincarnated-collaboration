# E07Z — per-pixel opaque mesh depth repairs prop ordering

Scoped opaque mesh depth PASS. The actual installed Pixi8.20.1 WebGL context supplies24 depth bits. GPU overlap controls prove order independence, deliberately disabled-depth failure and correct clearing between changed frames. The exact E07D prop geometry/materials/state are retained.

The named Pixi adapter now supplies camera-space depth and homogeneous w in its mesh vertex shader and enables depth tests/writes for opaque geometry. This also supplies perspective-correct texture interpolation. The comparison's depth-disabled control uses that same shader interpolation, isolating depth visibility from UV interpolation changes. Pure sim and neutral geometry/manifests contain no Pixi types.

An independent CPU ray/triangle oracle through actual fresh3× pixel centers selects21 interior witnesses across3 visible brace/band parts. Each witness has a nine-neighbor same-part guard against antialiasing edges. Old painter ordering matches12/21; deliberately reversed painter ordering matches0/21. Depth-enabled normal and reversed submission both match21/21 within2RGB channel values. Source C projection residual remains within0.5logicalpx. These tests qualify sampled opaque parts, not every pixel or every scene state.

Native960×640 and newly rasterized2880×1920 artwork were inspected. Crate braces and both chest bands are continuous, resolving E07D's visible defect without repainting or rebuilding the prop. Full faction architecture and material richness remain plain. Actor sprites still use the earlier approximate ordering and have not gained a full per-pixel depth/transparency/motion proof. Do not extend this result to translucent VFX, all prop states or production hardware performance.

Costs:0new generation calls,0paid services, unchanged local Pixi version. Three bounded capture batches including review; no byte/time-limit violation. Original E07D failed captures and sorting implementation remain intact. [Official API and installed-source evidence](API_SOURCES.md) informed the capability test; GPU pixels govern the pass.

Next: inspect the actual serial-content runtime consumer under its charter and register a bounded read-only JSON/state integration proof. Keep actor/translucent-effect depth and richer faction architecture as separate open tests; do not assume opaque depth has closed them.

[Review](review.html) · [capability](evidence/batch-01/validation.json) · [ray oracle](evidence/part-oracle.json) · [pixel checks](evidence/batch-02/pixel-validation.json) · [receipt](RECEIPT.json).
