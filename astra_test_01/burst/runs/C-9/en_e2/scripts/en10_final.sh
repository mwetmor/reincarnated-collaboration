#!/bin/zsh
# EN-E2 FINAL for one acolyte: idle seam closed (58 offset blend on its own keys) -> Meshy's clip stripped -> painted texture EMBEDDED
# (e42) -> scaled to the roster height (e19) -> measures (en09) -> lint (21) -> export/final_<g>/.
#   zsh scripts/en10_final.sh <m|f> <height_m> <tex.png>
set -e
cd "$(dirname "$0")/.."
g=$1; H=$2; TEX=$3
python3 scripts/58_loop_blend.py build work/${g}_c1.glb work/${g}_c2.glb idle=0:54:8:offset:0,0,1 ${=EN_LOOP_EXTRA} --json work/${g}_idle_blend.json | grep "build:" | cut -c1-120
mkdir -p export/$g
python3 - $g <<'PY'
import sys; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre')
g = sys.argv[1]
js, b = L.load_glb('work/%s_c2.glb' % g); js['animations'] = [a for a in js['animations'] if not a['name'].startswith('Armature|')]
R.write_glb('export/%s/en_%s_body.glb' % (g, g), js, bytearray(b))
PY
python3 scripts/e42_embed_tex.py export/$g/en_${g}_body.glb export/$g/en_${g}_body.glb $TEX
mkdir -p export/final_$g
python3 scripts/e19_height.py $H export/$g/en_${g}_body.glb --out export/final_$g | cut -c1-90
python3 scripts/en09_measure.py export/final_$g/en_${g}_body.glb work/${g}_graft.json export/final_$g/height.json --json export/final_$g/en_${g}_measure.json | cut -c1-400
python3 scripts/21_lint_export.py export/final_$g/en_${g}_body.glb | grep -E "WARN|FAIL|VERDICT" | cut -c1-140
