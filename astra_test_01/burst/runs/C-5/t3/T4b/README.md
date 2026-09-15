# T4b G1 effect component

Unzip painted_project.zip or grey_project.zip into a writable directory.
The source cliffside_v19 scene was not modified. Seven dummy assets have target=true.
The supplied scene contains six catalogue kits (the task referred to seven legacy scripts).
The legacy CLI catalogue remains supported; single-kit defaults retain the frozen regression bytes.

Run outside the sandbox:

    /Applications/Godot.app/Contents/MacOS/Godot --headless --path PROJECT --import
    /Applications/Godot.app/Contents/MacOS/Godot --headless --path PROJECT --script res://probe_vfx.gd

The probe writes PROJECT/out/events.json and PROJECT/out/probe_vfx.json.
Events use age_frames at 60 Hz from release, independently of hitstop time scale.
The synthetic dummy fires on scene load, before the first physics frame; the probe also tests
an existing live dummy, nearest/cone/range rules, cursor fallback, pooling, cancel, missing
resolution rejection, and Tab selection. The engine can report macOS certificate/editor
settings errors inside the sandbox; these are retained in test logs.

The runtime component uses one AnimatedSprite2D head and Line2D trail. A swept head
footprint prevents fast travel from skipping thin target footprints. Impact scenes retain
kit-specific layers, hitstop, and shake. Touch position is transformed into world coordinates.
Grey body PNGs have RGB 128 and unchanged alpha; body material recolouring is disabled.

Exports live under runs/C-5/t3/T4b because the task's explicit write restriction excludes
its conflicting runs/C-5/t4/T4b output instruction. Project zips include per-file SHA256 inventories.
The v19 material metadata used retired tint/pixel_scale; this copied export migrates it to a
four-entry cold palette without changing source art or source files.

## Remaining verification concerns

Full suite: 520 tests, 505 successful, 197.296 s. Full names and diagnostics are in
full_suite_reds.json. Five standing motif/walk entries remain; nine headless checks
encounter sandbox logging/certificate/editor-settings errors. One further material
test in test_effect_kit.py opens the retired per-kit bolt scene. That test file is
outside T4b's edit scope and was not changed. The K3 report-only test is not red.
Focused suite: 22 tests, 19 successful; its three engine wrappers report only the
sandbox diagnostics after completing all runtime assertions.
Both live exports register the first cast and real dummy contact with 0-frame lag,
zero unresolved releases, zero cursor error, and zero probe assertion errors.
