#!/bin/zsh
# EN-E2: convert the staged Pro Magic FBX (mixamo/fbx, gitignored) to rig-named GLBs (mixamo/glb) with wl_e1's e40a, one Blender per clip.
cd "$(dirname "$0")/.."
for f in mixamo/fbx/*.fbx; do b=$(basename $f .fbx)
  [ -f mixamo/glb/$b.glb ] && continue
  blender -b -noaudio --python scripts/e40a_mixamo_fbx.py -- $f mixamo/glb/$b.glb --json mixamo/glb/$b.json 2>&1 | grep "^MIXAMO" | cut -c1-200
done
