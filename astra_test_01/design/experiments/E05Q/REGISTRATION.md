# E05Q · Native character sampling and clarity

Godot shipping target; Pixi harness. E05J sparse geometry correctness passes; raw image exhibits aliasing/grain. Hold source image/geometry/bones/camera/light/outfit fixed. No new art generation.25active minutes,0generation,2adapter revisions,3capture batches,45MB.

Three labelled controls: A current native1×no-AA/no-mips; B native1×MSAA with mipmapping/anisotropy8; C freshly rendered3×MSAA/no-mips reference. C is new geometry rendering, not image enlargement. Inspect idle0 and cast36, eight directions, visible/hiddenhelmet, dark/light,50/150logical body axis. B must preserve the same geometry/state/texture hashes.

Measurement: compare A/B against per-channel3×3area averages of C on foreground union; B must reduce mean absolute error in at least6/8matched scene cases (2poses×2headstates×2backgrounds), without obvious material-color bleeding or erased meaningful silhouettes under visual inspection. This is a finite9sample reference, not an absolute art truth. Preserve full-resolution C; any area averages are measurement-only, not new source artwork. Inspect brass/ivory/cloth borders and hair. Bad control A is required to show edge aliasing; neither algorithm can qualify missing art details.

Batch1 all matched A/B/C sampling cases. Batch2 conditional material-boundary/repaired sampling controls if needed; batch3 savedreview. No animation/roster expansion. If B trades aliasing for material bleed, register revised atlas-safe sampling rather than calling blur acceptable. Native fullscreen sharpness remains conditional on actual viewport/camera sizes.
