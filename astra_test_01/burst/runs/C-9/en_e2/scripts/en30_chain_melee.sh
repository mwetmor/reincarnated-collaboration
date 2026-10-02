#!/bin/zsh
# EN-E2 round 4: the MELEE bodies' clip chain (brute b, wretch c, imp i): weapon bones -> Mixamo graft (e40b) -> [optional emerge concat
# (en29: crouch idle held, then crouch to standing)] -> [optional named edit (en31: the wretch's hunch)] -> joint lint (ref hit) + fixes.
#   zsh scripts/en30_chain_melee.sh <g> "<graft specs>" [emerge] [hunch_args]
set -e
cd "$(dirname "$0")/.."; g=$1; SPECS=$2; EM=${3:-none}; HUNCH=${4:-}
M=mixamo/glb
mkdir -p work/wb_$g; python3 scripts/52_weapon_bones.py --out work/wb_$g builds/en_${g}_rigged.glb --json work/wb_$g.json | tail -1
python3 scripts/e40b_mixamo_graft.py graft work/wb_$g/en_${g}_rigged.glb work/${g}_c0.glb ${=SPECS} --json work/${g}_graft.json | grep -E "^lint"
if [ $EM = emerge ]; then
  if [ -n "$EN_EMERGE_S" ]; then   # round 5: a LONG emerge sized to the roster's spawn window (crouch idle, a second crouch window, then the rise)
    python3 scripts/en29_concat.py work/${g}_c0.glb work/${g}_c0.glb em1 crouch_hold@0:1.6667 crouch_hold@0:$(python3 -c "print(round($EN_EMERGE_S - 1.6667 - 0.6 - 0.0667, 4))") --blend 4
    python3 scripts/en29_concat.py work/${g}_c0.glb work/${g}_c0.glb emerge em1@0:99 crouch_up --drop em1,crouch_hold,crouch_up --blend 4 --json work/${g}_emerge.json
  else
    python3 scripts/en29_concat.py work/${g}_c0.glb work/${g}_c0.glb emerge crouch_hold@0:1.0 crouch_up --drop crouch_hold,crouch_up --blend 4
  fi
fi
if [ -n "$HUNCH" ]; then python3 scripts/en31_hunch.py work/${g}_c0.glb work/${g}_c0.glb ${=HUNCH} --json work/${g}_hunch.json | cut -c1-160; fi
ALL=$(python3 -c "import sys;sys.path.insert(0,'scripts');L=__import__('21_lint_export');js,_=L.load_glb('work/${g}_c0.glb');print(','.join(a['name'] for a in js['animations'] if not a['name'].startswith('Armature')))")
python3 ../nb_join/scripts/j_joint_lint.py work/${g}_c0.glb --clips $ALL --ref hit --retargets none --layers ../wl_e1/work/layers_none.json --json work/${g}_joint_ref.json | grep "^MOVE" | cut -c1-70 || true
cp work/${g}_c0.glb work/${g}_c1.glb
for c in $(python3 -c "import json;d=json.load(open('work/${g}_joint_ref.json'))['moves'];print(' '.join(k for k,v in d.items() if v['verdict']=='FAIL'))"); do
  python3 scripts/63_joint_fix.py work/${g}_c1.glb work/${g}_c1.glb work/${g}_joint_ref.json $c --dev-max 38 --json work/${g}_fix_$c.json | head -1
done
python3 - $g <<'PY'
import sys, os; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre')
g = sys.argv[1]; js, b = L.load_glb('work/%s_c1.glb' % g); js['animations'] = [a for a in js['animations'] if not a['name'].startswith('Armature|')]
os.makedirs('export/%s' % g, exist_ok=True); R.write_glb('export/%s/en_%s_body.glb' % (g, g), js, bytearray(b)); print('clips', [a['name'] for a in js['animations']])
js.pop('animations'); R.write_glb('work/%s_static.glb' % g, js, bytearray(b))
PY
