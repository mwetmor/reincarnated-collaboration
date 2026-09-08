#!/bin/zsh
set -e
wizard_project_dir=${0:A:h}
exec /Applications/Godot.app/Contents/MacOS/Godot --path "$wizard_project_dir/godot"
