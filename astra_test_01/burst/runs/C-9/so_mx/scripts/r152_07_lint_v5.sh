#!/bin/zsh
# R-C9-152/224 step 5b: the v5 manifest lint against ss152b's body GLB, plus its 3 negative controls (one planted error
# each; each must exit 1). Same three controls as v4's work/manifest_lint_d2-fire-sorc-bm_v4.txt. No Godot, no lock.
C9=/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9; SO=$C9/so_mx; K=d2-fire-sorc-bm
M=$C9/join1_render/manifests/${K}_v5_clips.json; G=$SO/export/ss152b/so-body_ss152.glb; W=$SO/work
python3 - $M $W <<'PY'
import json, sys
m = json.load(open(sys.argv[1])); w = sys.argv[2]
a = json.loads(json.dumps(m)); a['casts']['cast_meteor']['release_s'] = 3.5; json.dump(a, open(w + '/_neg_release_v5.json', 'w'))
b = json.loads(json.dumps(m)); b['clips']['run']['note_neg'] = 'run lasts 0.9 s'; json.dump(b, open(w + '/_neg_prose_v5.json', 'w'))
c = json.loads(json.dumps(m)); c['clips']['cast_meteor']['note_neg'] = 'cast_meteor lasts 2.5 s'; json.dump(c, open(w + '/_neg_spin_v5.json', 'w'))
PY
cd $SO
{ echo "== the manifest"; python3 scripts/48_manifest_lint.py $M $G; echo "exit $?"
  for n in release prose spin; do echo "== negative control: neg_$n (a copy with one planted error)"; python3 scripts/48_manifest_lint.py $W/_neg_${n}_v5.json $G; echo "exit $?"; done
} > $C9/join1_render/work/manifest_lint_${K}_v5.txt 2>&1
cat $C9/join1_render/work/manifest_lint_${K}_v5.txt
