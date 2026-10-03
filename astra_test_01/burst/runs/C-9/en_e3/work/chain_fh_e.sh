#!/bin/zsh
# EN-E3 R-C9-135: frosthorn (woollyrhino, rhino_h02) -- bake EN3-FHPG a onto the 3.1 m culled prep, export, pack en-woollyrhino
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd); K=en-woollyrhino; N=frosthorn; P=builds/frosthorn_prep31_c.glb
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
H=../../C-7/conductor_scripts/heavy_lock.py
gate() { local g=$(df -k /System/Volumes/Data | tail -1 | awk '{print int($4/1048576)}'); echo "df ${g} GiB"; if [ $g -lt 21 ]; then echo "HALT disk ${g} GiB < 21"; exit 3; fi; }
gate
python3 $H C-9 -- blender -b -noaudio --python scripts/06a_surface.py -- $P work/surface_$N.npz --sheets ${N}_G --size 2048 2>&1 | grep -i "wrote\|error"
python3 scripts/06b_bake.py work/surface_$N.npz work/tex_${N}_G.png --sheet ${N}_G:views/$N/paint/EN3-FHPG_a.png 2>&1 | tail -1
python3 scripts/n08_blend_tex.py $P work/surface_$N.npz work/tex_${N}_G.png work/tex_${N}_GT.png --all | tail -1
python3 - <<'PY'
import json
c = json.load(open('work/cfg_frosthorn.json')); c['texture'] = 'work/tex_frosthorn_GT.png'
c['texture_status'] = 'PAINTED (D7): sheet EN3-FHPG a baked at the game pitch (52.95 deg, 8 views); Tripo projection of the approved sheet where no camera saw the surface'
json.dump(c, open('work/cfg_frosthorn.json', 'w'), indent=1)
PY
mkdir -p export/$N; cp export/${N}_vfx/* export/$N/
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n10_rig_quad.py -- $P work/cfg_$N.json export/$N/$N.glb 2>&1 | grep '^clip\|wrote\|Error'
blender -b -noaudio --python scripts/n17_fit_canvas.py -- export/$N/$N.glb 0.05 2>&1 | grep '^{'
"
python3 scripts/n12_manifest.py export/$N/$N.glb work/cfg_$N.json export/$N/vfx_$N.json export/$N/${N}_clips.json
python3 work/mk_states_$N.py
python3 scripts/n14_join_kit.py "frosthorn" $K export/$N/$N.glb export/$N/${N}_clips.json export/$N/vfx_$N.json work/states_$N.json
python3 - $C9/join1_render/kits/$K.json <<'PY'
import json, sys
k = json.load(open(sys.argv[1]))
k['texture_status'] = 'PAINTED (D7): sheet EN3-FHPG a at the game pitch'
k['true_size'] = dict(base_length_m=3.1, designed_length_m=4.0, reference_record='rhino_h02.dbr', reference_scale=1.2,
    note='conductor size call (KP-222): max-fit base mesh (n17: every clip clears the 768 canvas with 5% margin at 3.1 m); the runtime scales by factor = true/base when the per-kit ppm allows. true = designed length (the sheet brief: horn tip to tail, 4.0 m; shoulder hump 2.0 m = the record actorHeight) x scale(record) / scale(reference). The roster mesh box (8.01 x 4.46 mesh units) is not used (Lap F).',
    records={'rhino_h01/rhino_h02/rhino_h03/rhino_h04 (champion-hero; w157 rolls 2)': dict(scale=1.2, true_length_m=4.0, factor=round(4.0 / 3.1, 3), e_bodies=0.329)})
json.dump(k, open(sys.argv[1], 'w'), indent=1)
PY
gate
mkdir -p $C9/join1_pack/$K work/closure_$K
python3 $H C-9 -- zsh -c "J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E '\[j1\]|ERROR|SCRIPT|WATCHDOG' | tail -2"
python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | tail -4
python3 $C9/join1_render/scripts/validate_sockets.py work/raw_$K.json $C9/join1_render/kits/$K.json work/validate_sockets_$K.json 2>&1 | tail -1
echo "resample exact: $(python3 scripts/j_runtime_resample.py export/$N/$N.glb --clips idle,walk,run,attack_gore,attack_butt,attack_charge,cast_roar,hit,death --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c 'worst 0.000') of 9"
python3 - $C9/join1_render/manifests/${K}_clips.json $N <<'PY'
import json, sys
m=json.load(open(sys.argv[1])); n=sys.argv[2]
a=json.loads(json.dumps(m)); a['attacks']['attack_gore']['release_s']=4.0; json.dump(a,open('work/_neg_release_%s.json'%n,'w'))
b=json.loads(json.dumps(m)); b['clips']['run']['note_neg']='run lasts 0.9 s'; json.dump(b,open('work/_neg_prose_%s.json'%n,'w'))
PY
{ echo "== the manifest"; python3 scripts/48_manifest_lint.py $C9/join1_render/manifests/${K}_clips.json export/$N/$N.glb; echo "exit $?"; for n in release prose; do echo "== negative control: neg_$n"; python3 scripts/48_manifest_lint.py work/_neg_${n}_$N.json export/$N/$N.glb; echo "exit $?"; done; } > work/manifest_lint_$K.txt 2>&1; echo $K lint $(grep exit work/manifest_lint_$K.txt | tr '\n' ' ')
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb sheet film/${N}_stills_8heading.png idle:idle:0,walk:walk:6,gore:attack_gore:19,charge:attack_charge:20,roar:cast_roar:18,death:death:60 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb film film/${N}_playspeed.mp4 idle:1:SE,walk:3:SE,run:5:SW,attack_gore:1:SE,attack_butt:1:S,attack_charge:1:SW,cast_roar:1:SE,hit:1:E,death:1:SE --speeds walk=1.5,run=2.57 2>&1 | grep -i 'error\|film'
"
echo CHAIN_FH_E_DONE
