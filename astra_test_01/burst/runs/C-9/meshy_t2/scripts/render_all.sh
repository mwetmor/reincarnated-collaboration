#!/bin/sh
# C-9 meshy_t2: all four clips, all eight directions, all four passes.
cd "$(dirname "$0")/.."
for c in idle walk run attack; do
  blender -b -noaudio --python scripts/08_render.py -- work/clips.blend "$c" "out/$c" \
    --passes colour,pos,part,mask 2>&1 | grep -E "^($c):|ground:"
done
echo "RENDER_ALL_DONE"
