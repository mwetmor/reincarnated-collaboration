# T3r fly swarm tooling

Changes are limited to `export/props_layer.py` and the T3r additions in
`tests/test_props_layer.py`. `fixture_project/` is a generated synthetic Godot
project; `fixture_inputs/` retains its source PNGs and manifests.

## Contract

Optional `swarms` entries require name, texture, position, radius_px, count,
speed_px_s, land_time_s, flight_time_s, and jitter_px. `sort_y` is optional and
defaults to position[1] + 1; an explicit value is used directly. Counts are
integers 1 through 40. Radius, speeds, and time bounds are finite and positive;
time/speed ranges are ordered. Jitter is finite and nonnegative. Unknown keys,
invalid names, escaping paths, non-RGBA PNGs and invalid values are rejected by
load_props before build_project creates its output.

A Node2D under Actors supplies the fixed y-sort anchor. Its local centre offset
preserves the requested level-space centre. Its Sprite2D children use stable,
build-generated per-fly int64 seeds. The generated fly_swarm.gd runs independent
FLIGHT/LAND clocks at physics ticks, with substeps and random initial prewarming.
Targets use a 60% inner-half-radius disk / 40% outer annulus distribution,
uniform by area within each region. Flight jitter uses independent 8–14 Hz
sinusoids on both axes. Displayed positions are constrained to radius+jitter.
On a flight timeout, the reached position becomes the landing target without a
teleport. Landing twitches have amplitude 1–1.4 px (within the contracted 1–2).

## Evidence

- `t3q_baseline.json`: captured before edits; 12 text-file hashes for the T3q
  fixture. The unittest locks collection order and timing, matching prior locks.
- `headless_samples.json`: initial sample plus 180 deterministic 1/60-second
  physics advances in the actual Godot runtime, for all five flies.
- `acceptance.json`: measurements with null verdicts, two-run repeatability,
  engine return codes and complete diagnostic messages (excluding duplicate
  sample payloads). T3r import and both probe runs returned 0. macOS certificate
  and editor-settings sandbox errors remain visible in the log evidence.
- `full_suite.log`: output of the mandated unmodified full-suite command.

LAND counting uses runtime state boundaries and checks the displayed trace:
minimum sampled duration 0.14 seconds, total position diameter below 3 px.
Initial partial LAND bouts are excluded. FLIGHT means are displayed path
length divided by time, measured inside each bout; transitions are excluded.
The 60 Hz duration estimate is a lower bound, making the minimum-duration check
conservative. Identical traces compare all samples for all fly pairs.

## Reproduce

From the burst root, with bytecode disabled:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:tests python3 -B -m unittest test_props_layer.PropsLayerT3rTests -v
    PYTHONDONTWRITEBYTECODE=1 python3 -B tests/run_t0c.py

The fixture builder is `build_t3r_fixture(directory)` in tests/test_props_layer.py;
its CLI is `--fixture-t3r DIR` and expects a fresh directory. For the retained
project, run Godot headless with `--import`, then `--script res://probe.gd`, using
an explicit log file under T3r/tmp. Generated import caches were removed.

The requested reference cliffside_v9/scenes/frost_bolt.tscn was absent. No
substitute reference was read, and the existing project and VFX kit were not
modified. The T3r row has synthetic acceptance only; no real clip is specified.

## Full suite result

Both runs: tests_run=446, successful_tests=434 (runner counting). Runtime was
189.823838708 s and 186.191324 s. Diagnostic addSuccess counted 436 methods;
the runner subtracts all three annulus subtest entries independently. There
are 12 red entries in 10 methods, all within the named standing categories.
All 7 T3r tests are successful. Full names and traces: suite_diagnostics.json.

- test_godot_import.GodotImportTests.test_headless_state_machine_input_map_gear_vfx_and_nearest_fallback
- test_oracle_walk.Tests.test_synthetic_contract_and_grid
- test_oracles_motif.Tests.test_f04_outside_at_least_three
- test_oracles_motif.Tests.test_named_genuine_annuli_retained (center=[113, 201])
- test_oracles_motif.Tests.test_named_genuine_annuli_retained (center=[111, 311])
- test_oracles_motif.Tests.test_named_genuine_annuli_retained (center=[170, 253])
- test_parallax_scene.ParallaxSceneTests.test_headless_cliffside_follow_camera_parallax_and_projectile_collision
- test_props_layer.PropsLayerTests.test_headless_occlusion_fade_restore_overhead_near_and_particles
- test_scene_kit.SceneKitTests.test_headless_tower_import_run_and_physics
- test_sockets.SocketTests.test_headless_directional_release_and_resources
- test_vfx_picker.LivingEmbersTests.test_headless_glow_sixty_samples_extrema_range_and_particle_properties
- test_vfx_picker.VfxPickerTests.test_headless_tab_twice_cast_scene_labels_and_inflight_kit_lock
