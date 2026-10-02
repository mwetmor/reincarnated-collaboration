#!/bin/zsh
# re-render the maw and crab films/stills after the renderer's fps fix (n05: fps set BEFORE the glTF import)
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/7b4d3123-ce50-4e1f-af04-9f5d427f755a/scratchpad
blender -b -noaudio --python scripts/n05_render.py -- export/maw/maw.glb sheet film/maw_stills_8heading.png idle:idle:0,walk:walk:4,attack:attack_bite:11,death:death:26 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/maw/maw.glb film film/maw_playspeed.mp4 idle:2:SE,walk:4:SE,run:6:SW,attack_bite:1:SE,attack_bite_b:1:S,cast_spit:1:SE,hit:1:E,death:1:SE --speeds walk=1.5,run=3.85 2>&1 | grep -i 'error\|film'
blender -b -noaudio --python scripts/n05_render.py -- export/crab/crab.glb sheet film/crab_stills_8heading.png idle:idle:0,walk:walk:6,attack:attack_slam:12,death:death:20 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/crab/crab.glb film film/crab_playspeed.mp4 idle:2:SE,walk:3:SE,run:6:SW,attack_slam:1:SE,attack_strike:1:S,cast_breath:1:SE,cast_lob:1:SW,hit:1:E,death:1:SE --speeds walk=1.4,run=3.21 2>&1 | grep -i 'error\|film'
