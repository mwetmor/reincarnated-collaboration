#!/bin/zsh
# conductor's quick passes: crab leg region grade (texture only) + plant leaf-tip pin (weights); both re-exported, packs re-rendered
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd)
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n11_rig_crab.py -- builds/crab_prep.glb work/cfg_crab.json export/crab/crab.glb 2>&1 | grep 'wrote\|Error'
blender -b -noaudio --python scripts/n16_rig_plant.py -- builds/bloom_prep.glb work/cfg_bloom.json export/bloom/bloom.glb 2>&1 | grep '^clip\|wrote\|Error'
python3 scripts/n12_manifest.py export/crab/crab.glb work/cfg_crab.json export/crab/vfx_crab.json export/crab/crab_clips.json
python3 scripts/n12_manifest.py export/bloom/bloom.glb work/cfg_bloom.json export/bloom/vfx_bloom.json export/bloom/bloom_clips.json
python3 scripts/n14_join_kit.py "ossuary crab" en-ossuarycrab export/crab/crab.glb export/crab/crab_clips.json export/crab/vfx_crab.json work/states_crab.json
python3 scripts/n14_join_kit.py "ossuary bloom" en-ossuarybloom export/bloom/bloom.glb export/bloom/bloom_clips.json export/bloom/vfx_bloom.json work/states_bloom.json
blender -b -noaudio --python scripts/n05_render.py -- export/crab/crab.glb sheet film/crab_stills_8heading.png idle:idle:0,walk:walk:6,attack:attack_slam:12,death:death:20 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/crab/crab.glb film film/crab_playspeed.mp4 idle:2:SE,walk:3:SE,run:6:SW,attack_slam:1:SE,attack_strike:1:S,cast_breath:1:SE,cast_lob:1:SW,hit:1:E,death:1:SE --speeds walk=1.4,run=3.21 2>&1 | grep -i 'error\|film'
blender -b -noaudio --python scripts/n05_render.py -- export/bloom/bloom.glb sheet film/bloom_stills_8heading.png idle:idle:0,attack:attack_bite:12,spit:cast_spit:19,death:death:62,sprout:spawn:30 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/bloom/bloom.glb film film/bloom_playspeed.mp4 spawn:1:S,idle:1:S,attack_bite:1:S,cast_spit:1:SW,hit:1:S,attack_bite:1:SE,death:1:S 2>&1 | grep -i 'error\|film'
blender -b -noaudio --python scripts/n05_render.py -- export/bloom/bloom.glb strip work/strip_bloom_tips.png 'SW|attack_bite:12,attack_bite:13,death:30,death:62,hit:3,cast_spit:19' 2>&1 | grep -i 'error\|sheet'
zsh scripts/n13_godot_chk.sh $PWD/export/crab/crab.glb $PWD/work/godot_crab "idle:0.0" | grep "embedded"
zsh scripts/n13_godot_chk.sh $PWD/export/bloom/bloom.glb $PWD/work/godot_bloom "idle:0.0" | grep "embedded"
for K in en-ossuarycrab en-ossuarybloom; do
  G=export/crab/crab.glb; CL=idle,walk,run,attack_slam,attack_strike,cast_breath,cast_lob,hit,death; [ $K = en-ossuarybloom ] && G=export/bloom/bloom.glb && CL=idle,attack_bite,cast_spit,hit,death,spawn
  rm -rf $C9/join1_pack/$K/cells work/closure_$K; mkdir -p $C9/join1_pack/$K work/closure_$K
  J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
    perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -1
  python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | head -1
  python3 $C9/join1_render/scripts/validate_sockets.py work/raw_$K.json $C9/join1_render/kits/$K.json work/validate_sockets_$K.json 2>&1 | tail -1
  python3 scripts/j_runtime_resample.py $G --clips $CL --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c "worst 0.000"
done
