# E07X — practical light response: scoped PASS

Godot is the shipping target; Pixi is the test harness. Selected **A**: the supported wall-top practical with ambient0.55/key0.25, same6m radius/2.2 point strength. F01 remains the timber/stone waystation and F02 the reclaimed rock-cut reservoir; E07W finish A is retained.

## Evidence

- Source slab-ray oracle generated before the consumer capture: 1728 floor/wall equation comparisons across36 views (control/A/B × two factions × native/fresh3× × neutral/warm/cool), all ≤2RGB; maximum 1.362878. Source direct-vs-cell interpolation calibration ≤1RGB (maximum 0.996032) selected samples before GPU readings.
- 768 warm/cool response differences against neutral preserve the expected channel ordering. The independent evaluator includes the existing geometry's point-light blockers. It does not establish arbitrary shadow-boundary interpolation quality.
- 1488 visible core ID probes pass; the same core samples match declared emission in all three light modes. Neutral has a visibly grey core and no point illumination. 3 native and121 fresh3× guarded core pixels are available per faction/view.
- All four missing-fixture/stale-lamp controls detected; emitter projection agrees with the source anchor. State JSON identical across response/resolution/mode for each faction. The source checks support intersection, core/anchor containment and minimum2.79m geometry above current2.7m floor actors and2.5m raised pilot.
- No browser/GL errors in the36-view completed matrix. Native images are960×640; fresh3× images are unscaled780×900 crops from2880×1920 physical renders, with crop coordinates in the receipt. They are not enlarged native pixels.

## Visual judgement

Inspected F01 A/B native warm, F02 A native warm, and F01 A fresh3× warm. A preserves floor tile/wood/rock detail and a readable character. B makes the unlit character and timber structure unnecessarily dark. The small amber core has a visible bracket and local floor/wall response; no bloom or edge halo was added. The practical remains a blocky mechanism fixture, not finished faction prop art. The plain shared room layout and static NPC/monster mismatch remain visible; full faction identity/F03 atmosphere are PARTIAL.

## Preserved failures and limits

Initial source fixture referenced the wrong wall segment and floated above its top; source-v0 is preserved. Corrected support before consuming a renderer build. Build1 failed initialization because the copied adapter omitted its existing shadow-policy module (404). Build2 supplies the byte-identical E07W module; no shader retuning. Two of two consumer builds used; three capture batches including saved-review check; zero generation and paid-service spend. Built-in image-generation price remains unexposed; no generation used here.

Point-light blockers explicitly exclude the emitter fixture's own parent group: an approximation necessitated by its coarse AABBs. The fixture still participates in directional casting and opaque visual depth. No general self/soft-shadow or airborne actor qualification. Shared shadow and player-indicator mechanisms are inherited; their earlier full source matrices were not rerun after adding this small caster. No bloom, new painting, combat lighting, hardware qualification or whole-suite PASS is claimed.

[Comparison](review.html) · [source oracle](evidence/source-oracle.json) · [render checks](evidence/batch-02/validation.json) · [channel checks](evidence/channel-ordering.json) · [fixture data](fixture.json) · [failed build](evidence/capability-build1-failed.json)
