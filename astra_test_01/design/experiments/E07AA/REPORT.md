# E07AA — surface field and UV PASS; remaining seam PARTIAL

Godot shipping target; Pixi test harness. Retain candidate **B** for the next geometry test: stronger desaturated damp-stone tint with a gradual world-height transition. This is a scoped field/UV selection; the complete surface is not yet accepted.

The final36-view matrix covers control/A/B, two factions, native/fresh3× and neutral/warm/cool illumination. Every complete geometry-ID image is byte-identical to the matching control; state JSON also remains unchanged. All12 F01 painted comparisons are exactRGBA matches to control. No browser or GL errors.

Independent source camera-ray hits yield94 native and96 fresh3× samples on F02 backing/waterline faces. For each A/B candidate, all380 mask checks pass (maximum0.465561RGB), and all380 two-channel UV checks pass (maximum0.499640RGB), against the2RGB bound. These are190 distinct source positions across two candidate passes. At least16/21 source points lie in the transition for native/fresh. Wrong-height and wrong-UV controls are detected, as is the missing treatment in the original control. Source field samples remain in[0,1]; a0.1mm height step stays within the preregistered continuous-field bound. The two sinusoidal modulation terms are deterministic declared material data; no noise service, image seed or generated texture is assumed.

Inspected A/B F02 native warm and B fresh3× warm/cool. Both remove the hard green skirting look. B gives a more legible damp-stone base while retaining rock texture and local light response. A is too subtle for the intended reservoir cue. The strip and backing now share a planar rock UV field rather than vertically squeezing the strip texture.

A thin straight edge remains around the old shallow strip boundary in the fresh view. Its0.004m protruding mesh is a plausible source; fading tint and aligning texture cannot remove geometry. Preserve this as incomplete surface evidence. Next E07AB will remove only that redundant overlay and repeat source/field/geometry controls, while the continuous material still stains the backing. The disappearance of the edge must be observed before accepting the diagnosis or surface.

Build1 failed before scene capture because a zero phase emitted an integer literal in floating-point GLSL addition. The failed adapter and compiler message remain. Build2 formats the same phase as a decimal float; no field/tolerance change. Two consumer builds and three capture batches (last includes saved-review check), zero generation or paid-service spend. Fresh images are900×960 unscaled crops from2880×1920 renders; native images are960×640.

[Saved comparison](review.html) · [field and render checks](evidence/batch-03/validation.json) · [source field](evidence/field-oracle.json) · [unchanged F01](evidence/unrelated-faction.json) · [neutral treatment](surface.json) · [failed compiler](evidence/batch-02/validation.json)
