# Keeper cell review stub — Godot 4.6

Open project.godot. Arrows/WASD move; Shift runs; Space jumps; E or left
mouse casts; G switches gear when an advanced set was supplied.
Eight directions rotate the selected cell, never mirror its pixels.
The screen projection and light are baked into the supplied images.
PNG bytes are copied unchanged; offset (-256,-400) anchors the feet pivot.
Linear filtering is enabled. Idle=8, walk/run/jump=12, cast=20 fps;
jump/cast do not loop. Missing directions choose the nearest circular
direction within the state; missing states try idle, then another state.
Each missing request prints once. Ties follow S SW W NW N NE E SE.
Action states return to idle on animation_finished; a loop-only fallback
returns after one fallback cycle. No combat logic or collision geometry.

Optional gear uses a second complete SpriteFrames resource. Optional VFX
accepts numbered cast/travel/impact/frost_bolt PNGs at 20 fps. Casting
spawns an effect at the exported staff_tip_offset relative to the feet.
The default (0,-160) is a configurable stub offset, not a measured socket.
Non-loop effects free on completion; travel-only effects free after 1 s.

Build using python3 -B -m export.godot_import --cells DIR --out EMPTY_DIR
[--gear-variant DIR] [--vfx DIR]. Input cells have contiguous zero-based
animation_DIRECTION_N.png, 512x512 RGBA. Output directories must be empty.
No resampling, external assets, dependencies, or network are required.
The project requests file logging disabled; this did not prevent the bundled
macOS engine's logger startup under the restricted acceptance environment.
Godot editor settings and user-data setup still use the engine's normal OS
locations, which must be writable for a completely clean headless import.
