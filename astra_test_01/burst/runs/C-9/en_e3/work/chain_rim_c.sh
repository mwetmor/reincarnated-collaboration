#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd); K=en-rimethorn; N=rimethorn
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/06a_surface.py -- builds/${N}_prep.glb work/surface_$N.npz --sheets ${N}_G --size 2048 2>&1 | grep -i "wrote\|error"
python3 scripts/06b_bake.py work/surface_$N.npz work/tex_${N}_G.png --sheet ${N}_G:views/$N/paint/EN3-RTPG_a.png 2>&1 | tail -1
python3 scripts/n08_blend_tex.py builds/${N}_prep.glb work/surface_$N.npz work/tex_${N}_G.png work/tex_${N}_GT.png --all
mkdir -p export/$N; cp export/${N}_vfx/* export/$N/
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/${N}_prep.glb work/cfg_$N.json export/$N/$N.glb 2>&1 | grep '^clip\|wrote\|Error'
blender -b -noaudio --python scripts/n17_fit_canvas.py -- export/$N/$N.glb 0.05 2>&1 | grep '^{'
python3 scripts/n12_manifest.py export/$N/$N.glb work/cfg_$N.json export/$N/vfx_$N.json export/$N/${N}_clips.json
python3 work/mk_states_$N.py
python3 scripts/n14_join_kit.py "rimethorn brute" $K export/$N/$N.glb export/$N/${N}_clips.json export/$N/vfx_$N.json work/states_$N.json
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb sheet film/${N}_stills_8heading.png idle:idle:0,walk:walk:5,attack:attack_swipe:25,impale:cast_impale:27,death:death:60 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb film film/${N}_playspeed.mp4 idle:1:SE,walk:4:SE,run:6:SW,attack_swipe:1:SE,cast_impale:1:S,cast_shards:1:SE,hit:1:E,death:1:SE --speeds walk=1.6,run=3.72 2>&1 | grep -i 'error\|film'
zsh scripts/n13_godot_chk.sh $PWD/export/$N/$N.glb $PWD/work/godot_$N "idle:0.0,attack_swipe:0.8333,cast_impale:0.9,death:2.0" | grep -v "anim "
rm -rf $C9/join1_pack/$K/cells; mkdir -p $C9/join1_pack/$K work/closure_$K
J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
  perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -1
python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | tail -10
python3 $C9/join1_render/scripts/validate_sockets.py work/raw_$K.json $C9/join1_render/kits/$K.json work/validate_sockets_$K.json 2>&1 | tail -1
python3 scripts/j_runtime_resample.py export/$N/$N.glb --clips idle,walk,run,attack_swipe,cast_impale,cast_shards,hit,death --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c "worst 0.000"
python3 - <<'PY'
import json
m=json.load(open('../join1_render/manifests/en-rimethorn_clips.json'))
a=json.loads(json.dumps(m)); a['casts']['cast_impale']['release_s']=4.0; json.dump(a,open('work/_neg_release_rimethorn.json','w'))
b=json.loads(json.dumps(m)); b['clips']['run']['note_neg']='run lasts 0.9 s'; json.dump(b,open('work/_neg_prose_rimethorn.json','w'))
PY
{ echo "== the manifest"; python3 scripts/48_manifest_lint.py $C9/join1_render/manifests/${K}_clips.json export/$N/$N.glb; echo "exit $?"; for n in release prose; do echo "== negative control: neg_$n"; python3 scripts/48_manifest_lint.py work/_neg_${n}_$N.json export/$N/$N.glb; echo "exit $?"; done; } > work/manifest_lint_$K.txt 2>&1; grep exit work/manifest_lint_$K.txt | tr '\n' ' '
