#!/bin/zsh
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n05_render.py -- export/gazer/gazer.glb sheet film/gazer_stills_8heading.png idle:idle:0,walk:walk:5,glare:cast_glare:20,attack:attack_tail:16,death:death:36 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/gazer/gazer.glb film film/gazer_playspeed.mp4 idle:1:SE,walk:4:SE,run:6:SW,cast_glare:1:S,cast_breath:1:SE,attack_tail:1:SW,cast_spit:1:SE,hit:1:E,death:1:SE --speeds walk=1.3,run=3.21 2>&1 | grep -i 'error\|film'
