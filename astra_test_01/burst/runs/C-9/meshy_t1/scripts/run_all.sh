#!/bin/zsh
# C-9 meshy_t1: render every clip in all eight directions.
# Locomotion and idle use --carry (a library clip swings both arms, so a
# hand-socketed weapon swings with them); the attack is text-to-motion authored
# FOR a polearm, so its hands are already posed and it keeps the hand socket.
cd "$(dirname "$0")/.."
B=/opt/homebrew/bin/blender
for c in walk run idle; do
  $B -b -noaudio --python scripts/04_render.py -- $c.glb work/clip_$c.json $c \
     out/$c --height 1.8 --weapon work/socket_pollaxe.json --carry 2>&1 | grep -E "^$c:"
done
$B -b -noaudio --python scripts/04_render.py -- attack.glb work/clip_attack.json attack \
   out/attack --height 1.8 --weapon work/socket_pollaxe.json 2>&1 | grep -E "^attack:"
