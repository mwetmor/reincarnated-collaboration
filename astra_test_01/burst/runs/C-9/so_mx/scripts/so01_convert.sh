#!/bin/bash
# so_mx S2 (R-C9-131): Mixamo PRO MAGIC PACK FBX -> GLB on HER rig's names (e40a), one Blender process per file, all inside ONE
# heavy-lock hold (the caller wraps this script in heavy_lock). Output mixamo/glb/<slug>.glb (+ .json). Sources are gitignored.
cd "$(dirname "$0")/.."
B=/Applications/Blender.app/Contents/MacOS/Blender
while IFS='|' read -r slug src; do
  [ -z "$slug" ] && continue
  python3 ../gear_sets/scripts/to.py 600 $B -b -noaudio --python scripts/e40a_mixamo_fbx.py -- "mixamo/fbx/$src" mixamo/glb/$slug.glb --json mixamo/glb/$slug.json 2>&1 | grep -E "^MIXAMO|Error|TIMEOUT" | cut -c1-220
done <<'LIST'
idle|standing idle.fbx
idle02|standing idle 02.fbx
idle03|Standing Idle 03.fbx
idle04|Standing Idle 04.fbx
walk|Standing Walk Forward.fbx
run|Standing Run Forward.fbx
cast1h|standing 1H cast spell 01.fbx
atk1h_01|Standing 1H Magic Attack 01.fbx
atk1h_02|Standing 1H Magic Attack 02.fbx
atk1h_03|Standing 1H Magic Attack 03.fbx
cast2h|Standing 2H Cast Spell 01.fbx
atk2h_01|Standing 2H Magic Attack 01.fbx
atk2h_02|Standing 2H Magic Attack 02.fbx
atk2h_03|Standing 2H Magic Attack 03.fbx
atk2h_04|Standing 2H Magic Attack 04.fbx
atk2h_05|Standing 2H Magic Attack 05.fbx
area2h_01|Standing 2H Magic Area Attack 01.fbx
area2h_02|Standing 2H Magic Area Attack 02.fbx
hit_front|Standing React Small From Front.fbx
death_back|Standing React Death Backward.fbx
death_fwd|Standing React Death Forward.fbx
LIST
