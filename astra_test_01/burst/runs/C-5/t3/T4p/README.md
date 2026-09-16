# T4p E1 projectile arms

`kits_v9.json` entries 9 and 10 are `fire_bolt_e1_A` and `fire_bolt_e1_B`.
Both kits carry the complete supplied skill spec, indexed P01/P02 textures,
independent alpha, screen-pixel placement, and an explicit impact dependency.
Export the catalogue with `export.godot_import.build_project(..., vfx_kits=...,
sockets=...)`. A single-kit export is rejected because the bound impact must be
present in the catalogue. The impact binding validates template, seed, palette,
layers, and screen-pixel placement against `fire_burst_e0p_v2`.

Travel uses the shared G1 event, collision, pierce, and label implementation.
Its opt-in subclass has a head, streak, dark duplicates, and a brief cast halo.
The +x head uses its tip as the origin, the alpha-bounds rear as the streak
socket, and runtime downscales to the spec's 1.2 BH head / 2.0 BH streak extents
at 130 px/BH. Source PNGs remain 512 square and are never resized. The streak's
length multiplier clamps speed/spec-speed to 0.6–1.4. Only band 3 flickers, held
for two ticks per state. An independent horizontal distance texture erodes the
streak from its tail over nine 60 Hz ticks after contact, range, or cancellation.
A draining projectile is unavailable to the pool until its tail finishes.

Aim is captured once at release. Cursor distance selects direction, not range;
travel ends at the first contact or 520 px. Range exhaustion has no contact
burst. The reused pieces impact is instantiated once on contact; FULL/PARTIAL
labels remain the T4f implementation. Victim tint restores after 0.15 seconds.
The enabled hit-stop uses the spec's one contact frame as duration, a 0.1 time
scale, and the existing tree-owned, overlapping-stop restoration pattern.
Both arms use identical layers and all identical mechanics.

## Supplying arm A paintings

`effect_kit.build_projectile_arms(spec_path, head_path, streak_path, impact_dir,
out_parent, staging, key_states=None)` builds both kits into an empty output
parent. Its explicit optional list accepts zero, one, or two items:

```json
{"state":"stretched", "png":"/absolute/path/to/KS-fire-bolt/stretched.png",
 "hold_frames":3, "pivot":[256,256], "scale":1.0}
```

The conductor supplies the painted paths, pivots, and scales. Holds must be 3
or 4 ticks; scale is positive and at most 1.0. The helper quantises each supplied
painting while retaining its coverage and canvas. Only arm A receives keys;
arm B remains the same two rest primitives. There is no automatic globbing,
name-based grammar selection, or newly invented painting. The complete travel
key replaces both rest primitives while held. The clock cycles rest → key1 →
rest → key2, with each rest held for three ticks. Empty lists produce identical
kit and exported bytes after normalizing only the kit name. No actual travel
key paintings were supplied for this delivery; the runtime key test uses
explicitly synthetic copies of a provided primitive.

## Evidence

- `acceptance.json`: observations, named suite reds, and limitations.
- `e1_rest_trace.json`: actual shipped arms, contact/range/tail/label clock.
- `e1_key_trace.json`: synthetic two-key schedule and the same mechanics.
- `e1_rest_headless.json`, `e1_headless.json`: import and runtime logs.
- `baseline_hashes.json`, `byte_comparison.json`: pre-edit 644-file lock.
- `focused_tests.json`, `suite_tests.json`: 10 targeted and 167 suite tests.
- `run_tests.py`: confined runner; `focused` or `suite` argument. It redirects
  module TMP values and rejects unrelated writes without changing old tests.

Headless import/clock proofs do not establish rendered appearance. Rendered
acceptance belongs to the conductor. Existing tests have named sandbox errors
and an older expansion-time dissolve assertion, retained without modification.
