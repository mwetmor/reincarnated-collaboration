# T4c deterministic replay and native bake

## Delivered instruments

- `export/godot_import.py`: optional `bake=False` parameter and `--bake` flag; default exports retain their bytes. Bake installs a transparent 512×512 viewport, 60 Hz physics, scene-visibility hook and replay probe.
- `export/replay.py`: `prepare_project`, `install_hooks`, `movie_command`, `run_replay`, `replay_to_frame`, `background_comparisons`, `compare_bakes`, `scene_pixel_probe`, `compare_vo1`, and `diagnose`.
- `oracle/sheet_pack.py`: strict `numbered_frames` and lossless `sheet_pack(frames, out, columns=8, pivot=(256,256), fps=60)`; no trim/resampling, full RGBA cells and unchanged pivot offsets.
- New stdlib unittest modules cover corrupted/missing/shifted frames, encoding differences, scene leakage, bad dimensions, alpha roundtrip, pivot offsets, per-frame VO1 tolerance, and legacy export bytes.

## Replay recipe

Run from the burst root, using a **new empty output project**, never T4b in place:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m export.replay \
  --source runs/C-5/t3/T4b/painted_project \
  --project runs/C-5/t3/T4c/tmp/project_new \
  --out runs/C-5/t3/T4c/tmp/bake_new --bake --frames 126
```

The executable recipe includes `--write-movie <out>/fx.png --fixed-fps 60`. The project has `rendering/viewport/transparent_background=true`. No headless render substitutes for this recipe: the macOS headless driver is a dummy renderer. `probe_only=True` measures runtime state without pixels and is labeled accordingly.

`replay_to_frame(project, out, frame=N)` starts a fresh process and re-instantiates the effect. It seeds the global RNG and each supported particle emitter **before** adding the effect to the tree. It advances actual 60 Hz physics frames and records the observed age alongside the requested age. The default effect is the supplied frozen-orb **impact component**, origin (2285.62,2407.32), seed 1, crop 512×512. Cast/travel orchestration is not implicitly claimed by this impact probe. Hit-stop remains active; frame age is measured from engine physics ticks rather than elapsed scaled seconds.

Two independent `run_replay` calls produce bakes for `compare_bakes`. `scene_pixel_probe` requires a separately rendered `blank=True` negative control; checking only an effect alpha bbox cannot prove scene exclusion. `background_comparisons` captures live and flipbook runs on ground, black, white and a supplied native foliage crop. Feedback runs live in flipbook comparisons while effect art is hidden; the baked image is screen-space to avoid applying camera shake twice.

Feed independently computed **frozen VO1** values for those captures into `compare_vo1`; this burst was not authorized to read/redefine the VO1 implementation. Missing measurements remain unevaluable, and uncommitted bands produce null judgments. Do not substitute an RGB-error metric for VO1. Additive layers flattened to RGBA may be background-dependent; the instrument does not repair or conceal that limitation.

## Evidence and limits

`headless_summary.json` records a real engine execution at native 512×512: requested/observed physics frame 30/30, 60 Hz, 91 hidden scene drawables, zero reappearing scene drawables, floor light live, hit-stop scales 0.1 and 1.0, and 3 px camera shake. This is structural evidence, **not a scene-pixel measurement**.

Godot 4.6.3 runtime introspection confirms both CPU and GPU particles have `use_fixed_seed` and `seed`. The permitted GPUParticles2D API declarations were also extracted locally with Godot's documentation tool. The requested `creating_movies` prose docs were unavailable within the allowed local inputs; no web was used. CLI flags were checked against the installed engine's `--help`.

Graphical Movie Maker startup aborted with signal 6 twice, in 0.212 s and 0.081 s, with empty stdout/stderr and no frames. The same engine runs the headless probe. This isolates the obstruction to graphical startup, but does not identify an OS/driver cause or establish effect nondeterminism. No particle substitution, layer removal, frame repair, cached-frame substitution or false empty-image comparison was used. The conductor retains the E0(b) decision.

Consequently byte identity, rendered scene exclusion, and per-frame VO1 ±5% on four backgrounds are **unmeasured**. The source inventory is a diagnostic list of possible timing/randomness sites, not evidence that any listed site caused nondeterminism. A supported graphical runtime is required to finish those measurements.

Outputs follow the explicit task path `runs/C-5/t3/T4c/`; the SPEC table's `t4/T4c/` spelling was superseded by the task write restriction. Large copied projects, extracted API trees, and runtime temporaries are removed after evidence is collected.

## Full-suite accounting

The direct full command reported tests_run=539, successful_tests=524, elapsed_s=203.276228. An observed repeat recorded 14 assertion/subtest outcomes and 1 error, with no skips. The 19 new synthetic tests are all green. `test_k3_combat_report_only` is not red. Every red outcome follows; complete tracebacks are in `suite_observed.json`.

- test_every_material_sprite_is_linear_and_animation_fields_are_bound (test_effect_kit.SharedVFXMaterialTests.test_every_material_sprite_is_linear_and_animation_fields_are_bound)
- test_headless_state_machine_input_map_gear_vfx_and_nearest_fallback (test_godot_import.GodotImportTests.test_headless_state_machine_input_map_gear_vfx_and_nearest_fallback)
- test_synthetic_contract_and_grid (test_oracle_walk.Tests.test_synthetic_contract_and_grid)
- test_f04_outside_at_least_three (test_oracles_motif.Tests.test_f04_outside_at_least_three)
- test_named_genuine_annuli_retained (test_oracles_motif.Tests.test_named_genuine_annuli_retained) (center=[113, 201])
- test_named_genuine_annuli_retained (test_oracles_motif.Tests.test_named_genuine_annuli_retained) (center=[111, 311])
- test_named_genuine_annuli_retained (test_oracles_motif.Tests.test_named_genuine_annuli_retained) (center=[170, 253])
- test_headless_cliffside_follow_camera_parallax_and_projectile_collision (test_parallax_scene.ParallaxSceneTests.test_headless_cliffside_follow_camera_parallax_and_projectile_collision)
- test_headless_occlusion_fade_restore_overhead_near_and_particles (test_props_layer.PropsLayerTests.test_headless_occlusion_fade_restore_overhead_near_and_particles)
- test_headless_tower_import_run_and_physics (test_scene_kit.SceneKitTests.test_headless_tower_import_run_and_physics)
- test_headless_directional_release_and_resources (test_sockets.SocketTests.test_headless_directional_release_and_resources)
- test_headless_authored_cast_east_north_collision_timing_and_feedback_cleanup (test_vfx_picker.AuthoredEffectPickerTests.test_headless_authored_cast_east_north_collision_timing_and_feedback_cleanup)
- test_headless_first_cast_contact_cursor_pool_cancel_and_picker (test_vfx_picker.G1ComponentTests.test_headless_first_cast_contact_cursor_pool_cancel_and_picker)
- test_headless_glow_sixty_samples_extrema_range_and_particle_properties (test_vfx_picker.LivingEmbersTests.test_headless_glow_sixty_samples_extrema_range_and_particle_properties)
- test_headless_tab_twice_cast_scene_labels_and_inflight_kit_lock (test_vfx_picker.VfxPickerTests.test_headless_tab_twice_cast_scene_labels_and_inflight_kit_lock)
