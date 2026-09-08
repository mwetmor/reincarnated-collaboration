# The Gilded Grimoire — playable wizard prototype

An original purple-and-gold wizard modeled from the two supplied character
references, rigged in Blender, and imported into a standalone Godot courtyard.

## Play

Double-click **Play Wizard.command**, or open **godot/project.godot** in Godot
and press **F6** with `scenes/courtyard.tscn` open (F5 runs the main scene).

- **WASD:** move relative to the camera; the character turns toward movement.
- **Hold Shift:** sprint.
- **Mouse wheel:** zoom.
- **Escape:** exit the game.

Walking speed is 1.2 m/s; sprinting speed is 3.0 m/s. Movement accelerates and
stops smoothly. The capsule collides with the courtyard floor, pillars, and
perimeter walls. Standing, walking, and running switch automatically with a
0.18-second animation blend. Diagonal movement is normalized.

## Assets

- `assets/purple_wizard.blend`: editable model, packed reference images,
  humanoid skeleton, animation actions, and review lighting.
- `godot/assets/purple_wizard.glb`: embedded materials, skin, and all three clips.
- `godot/scenes/courtyard.tscn`: playable scene with the imported model.
- `godot/scripts/wizard_player.gd`: movement, turning, zoom, and animation control.
- `renders/`: Blender review images and captures from the running Godot game.

The model has 35 bones, including separate robe-panel bones and finger bones.
Idle is a three-second breathing loop; Walk is 0.8 seconds; Run is 0.6 seconds.
All clips run in place. Godot moves the collision body; animation does not add
root displacement. The tome is a rigid accessory attached to the pelvis.

This is a playable stylized interpretation of the references. Clothing and hair
use simplified geometry. The face and torso retain reference-image color via UV
projection; other surfaces use solid materials and modeled trim. Robe motion is
authored skeletal motion, with clearance based on the knee trajectory, rather
than a cloth simulation. Facial expressions are not animated.

## Verified

Godot 4.6.3 and Blender 5.2.0 LTS were used locally. The actual Blender MCP 1.9.1
server was called over stdio to build, rig, and export the character. The locally
installed Godot MCP Pro 1.15.1 created/saved the scene, set input bindings, launched
the game, and captured its running animations. `mcp_client.py` verifies the
connected Godot project path before executing commands.

The integration test loads the actual courtyard and imported GLB, injects physical
W/A/S/D/Shift events, advances physics, and checks movement and animation state.
It verified all four directions, floor contact, stopping, Idle/Walk/Run selection,
Shift without direction, normalized diagonal speed, and wall collision. One-second
walk displacement was 1.13 m including acceleration; sprint displacement was
2.525 m. Detailed results are in `logs/movement-verification.json`.

Rendered walk/run captures also verified changing poses in the game. Final runtime
error checks are recorded with those captures in `logs/`. A defect in the installed
MCP add-on's `KEY_W` simulator causes a Godot constant-lookup diagnostic and does not
populate physical keycodes. Visual captures therefore use its `simulate_action`
tool; the independent integration test verifies the actual physical key bindings.

Run the integration test:

```sh
/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --script res://scripts/verify_movement.gd
```

## Modeling tools and rebuild

From this folder, install the pinned MCP dependency into an isolated environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
/Applications/Blender.app/Contents/MacOS/Blender --factory-startup --python scripts/start_blender.py
```

The starter loads the package's bundled Blender add-on for this session and exposes
it on localhost port 9877. It does not save Blender preferences. Telemetry is disabled
by the project MCP client. Run these commands from the parent collaboration repo:

```sh
codex-3d-modeling/.venv/bin/python codex-3d-modeling/scripts/mcp_client.py blender --tool execute_blender_code --code-file codex-3d-modeling/scripts/build_wizard.py
codex-3d-modeling/.venv/bin/python codex-3d-modeling/scripts/mcp_client.py blender --tool execute_blender_code --code-file codex-3d-modeling/scripts/rig_animate.py
```

`build_wizard.py` rebuilds the dedicated Blender scene. Use it only in the wizard
session. `render_review.py` renders three review angles from the saved `.blend`.
`build_courtyard.gd` authors an empty `Courtyard` scene through the Godot MCP editor
script tool; save through `save_scene` afterward.

After a new GLB export, stop the game and reimport `assets/purple_wizard.glb` in
Godot before running it again. An unfocused editor can retain the previous imported
animation. Through `execute_editor_script`, the equivalent is:

```gdscript
EditorInterface.get_resource_filesystem().reimport_files(PackedStringArray(["res://assets/purple_wizard.glb"]))
```

The Godot MCP Pro add-on is copied locally from
`/Users/admin/Games/vendor/godot-mcp-pro-v1/addons/godot_mcp`; its MCP server remains
at that installed vendor location. No changes were made to the existing
`reincarnated-godot` project or global Codex MCP configuration. Tool paths in this
prototype target this Mac workspace.

Per repository rules, generated binaries, reference PNGs, caches, environments,
captures, and the separately installed Godot MCP add-on remain local and ignored
by git. The scripts, scenes, input configuration, and this documentation are the
versioned work products. Rebuilding elsewhere requires the two original PNGs and
the installed Godot MCP Pro add-on in addition to these sources.
