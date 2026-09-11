# E07C — padded shadow domain

Scoped domain/interaction PASS. The current fractional pilot floor shadow now survives the crate, chest and exterior-apron fixtures. Godot is the shipping target; Pixi is the test harness. Full scene lighting, actor visibility, art and production scale remain unqualified.

The allocation is derived from the full floor bounding rectangle (a conservative superset of valid actor roots), current caster radius/height, directional light and 0/0.5 m altitude. Outward whole-metre rounding gives [−9,−5,11,7], 2560 × 1536 pixels. All 144 extremal combinations fit; the old domain fails the crate approach. The 7.8125 mm texel pitch and original grid alignment remain unchanged. The measured device maximum texture size is 16384; the adapter rejects requests above it. Fifteen MiB RGBA8 allocation is arithmetic, not actual VRAM/process residency evidence.

All 640 original independent visible-floor witnesses pass. The 16 interior comparison crops have eight changed pixels in total, each differing by one channel level; worst MAE is 7.30994e-7 and fraction over eight levels is zero. No source, geometry, simulation or light-policy changes were made.

New boundary cases cover crate, raised cast at crate, east/west apron extremes, the other faction's crate, and chest. 440 available camera witnesses pass, with lit material samples unchanged and positive samples darkened. Missing/stale controls each reject all 20 positive samples wherever positive camera witnesses exist. The west apron has zero acquired visible positive shadow samples at both resolutions; the wall hides its floor in this camera view. Its camera-positive control is explicitly unavailable, not passed.

To verify that allocation independently of camera visibility, 240 additional mask-space source ray/triangle witnesses cover all six cases, with nine-neighbor guards. All pass, including the hidden west-apron case; missing and stale controls fail at least one positive sample in every case. The diagnostic reads the actual mask through the locally inspected Pixi 8.20.1 extraction implementation, whose WebGL path returns raw framebuffer pixels; no assumed orientation was used to select evidence. This addition is diagnostic-only consumer build two.

Actual chest/crate/door buttons, shadow and raised toggles, all intended fixture positions, and three continuous-root walks pass with no browser/GL errors. Both factions' shadow-disabled geometry-ID images remain exactly equal to the earlier E05F baseline. Warm/cool consistency probes retain point-light contribution while removing the key contribution. The moving shadow improves ground attachment in inspected native video sequences; hard edges, occluded actors and plain chamber materials remain visible limitations.

Two acquisition failures remain:

1. The inherited source oracle initially left external exits closed. Correcting that state mismatch did not restore west-apron positive camera witnesses; the initial causal attribution was incomplete. Open-exit partial evidence records zero positive / 20 lit samples at both resolutions. The mask-space proof does not relabel the unavailable camera control as a pass.
2. Initial boundary capture carried its deliberately stale offset into the next fixture before resetting controls. The inherited guard rejected that diagnostic state at the east boundary. Ten completed native captures and their failed receipt are retained. Resetting diagnostics before placement recovered only the missing 20 native cases. The fresh matrix has all 30 cases. No production rendering rule was weakened.

The first analysis labelled the unavailable camera control with a true boolean despite an explicit no-claim note. That report is retained as `pixel-validation-initial-label.json`; the corrected report uses null and gates only available camera controls. Direct mask controls remain separately mandatory and pass.

Three registered capture batches contain interior continuity, boundary/mask/UI/playback, and review. No generation or paid-service calls occurred. Sixteen images and three videos load from the standalone review. E07B failures and all earlier source evidence remain intact.

Next E07E: a bounded shared directional-shadow capability proof for opaque chamber geometry and the current pilot, including vertical receivers. Then continue stronger floor/wall lighting, richer faction architecture, visibility policy, modular/animated content and the VFX matrix under separate limits. Do not infer full-suite PASS from this local repair.
