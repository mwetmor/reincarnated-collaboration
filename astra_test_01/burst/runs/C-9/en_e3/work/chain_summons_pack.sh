#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd)
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
echo '{"creature": "summon", "effects": []}' > work/_novfx.json
for P in larva:en-crawlerlarva:'crawler larva' worm:en-burrowworm:'burrow worm'; do
  N=${P%%:*}; r=${P#*:}; K=${r%%:*}; NM=${r#*:}
  python3 scripts/n12_manifest.py export/$N/$N.glb work/cfg_$N.json work/_novfx.json export/$N/${N}_clips.json
  python3 work/mk_states_summon.py $N
  python3 scripts/n14_join_kit.py "$NM" $K export/$N/$N.glb export/$N/${N}_clips.json work/_novfx.json work/states_$N.json
  python3 - $C9/join1_render/kits/$K.json work/cfg_$N.json <<'PY'
import json, sys
k = json.load(open(sys.argv[1])); c = json.load(open(sys.argv[2]))
k['texture_status'] = c['texture_status']; k['shared_mesh'] = 'ONE mesh (the parked parasite sheet EN3-PZ a_r1, one Tripo build) at two scales with two grades: en-crawlerlarva 0.9 m, en-burrowworm 2.8 m'
k['vfx_runtime'] = dict(note='none: the summon arrives with its owner effects (the larva spawns from the owner; the worm from a burrow puff -- reuse the bloom sprout dust)')
json.dump(k, open(sys.argv[1], 'w'), indent=1)
PY
  rm -rf $C9/join1_pack/$K/cells; mkdir -p $C9/join1_pack/$K work/closure_$K
  J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
    perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -1
  python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | head -1
  python3 $C9/join1_render/scripts/validate_sockets.py work/raw_$K.json $C9/join1_render/kits/$K.json work/validate_sockets_$K.json 2>&1 | tail -1
  CL=idle,attack_bite,death,$( [ $N = larva ] && echo crawl || echo emerge )
  python3 scripts/j_runtime_resample.py export/$N/$N.glb --clips $CL --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c "worst 0.000"
  python3 - $C9/join1_render/manifests/${K}_clips.json $N <<'PY'
import json, sys
m=json.load(open(sys.argv[1])); n=sys.argv[2]
a=json.loads(json.dumps(m)); a['attacks']['attack_bite']['release_s']=4.0; json.dump(a,open('work/_neg_release_%s.json'%n,'w'))
b=json.loads(json.dumps(m)); b['clips']['idle']['note_neg']='idle lasts 0.2 s'; json.dump(b,open('work/_neg_prose_%s.json'%n,'w'))
PY
  { echo "== the manifest"; python3 scripts/48_manifest_lint.py $C9/join1_render/manifests/${K}_clips.json export/$N/$N.glb; echo "exit $?"; for n in release prose; do echo "== negative control: neg_$n"; python3 scripts/48_manifest_lint.py work/_neg_${n}_$N.json export/$N/$N.glb; echo "exit $?"; done; } > work/manifest_lint_$K.txt 2>&1; echo $K $(grep exit work/manifest_lint_$K.txt | tr '\n' ' ')
  zsh scripts/n13_godot_chk.sh $PWD/export/$N/$N.glb $PWD/work/godot_$N "idle:0.0" | grep "embedded"
  blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb sheet film/${N}_stills_8heading.png "idle:idle:0,$( [ $N = larva ] && echo crawl:crawl:4 || echo emerge:emerge:20 ),bite:attack_bite:11,death:death:29" 2>&1 | grep -i 'error\|sheet'
  blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb film film/${N}_playspeed.mp4 "$( [ $N = larva ] && echo idle:1:SE,crawl:6:SW || echo emerge:1:S,idle:1:SE ),attack_bite:1:S,death:1:SE" $( [ $N = larva ] && echo --speeds crawl=3.21 ) 2>&1 | grep -i 'error\|film'
done
