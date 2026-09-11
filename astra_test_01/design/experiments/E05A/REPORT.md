# E05A · Better fit, failed layer transfer, art still open

The helmet now exposes the face and fits within a narrower/lower source envelope. Helmet-hidden state restores the intact E05H hair, with the same advanced torso/shoulder selection. The second shoulder revision replaces rounded pads with tapered planes. Body mesh, weights, rig actions and camera are unchanged.

This is not an advanced-outfit or painted-pilot pass. The armor remains too simple and block-like compared with F04, and the body retains a smooth low-detail appearance. Painted albedo alone does not establish F04's shaped plates, folds, straps, material separation or identity. No animation or roster expansion follows this turnaround.

## Measured results

-11 headless/source checks pass, including hashes for56 source frames, eight actual rig rotations, neutral manifest and state invariants.
-4 actual Pixi delivery/state checks pass.
-49/96 layer/reference composites pass;47 fail the previously frozen MAE≤1 and fraction error>8≤.02. Worst MAE1.89326, fraction.0546684.
-Visible helmet failures15/48; hidden helmet failures32/48. Hair restoration adds a distinct composition dependency.
-Deliberate20source-pixel head shift fails (MAE8.8524/fraction.13368). Keeping hair through the fitted helmet also fails (MAE1.20578/fraction.02857), visibly exposing the bun.

The difference view localizes errors around hair/head, shoulder tips and body/armor overlap. Separate holdout renders plus ordinary alpha-over do not reproduce the full source render closely enough here. Shared silhouette coverage, denoising and secondary illumination are candidate causes, not proven diagnoses. E05G's older sparse result remains true for its own source and poses; it did not prove this representation universally reusable.

## Reproducible inputs and limits

Source E05H `head-shell-v1.blend`; F04 style reference; one built-in generated1254×1254 RGB material atlas, preserved unchanged with prompt/hash. No native alpha claim for this albedo atlas; source renders are native RGBA. Material UVs stay within inset third-panel rectangles. No upscaling.

One of2 generation calls, both source revisions and4capture batches used. Batch2 includes revised full reference renders as registered in BATCH2_REVISION.md. No fifth capture. No paid API/service spend; built-in generation price unexposed. Gear secondary rays remain disabled as in E05G; no gear lighting qualification.

Named Pixi adapter owns sprites/visibility mapping. JSON manifest describes frames, pivots, directions, hitboxes, emissive-null paths, atlas rectangles and explicit hair inclusion/exclusion. The two-field diagnostic sim is JSON-in/out, with no rendering import. This does not replace the actual combat boundary audited in E09I.

Next: register a narrow layer-visibility diagnosis with source sample/denoising controls and independently checked alpha coverage. Preserve these failures and thresholds. Full character art still needs a different shaped-detail method before animation expansion.
