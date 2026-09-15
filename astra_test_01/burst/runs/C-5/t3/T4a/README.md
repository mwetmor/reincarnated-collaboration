# T4a shared VFX material

## Delivered interface

`build(effect_json, out_dir)` accepts `material.palette`: four RGBA lists in
low-to-high index order. Visible source RGB must be exactly 0, 85, 170 or 255
in all three channels. Alpha is independent coverage, including opaque index 0.
Defaults: `blend_mode="MIX"`, `light_participation=false`, `erode=0`,
`dissolve=0`. Modes: MIX, ADD, PREMULT_ALPHA. Light participation selects ordinary
CanvasItem lighting or `unshaded`. Blend and lighting are resource parameters:
Godot fixes them in `render_mode`, so the writer emits six variants of one shared
fragment shader. Erode/dissolve and palette colours are editable shader uniforms.

`write_vfx_material(out, resource, material, distance_texture,
dark_duplicate=False)` writes a ShaderMaterial and shader variant.
`shader_source(blend_mode="MIX", light_participation=False)` supplies its source.
`distance_field(rgba)` encodes alpha-weighted radial-distance quantiles around
the coverage centroid. This mapping makes erosion represent removed coverage;
equal-radius pixels share a threshold. Erode 0 and 1 are explicit endpoints.
`material_pixels(rgba, palette, distance=None, erode=0, dissolve=0,
blend_mode="MIX", dark_duplicate=False)` is a CPU reference, not a GPU proof.
Dissolve holds until 0.5, then removes indices 3, 2, 1, 0 at 0.5, 2/3, 5/6, 1.
Retained palette colours do not change.

The builder retains native index PNGs. `phase_scale` is applied to scene
geometry, never a nearest-neighbour raster operation. Each affected sprite uses
LINEAR. Runtime frame/animation changes bind the matching independent distance
texture, with a separate ShaderMaterial instance per sprite. Cast flares,
residuals, floor light, particles and the black MIX duplicate use the same shader.
RGB modulate is intentionally ignored; modulate alpha remains useful for fades.

Legacy `white_core_keep`, `tint` and `pixel_scale` produce named validation errors.
The frozen_orb_v3 kit is tested at both build and load without modification.
Private historical `_tint`/`_tint_particles` helpers remain solely for existing
arithmetic regression tests; the builder/exporter never calls them. Unrelated
non-authored exports and default SpriteFrames serialization retain their paths.
The tests that required retired builder behavior now test its explicit rejection
or the replacement material behavior; no expected-failure/skip decorators added.

## Conductor rendering proof (outside this sandbox)

The ready project is `proof/`. It has seven materials (six blend/light variants
plus the black MIX duplicate), a 64x64 index texture, its distance texture, and
`proof.gd`. Import with Godot 4.6, then execute the script on a functioning
Compatibility renderer. Example commands, with the conductor's Godot executable:

```
godot --headless --editor --path <proof-directory> --import
godot --path <proof-directory> --rendering-method gl_compatibility --script res://proof.gd
```

Use the platform's offscreen/display setup for the second command. A dummy
`--headless` renderer cannot supply rendered pixels and is deliberately rejected.
The script checks the selected renderer, material/shader uniforms, exact palette
colours, opaque index 0, erosion 0/0.5/1, brightest-only dissolve, all six variant
renders, and ADD over an opaque black MIX duplicate in one scene. It writes PNGs
and `rendered/render_proof.json`; nonzero exit means a check was not met. Two
negative controls use `-- --known-bad-dark-index` or
`-- --known-bad-compatibility`. The latter injects an invalid shader and records
its explicit rejection; the former must be caught by measured alpha.

`cpu_reference.json` is labelled CPU-only and retains `passed: null`. It does not
claim that the required rendered-frame checks have run. The Godot 4.6 CanvasItem
reference was not supplied at a readable local path (no matching shader/reference
file was found in the allowed roots); no network access was used. Compatibility
load/render remains a conductor-side acceptance check.

## Output location

SPEC says `runs/C-5/t4/T4a/`; the task explicitly permits only
`runs/C-5/t3/T4a/`. These outputs use the permitted t3 path. No manifest, fixture,
brief, lane, bible, or earlier run artifact was changed.

## Recorded verification

Material tests: 45/45 successful (1.981 s). First full suite: 512 run, 498 successful (254.394 s). Diagnostic full suite: 513 run, 499 successful (249.666 s). The one-test increase is the proof-fixture resource test. Fourteen red records: five standing motif/walk records, seven environment failures, two obsolete CanvasItemMaterial expectations in protected test_vfx_picker.py. The latter assert `blend_mode = 1` in scene text and access `ShaderMaterial.blend_mode`; the targeted timeout capture confirms the invalid property access. K3 is not among recorded reds. Full tracebacks and every red name are in full_suite_diagnostics.json; summary.json classifies them. No acceptance threshold was relaxed.
