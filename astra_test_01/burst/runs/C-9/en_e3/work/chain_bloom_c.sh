#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd); K=en-ossuarybloom
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/06a_surface.py -- builds/bloom_prep.glb work/surface_bloom.npz --sheets bloom_G --size 2048 2>&1 | grep -i "wrote\|error"
python3 scripts/06b_bake.py work/surface_bloom.npz work/tex_bloom_G.png --sheet bloom_G:views/bloom/paint/EN3-BLPG_b.png 2>&1 | tail -1
python3 scripts/n08_blend_tex.py builds/bloom_prep.glb work/surface_bloom.npz work/tex_bloom_G.png work/tex_bloom_GT.png --all
mkdir -p export/bloom; cp export/bloom_vfx/* export/bloom/
blender -b -noaudio --python scripts/n16_rig_plant.py -- builds/bloom_prep.glb work/cfg_bloom.json export/bloom/bloom.glb 2>&1 | grep '^clip\|wrote\|Error'
python3 scripts/n12_manifest.py export/bloom/bloom.glb work/cfg_bloom.json export/bloom/vfx_bloom.json export/bloom/bloom_clips.json
python3 work/mk_states_bloom.py
python3 scripts/n14_join_kit.py "ossuary bloom" $K export/bloom/bloom.glb export/bloom/bloom_clips.json export/bloom/vfx_bloom.json work/states_bloom.json
blender -b -noaudio --python scripts/n05_render.py -- export/bloom/bloom.glb sheet film/bloom_stills_8heading.png idle:idle:0,attack:attack_bite:12,spit:cast_spit:19,death:death:62,sprout:spawn:30 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/bloom/bloom.glb film film/bloom_playspeed.mp4 spawn:1:S,idle:1:S,attack_bite:1:S,cast_spit:1:SW,hit:1:S,attack_bite:1:SE,death:1:S 2>&1 | grep -i 'error\|film'
zsh scripts/n13_godot_chk.sh $PWD/export/bloom/bloom.glb $PWD/work/godot_bloom "idle:0.0,spawn:0.5,attack_bite:0.4,cast_spit:0.6333,death:2.0667" | grep -v "anim "
mkdir -p $C9/join1_pack/$K work/closure_$K
J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
  perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -2
python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | tail -9
python3 scripts/j_runtime_resample.py export/bloom/bloom.glb --clips idle,attack_bite,cast_spit,hit,death,spawn --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c "worst 0.000"
