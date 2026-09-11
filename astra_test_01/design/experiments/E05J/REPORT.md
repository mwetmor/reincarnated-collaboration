# E05J · Sparse depth-bearing gear transfer passes

The existing Pixi harness can render this painted source as shared geometry, a shared bone palette and separately selectable gear. All288source-oracle comparisons pass at eight directions,50/150body-axis pixels, three sparse poses and both helmet states on three backgrounds. WorstMAE=.314765; worst fractionerror>8=.0126266, within unchanged1/.02pixel tolerances. Bad20px gear shift and wrong pose palette are detected.

This changes the tested representation. It does not rehabilitate E05A/E05O's failed independent RGBA reconstruction, nor qualify full painted art. Textures are unchanged copies; no body painting or animation was regenerated per outfit. Godot remains shipping target; Pixi remains the test harness, with no added3Drenderer dependency.

## Independent evidence

The neutral export contains64,549vertices,104,380triangles,132source meshes and14materials. Blender evaluated geometry is the reference for idle0,walk12,cast36.30,351sampled vertices agree with rest-geometry/bone deformation within.000000677m. References contain evaluated positions/normals, independent of the GPU skinning calculation. The rendered comparison uses the same diagnostic material policy on both paths; it is not a Cycles lighting comparison.

Seven corrected capability controls and10contract checks pass. Bone arrays fit the actual1024vertex-uniform-vector limit; depth buffer24bits. Gear/head selection preserves shared rest buffers/textures. Supplemental starter idle image is included; it is not a complete second-outfit animation matrix. The36-entry palette consists of35actual bones plus a static rig transform entry.

## Preserved failures and corrections

Exporter revision1 failed Python parsing and wrote no assets; revision2 fixed parsing and completed export. Both revisions counted. In the first GPU probe, the custom vec3`uColor` collided with Pixi's reserved mesh vec4uniform. Renaming it`uProbeColor` removes GL_INVALID_OPERATION; every corrected probe reports0GLerror. Do not interpret the instrumented debug probe's consumed error flag as the fix.

Initial near.1/far100depth produces54draw-order-dependent pixels. Holding geometry/screen projection/materials fixed and narrowing this isolated character's clip interval to10–40m makes reversed order pixel-exact, while all288source comparisons still pass. Every exported vertex across all3poses/8headings lies at depth22.2081–24.3406m. This supports depth precision as the cause in these samples. Validate a full world range separately before adopting its clip planes. Last-batch allocation changes are recorded; no fifthbatch.

## Scope and costs

No image generation or paid-service spend. Typed geometry/oracle/palette assets10,038,136bytes; unchanged texture sources8,446,727bytes. Three sparse palettes total6,912bytes. Body and gear painting/motion remain reusable source assets; full animation streaming/import/residency still require tests.

The final16figure comparison collage uses192–256material draw meshes; measured CPU composition plus synchronous GPU finish median.75ms,p95~1.90ms,max~2.90ms on this local run. These are probe observations with cold/warm builds mixed, not a gameplay frame-time or production hardware pass. Source art still looks too simple and its raw minification is visibly grainy/jagged. Material response is diagnostic albedo+diffuse, not final painted lighting. No full G4/G6/G7promotion.

Next: bound E05Q native sampling/sharpness comparison for this representation, holding source art/geometry/camera fixed. Test geometry antialiasing and material minification against the F04 clarity target before further art/detail changes. Full painted pilot and animation inventory remain open.
