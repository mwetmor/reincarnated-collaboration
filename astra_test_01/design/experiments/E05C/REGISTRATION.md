# E05C — short-garment visibility and clean material probe

Use the chosen F04 gameplay clarity target and F03 environment-light reference in ../../VISUAL_TARGET.md. This is a local source-authoring probe over an isolated E05B rig, not generated painting or a new faction character. Godot shipping target; Pixi test harness. No edits to original assets.

Freeze cameraC,2m physical reference,2m/s,.8s gait, E05B rig action/soles/accessories. Change only lower garment geometry/piping and a labelled clean material variant. Register original long garment as control. The clean variant must not hide failures with blur, post-upscale or softened alpha. Preserve skin/face source and body identity.

Limits:90active minutes,2garment revisions,2material revisions,4capture batches,100MB,zero imagegen/paid calls. Render previews before full frames. No expansion to eight views without the pilot pass.

Measurements: actual deformed-sole stance drift≤.02m; sole penetration≤.001m; bone-length residual≤.001m; attached book transform stable within.001m. Bad detached-book control must fail. Camera projection agreement≤.01 native-buffer pixel. A supporting boot must remain discernible through each stance half-cycle at50px gameplay and150px inspection. Test actual raster visibility with foot-ID occlusion diagnostics and visually review native color motion. A numerical visibility pass is not an aesthetic pass. Compare clean material appearance with F04; preserve FAIL/PARTIAL if low-poly shape, rigid cloth or material response still differs.

Candidate1 raises panel/trim hems together to clear shin/boot without moving root or feet; shortens front tabard proportionally. Material1 removes projected front/back cloth images only on garment meshes and uses matte slate cloth, aged brass trim and worn leather while retaining facial identity. This is a 3D material hypothesis; it does not manufacture hand-painted artwork. F03's room light-spill proof is a later chamber test, not inferred from this character render.

Before batch02: render48 color frames and48 boot-ID depth-occluded frames each for short garment and restored-long control, same camera. Supplementary visibility floor: at least1 integrated opaque-equivalent boot pixel at50px body reference for the planted side. This floor detects complete concealment; visual discernibility remains a separate unchanged gate. ID colors use emission, one sample, no denoising; native color uses unchanged16-sample denoising. No final art pixels are edited.
