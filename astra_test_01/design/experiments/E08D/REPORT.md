# E08D — capacity is unresolved; scenario counts are explicit

The two outstanding inventory interpretations produce **300 or 400 base ensemble designs**, plus either **50 individual unique items** or **50 complete unique sets**. Complete-set scenarios therefore total350 or450 ensembles. These are not authored-piece counts or runtime combinations. Slots, reusable pieces and fit compatibility are unknown; summing them as “350 assets” would conceal most of the production problem.

Measured E08A allocation is8MiB for one view of one48-frame walk. If eight views packed equally, that one clip would require64MiB per actor. Ten such actors resident together would be640MiB;100 would be6.25GiB, before any other animation, modular layer, floor or effect. These are scenario arithmetic, not measured VRAM. The catalog needs residency/streaming and reuse evidence before a capacity claim.

E05B’s48 render samples support only the observed ~1.007s median/~1.058s p95 frame-render cost on the local machine. They exclude the inherited model’s authoring cost, painting, rig repairs, additional views and asset validation. Built-in imagegen prices are not exposed. External paid-service spend remains$0; unknown authoring and generation costs remain unknown.

No production pass follows. Keep broad roster production stopped until the painted pilot and transfer mechanism work. After visual selection, the immediate source-art test is garment visibility/material response on the existing isolated rig; then modular advanced gear and the remaining pilot motions. The ten-character3/3/2/2 batch and two held-out cases must be preregistered after the pilot; no character identities are silently selected here.

See [scenario data](scenarios.json) and [browser summary](review.html). Godot is the shipping target; Pixi is the test harness.
