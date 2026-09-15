# T3t effect-kit builder

`export.effect_kit.build(effect_json, out_dir)` accepts a dictionary or JSON path.
JSON asset paths resolve beside that JSON; dict paths resolve from the current
directory. `sheet` is a validated source PNG; each `frames[].file` explicitly
names a frame PNG. The schema has no crop rectangle, so no atlas grid is guessed.
Cast, travel and impact are required; residual and individual layers are optional.
Travel defaults to 520 px/s and no streak. Holds are integer 60 Hz ticks.

## Review fixture

Extract `synthetic_fixture.zip` under `tests/tmp/` or this burst's `tmp/`.
Open `acceptance_fixture/project/project.godot` in Godot 4.6. E/left mouse casts;
Tab changes the authored frost effect and legacy frost kit. The archive includes
relative `kits.json`, explicit 16x16 source PNGs, all compiled layers and a copy
of the read-only legacy kit with its credits/license. No source artwork changed.

Run the engine probe after importing the project:

    Godot --headless --path <project> --import
    Godot --headless --path <project> --script res://effect_probe.gd

`effect_probe.gd` tests E/N socket releases, actual sprite rotation, ground
squash, frame durations, speed, collision impacts, time-scale restoration after
early deletion, camera offset restoration, and body/residual/flash/light cleanup.
Engine editor-settings and certificate errors remain visible inside the sandbox.

## Measurements

`acceptance.json` records numerical fixture measurements. `targeted_suite.log`
records the final 15 focused tests. `full_suite.log` is the exact requested
runner invocation; `full_suite_final.log` reruns that runner with result-event
capture, recorded in `suite_details.json`, to identify every red on final code.
All result-envelope `passed` fields are null; no conductor gates were changed.
