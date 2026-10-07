#!/bin/bash
# BV2F M1': WALK the barrow_v2 ART blockout (sketch A, v1 practice) in v1's engine (v1's controls, camera, rig).
# Double-click on the Mac. WASD/arrows walk, Shift runs. Close the window to quit.
G=/Applications/Godot.app/Contents/MacOS/Godot
P="$(cd "$(dirname "$0")/../../../../barrow_full/godot" && pwd)"
export BV2F_VARIANT=art
exec "$G" --path "$P" --resolution 1600x900 scenes/bv2f_barrow_v2.tscn
