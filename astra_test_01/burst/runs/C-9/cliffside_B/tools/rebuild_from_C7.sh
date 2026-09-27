#!/bin/bash
# Reconstruct runs/C-9/cliffside_B from scratch.
#
# cliffside_B is a copy of the H1 cliffside (runs/C-7/cliffside_v45, minus its .godot
# cache) with the A/B style toggle added. The C-7 build is DISK-ONLY -- it has no
# tracked files in git -- and this copy inherits that: what is committed here is only
# what C-9 authored or changed, namely
#
#     project.godot                  (+ style_toggle / quit_game input actions, app name)
#     scenes/cliffside.tscn          (+ style_toggle.gd, + the KnightSprite node)
#     scripts/style_toggle.gd        (the toggle itself)
#     scripts/knight_skin.gd         (the knight as the style-B player skin)
#     frames/knight.tres             (the knight SpriteFrames, per-direction walk fps)
#     frames/knight_fit.json         (scale / pivot / fps, with the measurements)
#     frames/knight_foot_slide.json  (the measured slide; nothing is applied from it)
#     parallax/layers_b/offsets.json (per-style vertical offsets for the B layers)
#     tools/                         (this script and its siblings)
#     parallax/{tiles_b,layers_b}/*.png.import
#
# Everything else -- the H1 plate tiles, the H1 parallax layers, the 49 props and
# their art, the Keeper frames, the vfx library, the B texture set built from the
# CS9-assembly art, and both .godot import caches -- is BINARY AND DISK-ONLY
# (astra_test_01/.gitignore ignores *.png). This script regenerates all of it.
#
#   usage: tools/rebuild_from_C7.sh        # run from inside cliffside_B
set -euo pipefail

HERE=$(cd "$(dirname "$0")/.." && pwd)
RUNS=$(cd "$HERE/../.." && pwd)
SRC="$RUNS/C-7/cliffside_v45"
GODOT=${GODOT:-/Applications/Godot.app/Contents/MacOS/Godot}
HEAVY_LOCK=${HEAVY_LOCK:-$RUNS/C-7/conductor_scripts/heavy_lock.py}

[ -d "$SRC" ] || { echo "source H1 build not found at $SRC" >&2; exit 2; }

# 1. the H1 build, minus its import cache. --ignore-existing so the committed C-9
#    files (project.godot, cliffside.tscn, style_toggle.gd, tools/) are never clobbered.
echo "== 1/3  copy H1 art + scenes from $SRC (never modifies the source)"
rsync -a --ignore-existing --exclude '.godot/' "$SRC"/ "$HERE"/

# 2. the Illuminated ("B") texture set, keyed/split/resized from the painted art
echo "== 2/4  build the B texture set"
python3 "$HERE/tools/build_b_assets.py"

# 3. the knight's 16 cells (208 pngs) + frames/knight.tres. Binary and disk-only like
#    the Keeper's own sprites/, so this regenerates them from the manifest.
echo "== 3/4  build the knight frames"
python3 "$HERE/tools/build_knight_frames.py"

# 4. import (heavy: ~400 MB of texture decode -- always under the shared lock)
echo "== 4/4  headless import"
python3 "$HEAVY_LOCK" C-9 -- "$GODOT" --headless --path "$HERE" --import

echo "== done. verify with:"
echo "   python3 $HEAVY_LOCK C-9 -- $GODOT --headless --path $HERE --script tools/probe_ab.gd"
echo "== foot-slide numbers (measure only; walk_px_s is never changed):"
echo "   python3 $HERE/tools/measure_foot_slide.py"
