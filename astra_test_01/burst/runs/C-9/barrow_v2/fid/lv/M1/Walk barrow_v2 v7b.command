#!/bin/bash
# BV2F M1: WALK the barrow_v2 layout v7b greybox in v1's engine (v1's controls, camera, rig; class-tinted greybox).
# Double-click on the Mac. WASD/arrows walk, Shift runs (v1's keys). Close the window to quit.
# (Runs the level from the barrow_full Godot project with the installed Godot 4.6.3 -- no export needed.)
G=/Applications/Godot.app/Contents/MacOS/Godot
P="$(cd "$(dirname "$0")/../../../../barrow_full/godot" && pwd)"
exec "$G" --path "$P" --resolution 1600x900 scenes/bv2f_barrow_v2.tscn
