# T4f-r1 — legacy contact regression repair

## Root cause

T4f conflated target selection with collision eligibility. Its swept query visited only `vfx_targets`, the zero-pierce overlap callback accepted only the resolved target, and `contact_body` rejected every untagged body. The frozen Area2D fixtures intentionally have no target tag, so their callbacks produced neither contact nor impact. The picker consequently could not verify its in-flight kit snapshot. The authored probe then treated a non-impact child as an impact, disrupting its cleanup path and timing out. Legacy StaticBody2D contacts also needed their body callback and swept-body participation restored.

## Runtime change

Only production file changed: `export/godot_import.py`, in its emitted G1 script. `runtime.patch` is relative to the working-tree T4f source supplied to this burst.

- Sweep collision-mask bodies and areas, excluding the projectile, caster, and previously contacted bodies. Enumerate from the same start with accumulated exclusions, then sort by collision fraction and along-path position before dispatch. This covers mixed tagged/untagged lines and multiple contacts in one tick.
- Accept untagged Area2D callbacks and reconnect StaticBody2D callbacks. Extend the shared contact argument to CollisionObject2D. Keep piercing callbacks under swept ordering and retain per-cast de-duplication, classifications, and strike budget.
- Create floating labels only for tagged props. Keep prop-anchored impacts for tagged props and restore projectile-position impacts for legacy collisions. The deep-copied cast kit remains untouched.
- Bound each step by both destination distance and the remaining configured range; terminal range exhaustion uses the existing cleanup branch. No speed, range value, aiming, picker, kit builder, material, or fixture expectation changed.

## Verification

The two unchanged frozen fixtures were run individually against the final runtime (`picker_test.log`, `authored_test.log`). Both Godot probes report zero runtime assertion errors and `T3O_RUNTIME_ASSERTIONS=complete`; neither times out. Both unittest processes return 1 solely because their wrappers reject the sandbox's macOS certificate and editor-settings diagnostics. Outside the sandbox both are expected to complete successfully; that expectation is inferred from the completed runtime checks, not an outside-sandbox execution by this burst.

`test_vfx_picker` plus `test_effect_kit`: 79 tests, 74 successful, five headless wrapper red entries, all with zero runtime assertion errors. `focused_summary.json` preserves the identifiers and runtime reports. The original tests and all expectations are unchanged.

`byte_lock.json`: all 33 files match the frozen aggregate SHA256 `2495fc1bd2f2d8b3dbee84d527a05632ddb35d418964b8fcb28a3686815548bf`, normalizing only the new default `pierce: 0` field out of kit.json.

The re-exported seven-dummy `probe_pierce.gd` exits 0 with no assertion errors. Unlimited and fast sweep: FULL/PARTIAL/PARTIAL; zero pierce: FULL; finite pierce: FULL/PARTIAL; chain callbacks: FULL/FULL/FULL. Every scenario records one strike response. Fifteen labels reuse three nodes; maximum observed lifetime is 0.606793 s. Import and runtime logs retain the sandbox diagnostics.

Supplementary `regression_probe.gd` exercises real mixed Area2D/StaticBody2D/tagged collisions in reverse creation order: body indices 0/1/2, primary/secondary/secondary, one strike, and a label only for the tagged prop. A zero-pierce cast stops on an untagged StaticBody2D. A no-contact cursor cast aimed beyond range remains active for 74 simulated 60-Hz ticks and expires at tick 75, exactly 650 units at 520 units/s. `regression_probe.json` records zero assertion errors. This probe adds coverage without changing the frozen fixtures.

## Full suite

Ran the requested command from the burst root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B tests/run_t0c.py
```

It returned 1 after 217.263 s: 545 tests, 530 successful, 15 non-successful entries. These totals match the supplied T4f README. `full_suite.log` is the complete stdout/stderr capture; `full_suite_summary.json` preserves the totals. The runner exposes totals but no individual unsuccessful-test identifiers in stdout, so this burst does not claim that all 15 entries have been individually reconciled to the five standing reds and sandbox diagnostics. The two affected fixtures and other focused headless probes do explicitly show zero runtime assertion errors in this full run as well.

## Project

`cliffside_t4f_r1.zip` contains 869 resources. The complete T4f export was used as the immutable asset baseline and its G1 resources were re-emitted with the current exporter; only `scripts/vfx_g1.gd` changed in the archive. The other 868 resource bytes, including the existing pierce probe and every kit asset, remain identical. `reexport.json` records the source archive hash and exact resource delta. Zip integrity was checked and its G1 script matches the tested export.

To reproduce, extract the zip to PROJECT, then run:

```sh
/Applications/Godot.app/Contents/MacOS/Godot --headless --path PROJECT --import
/Applications/Godot.app/Contents/MacOS/Godot --headless --path PROJECT --script res://probe_pierce.gd
```

For the supplemental coverage, copy `regression_probe.gd` into PROJECT and invoke it with the same `--script res://regression_probe.gd` option.
