# E05Q · Select antialiasing and mipmapping for continued tests

B reduces error against the fresh3×reference in all8registered cases and visibly reduces grain/jagged edges. Actual MSAA is4samples forB/C,0forA; onlyBhas mip chains and anisotropy8. Source geometry, painting, rig and character display scale are unchanged. No obvious ivory/brass/blue color bleed or white alpha fringe appears in the inspected idle/hidden/dark and cast/helmet/light views. Full painted art and temporal shimmer remain unqualified.

A is native no-AA/no-mips. B is native MSAA+mips. C is freshly rendered3×geometry withMSAA/no-mips. C is not a resized A/Bimage. Its exact3×3channel area mean is used only for measurement. This finite9sample reference is not absolute art truth. After framing correction, worst sceneMAE versus that reference is7.7581forA and3.1227forB; the selection bar is relative improvement≥6/8cases, not E05J's different source-geometry equality test. B improves8/8.

## Framing failure preserved

The first800pxstrip clips the final casting hand. Both E05J source and skin paths shared that layout, so their288comparisons demonstrate captured-pixel agreement, not full-pose coverage. The old images, reports and measurements remain; E05J now carries an explicit subsequent finding.

The corrected strip is1440×460; C is4320×1380. Character sizes remain50/150logical body pixels. All32geometry-bound checks for the two registered poses (idle/cast×8headings×2scales) leave≥5pxframe margin. A supplemental16case check on the uncaptured walk pose finds its final150pxview would still exceed this strip by2.744px. That wider-motion framing remains held; use pose-derived bounds rather than reusing a fixed strip width in the next review.

## Interpretation and limits

A native full-screen render can use more geometry samples, as C shows. Enlarging a low-resolution screenshot cannot produce the same result. Texture resolution, UV allocation, camera scale and missing sculpted/painted detail still limit what is visible. The simple armor/hair/cloth do not match the final F04art bar merely because their edges are cleaner. No full-screen production hardware claim follows this local static probe.

Both allowed adapter revisions and3actual capture batches used (initial matrix, initial savedreview, corrected wide matrix+review); numbered folders reflect purpose, not quota usage.0generation, no paid service. All source artwork is unchanged. B's neutral policy is in sampling.json. Next: integrate the depth-bearing pilot with chamber geometry under one camera-depth/light policy, testing front/back occlusion and interaction states before more visual detail or animation inventory expansion.
