# E07O — visibility capability remains failed

Mask geometry, orientation, alpha composition and negative controls pass in build2, but GL errors remain. No chamber visibility art is produced or promoted. E07J remains the working chamber. Godot is the shipping target; Pixi is the test harness.

Build1 attaches a single-sample depth texture to a multisampled color target, causing incomplete framebuffers. Instrumented clear/draw/resolve calls identify GL1286. Reading the installed Pixi implementation confirms that RenderTarget with colorTextures and depth:true allocates a matching multisample depth renderbuffer. Build2 changes to that path; the seven mask/composite/control checks now pass.

A remaining GL1282 is traced to Pixi's mesh uniform4f upload against this adapter's custom vec3 `uColor`. This repeats the collision already recorded in E05J. The diagnosis is retained: prior naming knowledge was not applied to the new module. Do not count the diagnostic run's zero final getError as a pass; its wrappers consume and record the error.

The two consumer-build cap is reached. Stop E07O without a third build. E07P is a separately registered repair: rename the custom uniform to uIndicatorTint, audit custom adapter names against Pixi mesh-reserved names, rerun the tiny capability gate, then integrate only if it passes. A/B styles remain planned amber fill versus selective outline; no perceptual choice has yet been earned.

No generation or paid service call occurred. Offscreen mask storage also includes multisample buffers, so the initial 16 bytes/pixel value is only a lower bound, not a full allocation/residency claim. Correct that accounting with the repaired capability. Failed source, images, GL traces and original module remain intact.
