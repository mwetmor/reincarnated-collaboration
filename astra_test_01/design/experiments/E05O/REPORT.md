# E05O · Independent-layer branch still fails

None of the three final GPU composition methods passes all96cases. Corrected geometry-mask partition composition fails57/96 (worstMAE1.78431, fractionerror>8=.0401146). Ordinary native alpha-over fails34/96; display-size alpha-over fails46/96. E05A's earlier47/96fail remains preserved. No gear/motion/style gate advances.

The two-view native-source probe was insufficient to predict the complete GPU result. Cached16sample/denoised alpha-over fails8/12;128sample/no-denoise fails5/12. The combined hair-secondary-off/tighter-holdout condition passes12/12 under both ordinary-over and mask accumulation. That combined change does not isolate masks as the cause. The full eight-view/two-scale test falsifies broad acceptance of all these variants.

Batch3's custom offscreen shader initially inverted Y. Its96partition comparisons and negative controls are invalid for evaluating the representation. The source/reference and ordinary-over captures are independent and retain their measured verdicts. Adapterv1/pixels are preserved. Batch4 fixes the orientation and repeats only the partition cases/controls alongside saved review, as registered in PREPARATION_FAILURE.md. No fifth batch.

Corrected bad20px helmet shift fails (MAE11.4628/fraction.13284); opposite-heading visibility mask fails (MAE5.8907/fraction.20919). Native800×460 buffer, local review images and no browser errors pass. Nine source/manifest checks pass, including64frame hashes and unchanged source. These checks do not override raster failure.

The body painting is shared between head-visible/hidden states. Geometry-derived masks add16mask images to this idle proof. Each512×512 RGBA intermediate costs1MiB nominal;8views×2head states costs16MiB per cached composition method. This is byte arithmetic, not observed VRAM or a production residency pass. No new generation or paid service. Hair secondary rays and gear secondary rays are disabled in this isolated probe; lighting remains unqualified.

## Branch decision

Stop iterating independent denoised/holdout RGBA layers without a changed representation. Source-over changes and added visibility masks have not met the fixed tolerance across the matrix. Keep both E05A/E05O failures. A justified next research branch is depth-bearing painted source geometry or common-sample component output: preserve one rig/motion and separate gear assets, but avoid reconstructing partially overlapping surface samples from independently shaded RGBA frames. Register a small capability/transfer test before implementation; do not silently replace the Pixi harness or claim a new production renderer.

Full painted art is independently open: primitive armor/face/hair/cloth detail does not yet match F04. Source geometry can improve reuse mechanics while still failing art. Roster and full animation expansion remain stopped.
