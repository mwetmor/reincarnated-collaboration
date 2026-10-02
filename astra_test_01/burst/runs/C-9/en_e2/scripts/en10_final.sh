#!/bin/zsh
# EN-E2 FINAL for one acolyte: idle seam closed (58 offset blend on its own keys) -> Meshy's clip stripped -> painted texture EMBEDDED
# (e42) -> scaled to the roster height (e19) -> measures (en09) -> lint (21) -> export/final_<g>/.
#   zsh scripts/en10_final.sh <m|f> <height_m> <tex.png>
set -e
cd "$(dirname "$0")/.."
g=$1; H=$2; TEX=$3
# DEFECT 5 FIX (round 4 handback): the loop window was hard-coded 0:54 (right only for 55-key idles); a longer idle would have been
# TRIMMED silently. The window is now each clip's own full key range, read from the GLB, and the build refuses a clip it cannot see.
# EN_LOOP_CLIPS (default "idle") names the clips to close; "glide" for the wraith.
SPECS=$(python3 - $g ${EN_LOOP_CLIPS:-idle} <<'PY'
import sys; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export')
g, clips = sys.argv[1], sys.argv[2].split(',')
js, b = L.load_glb('work/%s_c1.glb' % g); an = {a['name']: a for a in js['animations']}; out = []
for c in clips:
    assert c in an, 'loop clip %r not in work/%s_c1.glb' % (c, g)
    n = max(js['accessors'][an[c]['samplers'][ch['sampler']]['input']]['count'] for ch in an[c]['channels'])
    out.append('%s=0:%d:8:offset:0,0,1' % (c, n - 1)); print('loop window %s: keys 0..%d (the clip\'s full range)' % (c, n - 1), file=sys.stderr)
print(' '.join(out))
PY
)
python3 scripts/58_loop_blend.py build work/${g}_c1.glb work/${g}_c2.glb ${=SPECS} --json work/${g}_idle_blend.json | grep "build:" | cut -c1-120
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
