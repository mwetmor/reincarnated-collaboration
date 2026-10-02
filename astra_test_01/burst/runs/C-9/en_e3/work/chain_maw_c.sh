#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/06a_surface.py -- builds/maw_prep.glb work/surface_maw.npz --sheets maw_A --size 2048 2>&1 | grep -iv '^info\|INFO' | tail -4
python3 scripts/06b_bake.py work/surface_maw.npz work/tex_maw_A.png --sheet maw_A:views/maw/paint/EN3-MWPA_b.png 2>&1 | tail -4
blender -b -noaudio --python scripts/n10_rig_quad.py -- builds/maw_prep.glb work/cfg_maw.json export/maw/maw.glb 2>&1 | grep '^clip\|wrote\|Error'
blender -b -noaudio --python scripts/n05_render.py -- export/maw/maw.glb sheet film/maw_stills_8heading.png idle:idle:0,walk:walk:4,attack:attack_bite:11,death:death:26 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/maw/maw.glb film film/maw_playspeed.mp4 idle:2:SE,walk:4:SE,run:6:SW,attack_bite:1:SE,attack_bite_b:1:S,cast_spit:1:SE,hit:1:E,death:1:SE --speeds walk=1.5,run=3.85 2>&1 | grep -i 'error\|film'
