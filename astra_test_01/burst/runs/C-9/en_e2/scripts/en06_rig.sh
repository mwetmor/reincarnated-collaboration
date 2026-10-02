#!/bin/zsh
# EN-E2: Meshy rig (model_url data URI, through the R-C9-132 Meshy ledger) for one body; fetches the rigged GLB + free walk/run.
#   zsh scripts/en06_rig.sh <m|f> <height_m>
cd "$(dirname "$0")/.."; g=$1
set -e -o pipefail
# DEFECT FIX (round 3): a failed POST (empty reply -> JSONDecodeError) left the PREVIOUS res_rig_tripo.json in place and this script then
# downloaded THAT rig under the new name (the wraith got the female acolyte's rig). The stale result is now removed first and errors stop the script.
[ -f work/res_rig_tripo.json ] && mv -f work/res_rig_tripo.json work/_res_rig_prev.json
python3 scripts/08_meshy.py rigfile builds/en_${g}_prepped.glb $2 | tail -3
[ -f work/res_rig_tripo.json ] || { echo "RIG FAILED: no result for $g"; exit 1; }
cp work/res_rig_tripo.json work/res_rig_${g}.json
python3 - $g <<'PY'
import json, subprocess, sys
g = sys.argv[1]; d = json.load(open('work/res_rig_%s.json' % g)); r = d['result']
subprocess.run(['curl', '-s', '-L', '-o', 'builds/en_%s_rigged.glb' % g, r['rigged_character_glb_url']], check=True)
for k in ('walking', 'running'):
    subprocess.run(['curl', '-s', '-L', '-o', 'anims/%s_free_%s.glb' % (g, k), r['basic_animations']['%s_glb_url' % k]], check=True)
assert d.get('status') == 'SUCCEEDED', d.get('status')
print('rig', g, d['id'], d.get('status'), d.get('consumed_credits'))
PY
