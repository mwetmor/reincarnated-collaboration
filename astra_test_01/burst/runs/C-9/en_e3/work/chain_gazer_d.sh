#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd); K=en-cryptgazer
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/06a_surface.py -- builds/gazer_prep.glb work/surface_gazer.npz --sheets gazer_G --size 2048 2>&1 | grep -i "wrote\|error"
mkdir -p export/gazer; cp export/gazer_vfx/* export/gazer/
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/gazer_prep.glb work/cfg_gazer.json export/gazer/gazer.glb 2>&1 | grep '^clip\|wrote\|Error'
blender -b -noaudio --python scripts/n17_fit_canvas.py -- export/gazer/gazer.glb 0.05 2>&1 | grep '^{'
python3 scripts/n12_manifest.py export/gazer/gazer.glb work/cfg_gazer.json export/gazer/vfx_gazer.json export/gazer/gazer_clips.json
python3 work/mk_states_gazer.py
python3 scripts/n14_join_kit.py "crypt gazer" $K export/gazer/gazer.glb export/gazer/gazer_clips.json export/gazer/vfx_gazer.json work/states_gazer.json
blender -b -noaudio --python scripts/n05_render.py -- export/gazer/gazer.glb look work/look_gazer_final.png 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/gazer/gazer.glb sheet film/gazer_stills_8heading.png idle:idle:0,walk:walk:5,glare:cast_glare:20,attack:attack_tail:16,death:death:36 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/gazer/gazer.glb film film/gazer_playspeed.mp4 idle:1:SE,walk:4:SE,run:6:SW,cast_glare:1:S,cast_breath:1:SE,attack_tail:1:SW,cast_spit:1:SE,hit:1:E,death:1:SE --speeds walk=1.3,run=3.21 2>&1 | grep -i 'error\|film'
zsh scripts/n13_godot_chk.sh $PWD/export/gazer/gazer.glb $PWD/work/godot_gazer "idle:0.0,cast_glare:0.6667,cast_breath:0.5333,attack_tail:0.5333,death:1.2" | grep -v "anim "
rm -rf $C9/join1_pack/$K/cells; mkdir -p $C9/join1_pack/$K work/closure_$K
J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
  perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -1
python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | tail -11
python3 $C9/join1_render/scripts/validate_sockets.py work/raw_$K.json $C9/join1_render/kits/$K.json work/validate_sockets_$K.json 2>&1 | tail -1
python3 scripts/j_runtime_resample.py export/gazer/gazer.glb --clips idle,walk,run,cast_glare,cast_breath,attack_tail,cast_spit,hit,death --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c "worst 0.000"
