#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd); K=en-ossuarycrab
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/06a_surface.py -- builds/crab_prep.glb work/surface_crab.npz --sheets crab_G --size 2048 2>&1 | grep -i "wrote\|error"
python3 scripts/06b_bake.py work/surface_crab.npz work/tex_crab_G.png --sheet crab_G:views/crab/paint/EN3-CRPG_a.png 2>&1 | tail -3
python3 scripts/n08_blend_tex.py builds/crab_prep.glb work/surface_crab.npz work/tex_crab_G.png work/tex_crab_GT.png --all
mkdir -p export/crab; cp export/crab_vfx/* export/crab/
blender -b -noaudio --python scripts/n11_rig_crab.py -- builds/crab_prep.glb work/cfg_crab.json export/crab/crab.glb 2>&1 | grep '^clip\|wrote\|Error'
python3 scripts/n12_manifest.py export/crab/crab.glb work/cfg_crab.json export/crab/vfx_crab.json export/crab/crab_clips.json
python3 work/mk_states_crab.py
python3 scripts/n14_join_kit.py "ossuary crab" $K export/crab/crab.glb export/crab/crab_clips.json export/crab/vfx_crab.json work/states_crab.json
blender -b -noaudio --python scripts/n05_render.py -- export/crab/crab.glb look work/look_crab_final.png 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/crab/crab.glb sheet film/crab_stills_8heading.png idle:idle:0,walk:walk:6,attack:attack_slam:12,death:death:20 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/crab/crab.glb film film/crab_playspeed.mp4 idle:2:SE,walk:3:SE,run:6:SW,attack_slam:1:SE,attack_strike:1:S,cast_breath:1:SE,cast_lob:1:SW,hit:1:E,death:1:SE --speeds walk=1.4,run=3.21 2>&1 | grep -i 'error\|film'
zsh scripts/n13_godot_chk.sh $PWD/export/crab/crab.glb $PWD/work/godot_crab "idle:0.0,walk:0.2,attack_slam:0.4,cast_breath:0.4667,death:0.6667" | grep -v "anim "
mkdir -p $C9/join1_pack/$K work/closure_$K
J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
  perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -3
python3 scripts/j_runtime_resample.py export/crab/crab.glb --clips idle,walk,run,attack_slam,attack_strike,cast_breath,cast_lob,hit,death --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | tail -2
