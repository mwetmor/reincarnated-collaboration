# T4f — per-skill pierce and contact text

`cliffside_t4f.zip` contains the complete Godot project rebuilt from the read-only cliffside_v19 inputs. `project_files.json` inventories all 869 archive resources by SHA256. Seven dummy assets are targets. Frozen Orb has pierce -1; the other five kits have pierce 0. The range remains 650 world units before the existing character/art scale. All exported scene filtering overrides are LINEAR.

## Run the conductor probe outside the sandbox

Extract the zip into a writable PROJECT directory, then run:

```sh
/Applications/Godot.app/Contents/MacOS/Godot --headless --path PROJECT --import
/Applications/Godot.app/Contents/MacOS/Godot --headless --path PROJECT --script res://probe_pierce.gd
```

The probe writes `PROJECT/out/probe_pierce.json`. The standalone `probe_pierce.gd` is the same file included in the project. The probe temporarily aligns three of the seven existing target footprints eastward in reverse group order, preserving their native shapes. The remaining four targets are moved off that line. Its very-fast sweep case traverses multiple bodies in one tick.

## Interface

`kit.json` accepts integer `pierce`, default 0; -1 is unlimited, positive N passes N bodies and stops at body N+1. Invalid integers below -1, booleans, strings and fractional numbers are rejected. Building the 33-file pre-T4f fixture without the field is byte-identical after removing the single new default field from kit.json.

The shared component keeps its existing acquire/release/resolve_target signatures. `contact_body(area: Area2D, phase: String = "head")` accepts head, chain_hop, field_centre, rim and shard callbacks on the same cast. It records body_index, contact_class, phase, distance and the first-contact strike flag. The swept head orders contacts before dispatch and excludes already-contacted bodies. A cast records at most one contact and one label per body. The impact script gates flash, hit-stop and shake together; later contacts retain impact layers. Labels are pooled, use font 22 with dark outline and palette_3 colour, rise 40 world pixels, and fade for 0.6 real-time seconds independently of hit-stop.

## Verification and limits

The real-scene probe measures unlimited contacts FULL/PARTIAL/PARTIAL, zero-pierce FULL, finite-pierce FULL/PARTIAL and one strike response for each scenario. The explicit chain phase callbacks produce FULL/FULL/FULL; centre/rim/shard callbacks produce FULL/PARTIAL/PARTIAL. Duplicate callbacks do not duplicate labels. Fifteen labels reuse three Label nodes. Numeric measurements are in `acceptance_metrics.json`, `invariants.json` and `probe_pierce.json`.

The baseline G1 component has no automatic chain/shard/rim routing. Those phase classifications are verified through explicit callbacks in one cast, not through autonomous phase producers. No targeting, locking, cycling or tap-to-cast protocol was added. The permitted cliffside_v19 scripts/scenes contain no CAST overlay; this export preserves the T4b directional input emitter exactly, and does not invent an overlay.

The v19 kits predate the material schema. Export reconstruction recovers their four native phase colours exactly into palette entries and preserves native dimensions and alpha; the two legacy particle colours become indices 170/255 in the same kit palette. The foreground is reconstructed from its two existing tiles for the importer, with no resizing. Source files are untouched. `build_export.py` reproduces this adaptation under `tmp/`.

Godot completed the runtime assertions but emitted macOS certificate/editor-settings sandbox diagnostics. Existing unittest wrappers count these diagnostics as reds. Full-suite counts and every red are recorded in `full_suite_summary.json`; focused checks are in `focused_final.log`. The named T4a structural test now exercises the shared component Head, its runtime material/field binding, and all existing impact material assertions.

## Final census

Full suite: 545 tests, 530 successful, 268.085 seconds, 15 red entries. The legacy-byte and CLI focused checks both succeed. The K3 report-only test and named T4a material test are not red. Probe scale 0.541666687, effective range 352.083346 px, maximum label lifetime 0.606004 s.

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
- test_vfx_picker.G1ComponentTests.test_headless_first_cast_contact_cursor_pool_cancel_and_picker
- test_vfx_picker.G1ComponentTests.test_headless_pierce_contacts_labels_pool_and_phase_callbacks
- test_vfx_picker.LivingEmbersTests.test_headless_glow_sixty_samples_extrema_range_and_particle_properties
- test_vfx_picker.VfxPickerTests.test_headless_tab_twice_cast_scene_labels_and_inflight_kit_lock
- test_vfx_picker.AuthoredEffectPickerTests.test_headless_authored_cast_east_north_collision_timing_and_feedback_cleanup
