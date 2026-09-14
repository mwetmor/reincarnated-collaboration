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


Directional VFX kit (--vfx-kit DIR [--sockets PATH])
------------------------------------------------
With this kit, casts fire once at the measured release_index (default 3),
using the displayed frame socket through the sprite transform. Missing
sockets suppress firing with a warning. Facing is screen space; diagonals
are normalized. Bolts move at 520*scale px/s up to 650*scale px, with
StaticBody2D collision and shatter/burst cleanup. impact_range in the
selection JSON is an inclusive [first,last]; absent means all frames.
Ambient emits inside the largest full-cell unblocked floor rectangle,
on an 8 px grid, inset by one cell on every side. Spawn containment
is guaranteed; subsequent particle drift is unconstrained.

## Credits

Synthetic zeta kit.


Directional VFX kit (--vfx-kit DIR [--sockets PATH])
------------------------------------------------
With this kit, casts fire once at the measured release_index (default 3),
using the displayed frame socket through the sprite transform. Missing
sockets suppress firing with a warning. Facing is screen space; diagonals
are normalized. Bolts move at 520*scale px/s up to 650*scale px, with
StaticBody2D collision and shatter/burst cleanup. impact_range in the
selection JSON is an inclusive [first,last]; absent means all frames.
Ambient emits inside the largest full-cell unblocked floor rectangle,
on an 8 px grid, inset by one cell on every side. Spawn containment
is guaranteed; subsequent particle drift is unconstrained.

## Credits

Synthetic alpha kit.

Tab cycles the ordered VFX kits; the HUD shows the selection.
Casts retain their starting kit through release, travel and impact.
