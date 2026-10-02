#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd); K=en-blightsac; N=blightsac
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/06a_surface.py -- builds/${N}_prep.glb work/surface_$N.npz --sheets ${N}_G --size 2048 2>&1 | grep -i "wrote\|error"
python3 scripts/06b_bake.py work/surface_$N.npz work/tex_${N}_G.png --sheet ${N}_G:views/$N/paint/EN3-BSPG_a.png 2>&1 | tail -1
python3 scripts/n08_blend_tex.py builds/${N}_prep.glb work/surface_$N.npz work/tex_${N}_G.png work/tex_${N}_GT.png --all
python3 scripts/n09_region_grade.py builds/${N}_prep.glb work/surface_$N.npz work/tex_${N}_GT.png work/tex_${N}_GT2.png all
mkdir -p export/$N; cp export/${N}_vfx/* export/$N/
blender -b -noaudio --python scripts/n18_rig_float.py -- builds/${N}_prep.glb work/cfg_$N.json export/$N/$N.glb 2>&1 | grep '^clip\|wrote\|Error'
blender -b -noaudio --python scripts/n17_fit_canvas.py -- export/$N/$N.glb 0.05 2>&1 | grep '^{'
python3 scripts/n12_manifest.py export/$N/$N.glb work/cfg_$N.json export/$N/vfx_$N.json export/$N/${N}_clips.json
python3 work/mk_states_$N.py
python3 scripts/n14_join_kit.py "blight sac" $K export/$N/$N.glb export/$N/${N}_clips.json export/$N/vfx_$N.json work/states_$N.json
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb sheet film/${N}_stills_8heading.png idle:idle:0,walk:walk:10,breath:cast_breath:19,aura:cast_aura:43,death:death:55 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb film film/${N}_playspeed.mp4 idle:1:SE,walk:2:SE,run:3:SW,cast_breath:1:S,cast_orb:1:SE,cast_aura:1:SW,hit:1:E,death:1:SE --speeds walk=1.4,run=2.57 2>&1 | grep -i 'error\|film'
zsh scripts/n13_godot_chk.sh $PWD/export/$N/$N.glb $PWD/work/godot_$N "idle:0.0,cast_breath:0.6333,cast_aura:1.5,death:1.8333" | grep -v "anim "
rm -rf $C9/join1_pack/$K/cells; mkdir -p $C9/join1_pack/$K work/closure_$K
J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
  perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -1
python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | tail -10
python3 $C9/join1_render/scripts/validate_sockets.py work/raw_$K.json $C9/join1_render/kits/$K.json work/validate_sockets_$K.json 2>&1 | tail -1
python3 scripts/j_runtime_resample.py export/$N/$N.glb --clips idle,walk,run,cast_breath,cast_orb,cast_aura,hit,death --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c "worst 0.000"
python3 - <<'PY'
import json
m=json.load(open('../join1_render/manifests/en-blightsac_clips.json'))
a=json.loads(json.dumps(m)); a['casts']['cast_breath']['release_s']=4.0; json.dump(a,open('work/_neg_release_blightsac.json','w'))
b=json.loads(json.dumps(m)); b['clips']['run']['note_neg']='run lasts 0.9 s'; json.dump(b,open('work/_neg_prose_blightsac.json','w'))
PY
{ echo "== the manifest"; python3 scripts/48_manifest_lint.py $C9/join1_render/manifests/${K}_clips.json export/$N/$N.glb; echo "exit $?"; for n in release prose; do echo "== negative control: neg_$n"; python3 scripts/48_manifest_lint.py work/_neg_${n}_$N.json export/$N/$N.glb; echo "exit $?"; done; } > work/manifest_lint_$K.txt 2>&1; grep exit work/manifest_lint_$K.txt | tr '\n' ' '
