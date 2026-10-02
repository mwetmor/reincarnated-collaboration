#!/bin/zsh
# the larva + worm summons from ONE parked sheet (EN3-PZ a_r1) and ONE Tripo build, two scales and two provisional grades, rig n22
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd)
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
for P in larva:0.9:en-crawlerlarva worm:2.8:en-burrowworm; do
  N=${P%%:*}; r=${P#*:}; L=${r%%:*}; K=${r#*:}
  blender -b -noaudio --python scripts/n04_prep.py -- builds/parasite_tripo.glb builds/${N}_prep.glb $L --minisland 0.0003 --faces 30000 ${PZ_FLIP:-} 2>&1 | grep '^{' | cut -c1-260
  python3 - builds/${N}_prep.glb work/tex_${N}_tripo.png <<'PY'
import io, json, struct, sys
from PIL import Image
b = open(sys.argv[1], 'rb').read(); n = struct.unpack('<I', b[12:16])[0]; js = json.loads(b[20:20 + n]); off = 20 + n + 8
bv = js['bufferViews'][js['images'][0]['bufferView']]
Image.open(io.BytesIO(b[off + bv.get('byteOffset', 0): off + bv.get('byteOffset', 0) + bv['byteLength']])).convert('RGB').save(sys.argv[2])
PY
  python3 scripts/n09d_tint.py work/tex_${N}_tripo.png work/tex_${N}_grade.png $N
  mkdir -p export/$N
  blender -b -noaudio --python scripts/n22_rig_worm.py -- builds/${N}_prep.glb work/cfg_$N.json export/$N/$N.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
  blender -b -noaudio --python scripts/n17_fit_canvas.py -- export/$N/$N.glb 0.05 2>&1 | grep '^{'
  blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb strip work/strip_$N.png "SW|$( [ $N = larva ] && echo 'idle:0,crawl:4,crawl:8,attack_bite:11,death:15,death:29' || echo 'idle:0,emerge:10,emerge:29,attack_bite:11,death:15,death:29')" 2>&1 | grep -i 'error\|sheet'
done
