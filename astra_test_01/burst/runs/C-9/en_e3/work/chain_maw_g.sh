#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd); K=en-cryptmaw
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/maw_prep.glb work/cfg_maw.json export/maw/maw.glb 2>&1 | grep '^clip\|wrote\|Error'
python3 scripts/n12_manifest.py export/maw/maw.glb work/cfg_maw.json export/maw/vfx_maw.json export/maw/maw_clips.json
python3 scripts/n14_join_kit.py "crypt maw" $K export/maw/maw.glb export/maw/maw_clips.json export/maw/vfx_maw.json work/states_maw.json
J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
  perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -14
