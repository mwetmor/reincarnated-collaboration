T3o — VFX picker and living embers

The fixture/project directory is a self-contained synthetic Godot project.
From the burst root, import and run the two runtime probes:

/Applications/Godot.app/Contents/MacOS/Godot --headless --path runs/C-3/t3/T3o/fixture/project --import
/Applications/Godot.app/Contents/MacOS/Godot --headless --path runs/C-3/t3/T3o/fixture/project --script res://picker_probe.gd
/Applications/Godot.app/Contents/MacOS/Godot --headless --path runs/C-3/t3/T3o/fixture/project --script res://glow_probe.gd

Unit tests: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:tests python3 -B -m unittest test_vfx_picker -v
Full suite: PYTHONDONTWRITEBYTECODE=1 python3 -B tests/run_t0c.py

Catalogues require 1–12 unique safe identifiers (ASCII letters/underscore,
then letters/digits/underscore; case-insensitive uniqueness also prevents
filesystem collisions). Relative dir paths resolve beside the catalogue.
All catalogue, kit, props and socket validation precedes output creation.
CREDITS_VFX.txt is the exact ordered concatenation, with no added separators.
The exporter report carries that same string in vfx_kits.credits.

The picker captures cast_kit_index before playing the first cast frame.
Tab updates selection and HUD during an existing cast, but neither that
cast's release nor its bolt's eventual impact changes kit.

Glows use level-pixel visual centres. sort_y is the owning prop's anchor y;
the Sprite2D node sorts at sort_y + 1. Without the override, select the
nearest displayed prop centre among props containing the glow, otherwise
the nearest prop anchor (manifest-order ties). With no props, use the glow's
own centre y. Explicit sort_y is recommended for overlapping props. Overhead
glows use their centre directly. Inverse-scaled Sprite2D offsets keep the
visual centre fixed during flicker while the sorting anchor stays fixed.
Each manifest index supplies a stable seed for three fixed random phases.
Flicker multiplies base alpha and scale by the same normalised three-sine
signal; no texture transformations occur.

Particle rect semantics remain [x0,y0,x1,y1], emitting about its centre with
half-size extents and local_coords=false. Optional gravity is level pixels
per second squared; angular_velocity bounds are degrees per second; the
scale_curve endpoints are nonnegative linear multipliers (zero is allowed).
Curve tangent values are explicitly floats for Godot's Variant::FLOAT loader.

baseline_t3m_text_sha256.json was captured before editing the exporter.
The 18-file lock includes a single kit plus legacy props and parallax.
The test fixes only clock readings and legacy set iteration order to the
captured process order, retaining literal byte comparison of every text file.
The diagnosed-attempt log retains the initial curve-tangent problem;
full_suite.log records the final implementation's results.
