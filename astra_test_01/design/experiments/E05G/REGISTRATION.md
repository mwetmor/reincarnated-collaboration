# E05G — modular source gear and occluded sprite composition

Use E05M's unchanged source actions, body geometry, native frames, C camera and hand sockets. Add distinct cuirass/pauldron/helmet geometry with named fit-family/bone bindings. Starter body source remains immutable; advanced pieces are separate. Helmet visibility is independent of equipped state. This is a gear reuse/occlusion mechanism test; final advanced-outfit painting and eight-view fit remain owed.

Limits:60active minutes,2source-authoring revisions,4capture batches,100MB,zero imagegen/paid calls for the initial mechanism proof. Do not paint or render full clip inventory before sparse controls pass. Test idle0,walk.2/.4,cast.3/.6/.9. Geometry-backed front gear layer uses body holdout; base pixels are reused unchanged. Compare with full source composite on matched backgrounds.

Freeze: source base vertex/weight hash and action references unchanged; hard gear dimensions relative to assigned bone vary≤1%; attachment relative drift≤1mm across all216action samples. Wrong-fit family and20source-pixel gear pivot control must fail. Actual layered vs full-reference composite: mean absolute RGB error≤1channel level over occupied sprite pixels and≤2%occupied pixels with any channel error>8. This is a bounded compositing approximation, not pixel identity. Report maximum and distribution; do not hide errors in empty canvas area.

Gear's shadow/diffuse/glossy/transmission visibility is disabled ONLY for this compositing control, explicitly isolating geometry/alpha ordering. Do not infer final gear shadow/light qualification. Body holdout must hide rear gear correctly rather than paste everything in front. Gear/equipment effects remain neutral data; simulation imports no renderer. Headgear-hidden must preserve the uncovered head and equipped-state identity, not unequip it.

Source material probe is matte ivory/brass geometry, not a generated painted advanced outfit. If this representation fails, preserve it and target the measured occlusion/alpha issue before expanding animation or texture authoring.
