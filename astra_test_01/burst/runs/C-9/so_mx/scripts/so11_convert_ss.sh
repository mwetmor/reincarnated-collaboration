#!/bin/bash
# so_mx R-C9-134: Mixamo PRO SWORD AND SHIELD PACK FBX -> GLB on her rig's names (e40a). The caller wraps it in heavy_lock.
cd "$(dirname "$0")/.."
B=/Applications/Blender.app/Contents/MacOS/Blender; S="/Users/admin/Games/reincarnated-godot/animations/mixamo/Pro Sword and Shield Pack"
while IFS='|' read -r slug src; do
  [ -z "$slug" ] && continue
  python3 ../gear_sets/scripts/to.py 600 $B -b -noaudio --python scripts/e40a_mixamo_fbx.py -- "$S/$src" mixamo/ss/$slug.glb --json mixamo/ss/$slug.json 2>&1 | grep -E "^MIXAMO|Error|TIMEOUT" | cut -c1-160
done <<'LIST'
idle|sword and shield idle.fbx
idle2|sword and shield idle (2).fbx
idle3|sword and shield idle (3).fbx
idle4|sword and shield idle (4).fbx
walk|sword and shield walk.fbx
walk2|sword and shield walk (2).fbx
run|sword and shield run.fbx
run2|sword and shield run (2).fbx
block|sword and shield block.fbx
block2|sword and shield block (2).fbx
block_idle|sword and shield block idle.fbx
casting|sword and shield casting.fbx
casting2|sword and shield casting (2).fbx
impact|sword and shield impact.fbx
impact2|sword and shield impact (2).fbx
death|sword and shield death.fbx
death2|sword and shield death (2).fbx
LIST
