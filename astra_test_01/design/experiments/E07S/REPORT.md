# E07S — exact exit geometry with reusable painted materials

Scoped geometry, state and light mechanisms PASS. Complete painted chamber art FAILS the selected F04 clarity/F03 detail and glow target: architecture is plain, chest/crate are still cube placeholders, and actor shading is not integrated. This is not a production or full chamber pass. Godot is the shipping target; Pixi is the test harness.

F01 uses the delegated defended timber-and-stone waystation; F02 uses the reclaimed reservoir. Two generated opaque material plates replace full-scene generation: timber and low-contrast rock. Existing E04S floor materials and explicit E05M/E04M2/E04 actor fixtures are reused. Geometry, typed identity, exit leaves and interior/exterior regions come from JSON exported from E07R's source scenes. Original paintings and the failed full-scene branch remain intact.

## Evidence

42 headless checks pass across both factions and both exits, including closed collision, open traversal, occupied closure, region identity and stale collision/reversed-region controls. Four additional browser command sequences at fresh 2880×1920 confirm closed exits reject the move and open exits allow it. These move a frozen-pose fixture; they do not prove gait or complete character occlusion.

16 GPU object-ID witnesses per batch agree with independent source-camera ray casts, including the foreground leaf and both exterior aprons. The maximum sampled mesh interpolation projection error is 0.111 logical pixels against the frozen 0.5 threshold. Analytic source doorway corner comparisons are below 0.001 native pixels against 3 pixels. The deliberately displaced rendered doorway is caught independently through its GPU ID-mask centroid: approximately 35.1 native source pixels displacement. Analytic corner metadata alone does not measure that injected renderer fault.

Actual receiver RGB at [3,0,0], native batch02: neutral [115,95,76], open warm [149,113,82], open cool [124,111,98]. Closing the leaf returns warm and cool to neutral exactly. The ignore-leaf light control and wrong-foreground-order control fail as intended. Fresh3× repeats all six pixel checks; RGB varies with sampling, but the same blocking/restoration relationship holds. These are sampled witnesses, not exhaustive visibility proofs.

Batch01 is retained. Batch02 declares mipmapped linear minification and anisotropy in neutral material data; the installed Pixi adapter applies those settings. This visually reduces timber/rock noise at native resolution. Iron now multiplies all illumination by its albedo rather than adding colored light to an already darkened value. No source images were resized or repainted. Two originals are 1254×1254 RGB, despite requesting 1024×1024.

## Art limits and next method

Fresh3× buffers are newly rasterized, not enlarged screenshots. This improves surface detail; it does not create absent detail in actor source frames. The NPC is mostly occluded behind the pillar, and the three actors have different material response. No global white outline is added to materials, but moving actor edges and shared lighting are not qualified here. The floor tiling, block architecture and sparse surface detail remain conspicuous. F02 does not yet communicate a convincing excavated reservoir.

Continue a separately bounded geometry-owned detail/interactive-prop test; add recognizable chest/crate geometry and faction-specific structural detail against unchanged doorway/collision witnesses. Do not restart full-scene generation or label typed cube IDs as recognizable props. Independently test the existing pilot and sparse gear in eight source-derived views before increasing animation inventory. Full combat-pipeline integration, all VFX, second chamber/chunks, roster and capacity remain open.

[Saved browser review](review.html) · [headless checks](evidence/headless.json) · [native GPU checks](evidence/batch-02/pixel-validation.json) · [fresh3× GPU checks](evidence/batch-03/pixel-validation.json) · [source oracle](evidence/source-oracle.json) · [receipt](RECEIPT.json).
