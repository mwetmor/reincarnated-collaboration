# E05U · Part-specific gear improves; full pilot art fails

One native1536×1024RGBatlas supplies distinct painted front/back torso, shoulder, helmet, bracer and greave surfaces. Fitted bracers/greaves and ornament improve the advanced outfit over generic swatches. Both source revisions pass144idle GPU/source comparisons apiece under unchanged limits. The full pilot still fails the selected F04art bar. Godot is the shipping target; Pixi is the test harness.

The fitted bracer/greave core surfaces retain more than10.10mmminimum signed clearance in12registered idle/walk/cast source checks (2,310vertex samples). Shell thickness is3mm, bevel1.5mm. This is a sampled core-fit result, not exhaustive outfit intersection proof. Base geometry/weights/actions are unchanged in revision1; revision2 preserves all geometry/weights/actions while replacing two residual royal-plum shoulder materials with existing painted cloth and its recorded UV projection. No second generation was needed.

Independent Blender export samples31,128positions in V1and31,176in V2; maximum source/skin error6.44e−7m, topology preserved, dropped weight0. Eight-view starter, advanced helmet and advanced hair-restored cases on dark/light/blue backgrounds at50/150pxbody-axis scales pass all144comparisons per revision. V2worstMAE.068952,fractionerror>8=.000976 versus unchanged1/.02limits. Bad20source-pixel gear shift fails (V2MAE28.9271,fraction.58691). These compare independent Blender-evaluated positions/normals under the same Pixi diffuse policy, not Cycles/PBR lighting equality.

All48source-pose/view/scale framing bounds pass in each revision with>=5pxmargin in1600×460strips (200pxcolumns). This avoids the prior shared-crop failure. Bsampling is actualMSAA4withmips/aniso8. Eight native runtime checks and6saved-review checks pass; GL/page errors absent, favicon404only.

## Visual findings and stopped expansion

All eight headings were inspected through native advanced hair-restored/light, helmet/blue and starter/dark strips, plus selected Cycles source views and the final repaired starter/light strip. Ivory/brass/navy surfaces and fitted greaves are clearer; no obvious white halo appears in the inspected light/blue views. Ornament reads at gameplay sizes without the old generic blank cuirass. Revision2 removes the residual purple shoulder color, including visible areas beneath advanced plates.

The saved review compares F04and candidate crops at approximate150/50pxvisible height. Reference camera, anatomy and lighting differ; it is a style comparison, not projection equality. Original image pixels are unchanged and only downscaled. Native eight-view strips remain unscaled with horizontal scrolling.

That comparison leaves substantial art failures: the broad smooth coat lacks F04's layered cloth/material separation, and the dark hair mass has a simplified/block-like rear silhouette. Full advanced outfit fit, full pilot, all motions and shared lighting are unqualified. The existing shader uses diffuse material response; exported roughness/metallic are metadata, not proven PBR. No animation/roster expansion occurred. Batch3was used for the diagnosed material repair, as registered, rather than motion transfer.

One of two allowed built-in calls used, both source-author revisions and all four capture batches. Known external paid spend0; built-in price unexposed. Native generated atlas and source files remain intact. Latest source: inputs/part-painted-gear-v2.blend; latest neutral export: v2/character.asset.json. Prior V1and all old failures preserved.

Next E05W must change the failing base-art method: separate ivory linen/navy cloth/leather/hair surfaces, improve the hair silhouette while preserving head clearance, and recheck source fit/eight-view readability. Rig/actions and proven gear stay reusable; explicitly register any base-geometry changes and their regressions. Do not retry the exhausted independent-RGBA branch or expand inventory before full pilot art passes.

[Saved review](review.html) · [Receipt](RECEIPT.json) · [Artifacts](ARTIFACTS.json).
