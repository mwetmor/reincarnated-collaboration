#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd); N=voiddrone
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
mkdir -p export/$N; cp export/${N}_vfx/* export/$N/
for V in "" _boss; do
  K=en-voiddrone$V; G=export/$N/$N$V.glb
  blender -b -noaudio --python scripts/n11_rig_crab.py -- builds/${N}_prep.glb work/cfg_$N$V.json $G 2>&1 | grep '^clip\|wrote\|Error'
  python3 scripts/n12_manifest.py $G work/cfg_$N$V.json export/$N/vfx_$N.json export/$N/$N${V}_clips.json
  python3 work/mk_states_$N.py export/$N/$N$V.rig.json work/states_$N$V.json
  python3 scripts/n14_join_kit.py "void drone$V" $K $G export/$N/$N${V}_clips.json export/$N/vfx_$N.json work/states_$N$V.json
  python3 - $C9/join1_render/kits/$K.json "$V" <<'PY'
import json, sys
k = json.load(open(sys.argv[1])); boss = sys.argv[2] == '_boss'
base = 3.6   # the base mesh's length (m); the roster records' bind-pose depth 8.79 mesh units at scale 1.0 (the boss record's box)
k['true_size'] = dict(base_length_m=base, roster_box_depth_at_scale1=8.79, note='conductor size call: one max-fit base mesh; the runtime scales each record by factor = true/base when the per-kit ppm allows (KC2 side)',
    records={r: dict(scale=s, true_length_m=round(8.79 * s, 2), factor=round(8.79 * s / base, 3)) for r, s in
             (('chthonianservitor_a01 (drone summon)', 0.5), ('chthonianservitor_b01/b02', 0.7), ('chthonianservitor_c01', 0.9), ('hero records h01-h04', 0.95), ('chthonianservitor_lunalvalgoth (boss)', 1.0))})
k['variant'] = 'boss grade (darker violet chitin, gold-warmed seams) on the same mesh and rig' if boss else 'base grade (black-violet chitin)'
json.dump(k, open(sys.argv[1], 'w'), indent=1)
PY
  rm -rf $C9/join1_pack/$K/cells; mkdir -p $C9/join1_pack/$K work/closure_$K
  J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
    perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -1
  python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | head -1
  python3 $C9/join1_render/scripts/validate_sockets.py work/raw_$K.json $C9/join1_render/kits/$K.json work/validate_sockets_$K.json 2>&1 | tail -1
  python3 scripts/j_runtime_resample.py $G --clips idle,walk,run,attack_impale,attack_slash,cast_spit,cast_rear,hit,death --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c "worst 0.000"
  python3 - $C9/join1_render/manifests/${K}_clips.json $N$V <<'PY'
import json, sys
m=json.load(open(sys.argv[1])); n=sys.argv[2]
a=json.loads(json.dumps(m)); a['casts']['cast_spit']['release_s']=4.0; json.dump(a,open('work/_neg_release_%s.json'%n,'w'))
b=json.loads(json.dumps(m)); b['clips']['run']['note_neg']='run lasts 0.9 s'; json.dump(b,open('work/_neg_prose_%s.json'%n,'w'))
PY
  { echo "== the manifest"; python3 scripts/48_manifest_lint.py $C9/join1_render/manifests/${K}_clips.json $G; echo "exit $?"; for n in release prose; do echo "== negative control: neg_$n"; python3 scripts/48_manifest_lint.py work/_neg_${n}_$N$V.json $G; echo "exit $?"; done; } > work/manifest_lint_$K.txt 2>&1; echo $K $(grep exit work/manifest_lint_$K.txt | tr '\n' ' ')
done
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb sheet film/${N}_stills_8heading.png idle:idle:0,walk:walk:6,impale:attack_impale:18,rear:cast_rear:28,death:death:29 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb film film/${N}_playspeed.mp4 idle:1:SE,walk:3:SE,run:6:SW,attack_impale:1:S,attack_slash:1:SE,cast_spit:1:SW,cast_rear:1:S,hit:1:E,death:1:SE --speeds walk=1.6,run=3.37 2>&1 | grep -i 'error\|film'
blender -b -noaudio --python scripts/n05_render.py -- export/$N/${N}_boss.glb look work/look_${N}_boss.png 2>&1 | grep -i 'error\|sheet'
zsh scripts/n13_godot_chk.sh $PWD/export/$N/$N.glb $PWD/work/godot_$N "idle:0.0,attack_impale:0.6,cast_rear:0.9333" | grep "embedded\|bones"
zsh scripts/n13_godot_chk.sh $PWD/export/$N/${N}_boss.glb $PWD/work/godot_${N}_boss "idle:0.0" | grep "embedded\|bones"
