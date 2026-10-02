#!/bin/zsh
# EN-E2 clip chain for ONE acolyte (wl_e1's final_k route, no gear): weapon bones -> Mixamo Pro Magic graft (e40b, rest-aligned,
# world space) -> joint lint (fixed native reference: hit) + 63 fixes -> strip Meshy's own clip -> body GLB (texture embedded later).
#   zsh scripts/en07_chain.sh <m|f> <bolt_clip> <area_clip> <death_clip>
set -e
cd "$(dirname "$0")/.."
g=$1; M=mixamo/glb
mkdir -p work/wb_$g
python3 scripts/52_weapon_bones.py --out work/wb_$g builds/en_${g}_rigged.glb --json work/wb_$g.json | tail -1
python3 scripts/e40b_mixamo_graft.py graft work/wb_$g/en_${g}_rigged.glb work/${g}_c0.glb idle=$M/standing_idle.glb+loop+deroot \
  walk=$M/standing_walk_forward.glb+loop+deroot run=$M/standing_run_forward.glb+loop+deroot cast_bolt=$M/$2.glb+deroot \
  cast_area=$M/$3.glb+deroot hit=$M/standing_react_small_from_front.glb+deroot death=$M/$4.glb+deroot --json work/${g}_graft.json | grep -E "^graft|^lint" | cut -c1-60
ALL=idle,walk,run,cast_bolt,cast_area,hit,death
python3 ../nb_join/scripts/j_joint_lint.py work/${g}_c0.glb --clips $ALL --ref hit --retargets none --layers ../wl_e1/work/layers_none.json --json work/${g}_joint_ref.json | grep "^MOVE" | cut -c1-70 || true
cp work/${g}_c0.glb work/${g}_c1.glb
for c in $(python3 -c "import json;d=json.load(open('work/${g}_joint_ref.json'))['moves'];print(' '.join(k for k,v in d.items() if v['verdict']=='FAIL'))"); do
  python3 scripts/63_joint_fix.py work/${g}_c1.glb work/${g}_c1.glb work/${g}_joint_ref.json $c --dev-max 38 --json work/${g}_fix_$c.json | head -1
done
mkdir -p export/$g
python3 - $g <<'PY'
import sys; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre')
g = sys.argv[1]
js, b = L.load_glb('work/%s_c1.glb' % g); js['animations'] = [a for a in js['animations'] if not a['name'].startswith('Armature|')]
R.write_glb('export/%s/en_%s_body.glb' % (g, g), js, bytearray(b)); print('clips', [a['name'] for a in js['animations']])
PY
