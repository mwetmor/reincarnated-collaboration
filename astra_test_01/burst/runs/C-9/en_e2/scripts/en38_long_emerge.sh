#!/bin/zsh
# EN-E2 (conductor, after round 4): the brute's LONG EMERGE, ~4.9 s, so the arena's warp onto the roster emergence window
# (aetherialcorruption_spawn_a01, 148 frames) is ~1:1. A long crouched phase -- crouch idle three times (its own breathing and
# shifting; the joins cross-faded over 4 keys, so each repeat reads as a twitch and re-settle), HUNCHED LOWER by the en31 named edit
# (spine 18, chest 12, neck -14 deg) -- then the same rise (crouch to standing). Built onto the shipped chain (work/b_c1.glb), then
# en10 re-exports (every other clip byte-identical in behaviour: the same chain, the same texture).
set -e
cd "$(dirname "$0")/.."; M=mixamo/glb; T=work/_b_le.glb
python3 scripts/e40b_mixamo_graft.py graft work/b_c1.glb $T crouch_hold=$M/axe_crouch_idle.glb+deroot crouch_up=$M/axe_crouch_to_standing_idle.glb+deroot | grep -E "^lint"
python3 scripts/en31_hunch.py $T $T --spine 18 --chest 12 --neck -14 --clips crouch_hold --json work/b_le_hunch.json | cut -c1-120
python3 scripts/en29_concat.py $T $T em1 crouch_hold@0:1.6667 crouch_hold --blend 4
python3 scripts/en29_concat.py $T $T em2 em1@0:3.3667 crouch_hold@0:0.9 --blend 4
python3 scripts/en29_concat.py $T $T emerge em2@0:4.3 crouch_up --drop em1,em2,crouch_hold,crouch_up --blend 4 --json work/b_emerge_long.json
cp $T work/b_c1.glb
