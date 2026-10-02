#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd); K=en-cinderstalker
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/06a_surface.py -- builds/raptor_prep.glb work/surface_raptor.npz --sheets raptor_G --size 2048 2>&1 | grep -i "wrote\|error"
python3 scripts/06b_bake.py work/surface_raptor.npz work/tex_raptor_G.png --sheet raptor_G:views/raptor/paint/EN3-RPPG_a.png 2>&1 | tail -2
python3 scripts/n08_blend_tex.py builds/raptor_prep.glb work/surface_raptor.npz work/tex_raptor_G.png work/tex_raptor_GT.png --all
mkdir -p export/raptor; cp export/raptor_vfx/* export/raptor/
blender -b -noaudio --python scripts/n15_rig_raptor.py -- builds/raptor_prep.glb work/cfg_raptor.json export/raptor/raptor.glb 2>&1 | grep '^clip\|wrote\|Error'
python3 scripts/n12_manifest.py export/raptor/raptor.glb work/cfg_raptor.json export/raptor/vfx_raptor.json export/raptor/raptor_clips.json
python3 work/mk_states_raptor.py
python3 scripts/n14_join_kit.py "cinder stalker" $K export/raptor/raptor.glb export/raptor/raptor_clips.json export/raptor/vfx_raptor.json work/states_raptor.json
blender -b -noaudio --python scripts/n05_render.py -- export/raptor/raptor.glb look work/look_raptor_final.png 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/raptor/raptor.glb sheet film/raptor_stills_8heading.png idle:idle:0,walk:walk:8,attack:attack_swipe:14,death:death:56 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/raptor/raptor.glb film film/raptor_playspeed.mp4 idle:1:SE,walk:3:SE,run:6:SW,attack_swipe:1:SE,attack_kick:1:S,attack_leap:1:SE,hit:1:E,death:1:SE --speeds walk=1.6,run=3.21 2>&1 | grep -i 'error\|film'
zsh scripts/n13_godot_chk.sh $PWD/export/raptor/raptor.glb $PWD/work/godot_raptor "idle:0.0,walk:0.3,attack_swipe:0.4667,attack_leap:0.6333,death:1.8667" | grep -v "anim "
mkdir -p $C9/join1_pack/$K work/closure_$K
J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
  perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -2
python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | tail -11
python3 scripts/j_runtime_resample.py export/raptor/raptor.glb --clips idle,walk,run,attack_swipe,attack_kick,attack_leap,hit,death --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c "worst 0.000"
