# Evidence-backed lessons — E05P

- **Identity persistence does not establish gait quality.** Source-region torso/bag and 19/19 kinematic/JSON checks coexist with visually rejected legs and a rigid upper body. Evidence: batch05 and motion-validation.json. Confidence high for this SE fixture; no claim that every mesh rig fails.
- **Straight-body gait authoring can make planted feet misleading.** The first implementation held soles still while targets exceeded leg reach by0.157m. A stance metric alone would miss the defect. Evidence: geometry-v1/failure.json. Require reach/length checks alongside contact, then actual raster inspection.
- **Completing hidden art and masking it are separate costs.** One generated trouser underlayer supplied missing pixels, but its first mask retained magenta. The corrected mask removed that defect while the walk still failed. Evidence: batch02/batch03 and source-receipt.json. A tool-success count is not a completed rig-part count.
- **Pose-dependent body height should come from the motion model.** Continuous reach-derived pelvis placement improved the geometric construction over fixed crouch, yet did not rescue the painted motion. Evidence: geometry-v2 and batch05. Do not promote the improvement to an animation pass.

Next falsifier: explicit pose-key artwork must independently satisfy foot contacts, identity/gear reuse and normal-speed gait. Its guide positions are not generated-pixel measurements.
