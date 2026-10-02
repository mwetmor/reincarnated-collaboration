#!/bin/zsh
# EN-E2: the clip manifest against the shipped GLB (wl_e1's 48_manifest_lint, copied in en_e2/scripts), plus two NEGATIVE CONTROLS
# (a copy with one planted error each) that must fail -- the warlord pack's procedure. Writes work/manifest_lint_en-acolyte-<g>.txt.
cd "$(dirname "$0")/.."; g=$1; K=${2:-en-acolyte-$g}; M=../join1_render/manifests/${K}_clips.json; B=export/final_$g/en_${g}_body.glb; O=work/manifest_lint_$K.txt
python3 - $M $g <<'PY'
import json, sys
m = json.load(open(sys.argv[1])); g = sys.argv[2]
a = json.loads(json.dumps(m)); a['casts'][sorted(a['casts'])[0]]['release_s'] = 9.0; json.dump(a, open('work/_neg_release_%s.json' % g, 'w'))
b = json.loads(json.dumps(m)); c = 'run' if 'run' in b['clips'] else 'glide'; b['clips'][c]['note_neg'] = '%s lasts 0.9 s' % c; json.dump(b, open('work/_neg_prose_%s.json' % g, 'w'))   # round 3: the wraith has no run clip
PY
{ echo "== the manifest"; python3 scripts/48_manifest_lint.py $M $B; echo "exit $?"
  for n in release prose; do echo "== negative control: neg_$n (a copy with one planted error)"; python3 scripts/48_manifest_lint.py work/_neg_${n}_$g.json $B; echo "exit $?"; done; } > $O 2>&1
cat $O
