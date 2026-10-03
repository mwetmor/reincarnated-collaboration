#!/bin/zsh
# MX audition (R-C9-149): Mixamo FBX (reincarnated-godot/animations/mixamo, gitignored, Matt's own account; never copied into collab)
# -> rig-named GLB (en_e2's e40a: Mixamo bones renamed to the Meshy 24-joint rig) in mx_audition/mxglb (gitignored *.glb).
# One Blender per clip, EACH under the heavy lock (short jobs; barrow_v2 lanes have priority, R-C9-147).
#   zsh scripts/mx01_convert.sh "<Pack>/<clip>" ...      -> mxglb/<pack-tag>__<clip_slug>.glb + .json
cd "$(dirname "$0")/.."; MX=~/Games/reincarnated-godot/animations/mixamo; HL="python3 ../../C-7/conductor_scripts/heavy_lock.py C-9 --"
for spec in "$@"; do
  pk=${spec%%/*}; cl=${spec#*/}
  tag=$(echo $pk | sed -e 's/Not So Scary Zombie Pack/nsz/' -e 's/Scary Zombie Pack/sz/' -e 's/Creature NPC Pack/cnpc/' -e 's/Creature Pack/cr/')
  slug=$(echo $cl | tr 'A-Z' 'a-z' | sed -e 's/[()]//g' -e 's/ /_/g')
  out=mxglb/${tag}__${slug}.glb
  [ -f $out ] && continue
  ${=HL} blender -b -noaudio --python ../en_e2/scripts/e40a_mixamo_fbx.py -- "$MX/$pk/$cl.fbx" $out --json mxglb/${tag}__${slug}.json 2>&1 | grep -E "^MIXAMO|Error|heavy_lock: waiting" | cut -c1-160
done
