#!/bin/zsh
# EN-E4 final build for one creature: bake the D7 paint, export the rig, kit + manifest + true_size, JOIN-1 cells, checks, stills8.
#   zsh work/chain_final.sh <name> <TID_paint> <variant> <rig script> <clips csv> <neg cast> <stills spec>
N=$1; TP=$2; VAR=$3; RIG=$4; CLIPS=$5; NEG=$6; STILLS=$7; K=en-$N
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e4; C9=$(cd .. && pwd)
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
echo "== bake"
blender -b -noaudio --python scripts/06a_surface.py -- builds/${N}_prep.glb work/surface_$N.npz --sheets ${N}_G --size 2048 2>&1 | grep -i "wrote\|error"
python3 scripts/06b_bake.py work/surface_$N.npz work/tex_${N}_G.png --sheet ${N}_G:views/$N/paint/${TP}_$VAR.png 2>&1 | tail -1
python3 scripts/n08_blend_tex.py builds/${N}_prep.glb work/surface_$N.npz work/tex_${N}_G.png work/tex_${N}_GT.png --all
echo "== rig export"
mkdir -p export/$N; cp export/${N}_vfx/* export/$N/
blender -b -noaudio --python scripts/$RIG -- builds/${N}_prep.glb work/cfg_$N.json export/$N/$N.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback' | cut -c1-400
blender -b -noaudio --python scripts/n17_fit_canvas.py -- export/$N/$N.glb 0.05 2>&1 | grep '^{'
python3 scripts/n12_manifest.py export/$N/$N.glb work/cfg_$N.json export/$N/vfx_$N.json export/$N/${N}_clips.json
python3 work/mk_states_$N.py
python3 scripts/n14_join_kit.py "$N" $K export/$N/$N.glb export/$N/${N}_clips.json export/$N/vfx_$N.json work/states_$N.json
python3 work/patch_kit_en4.py $N
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb look work/look_${N}_final.png 2>&1 | grep -i 'error\|sheet'
echo "== cells"
rm -rf $C9/join1_pack/$K/cells; mkdir -p $C9/join1_pack/$K work/closure_$K
J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K \
  perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E "\[j1\]|ERROR|SCRIPT|WATCHDOG" | tail -2
echo "== index_cells"
python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | tail -14
echo "== validate_sockets"
python3 $C9/join1_render/scripts/validate_sockets.py work/raw_$K.json $C9/join1_render/kits/$K.json work/validate_sockets_$K.json 2>&1 | tail -2
echo "== runtime_resample worst-0 count"
python3 scripts/j_runtime_resample.py export/$N/$N.glb --clips $CLIPS --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c "worst 0.000"
python3 - $C9/join1_render/manifests/${K}_clips.json $N $NEG <<'PY'
import json, sys
m=json.load(open(sys.argv[1])); n=sys.argv[2]; c=sys.argv[3]
a=json.loads(json.dumps(m)); a['casts'][c]['release_s']=4.0; json.dump(a,open('work/_neg_release_%s.json'%n,'w'))
b=json.loads(json.dumps(m)); b['clips']['run']['note_neg']='run lasts 0.9 s'; json.dump(b,open('work/_neg_prose_%s.json'%n,'w'))
PY
{ echo "== the manifest"; python3 scripts/48_manifest_lint.py $C9/join1_render/manifests/${K}_clips.json export/$N/$N.glb; echo "exit $?"; for n in release prose; do echo "== negative control: neg_$n"; python3 scripts/48_manifest_lint.py work/_neg_${n}_$N.json export/$N/$N.glb; echo "exit $?"; done; } > work/manifest_lint_$K.txt 2>&1
echo "== lint" $(grep exit work/manifest_lint_$K.txt | tr '\n' ' ')
echo "== stills8"
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb sheet film/${N}_stills_8heading.png $STILLS 2>&1 | grep -i 'error\|sheet'
zsh scripts/n13_godot_chk.sh $PWD/export/$N/$N.glb $PWD/work/godot_$N "idle:0.0" | grep "embedded\|bones"
echo "== FINAL DONE $N"
