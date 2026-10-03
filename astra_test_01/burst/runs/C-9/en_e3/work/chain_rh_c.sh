#!/bin/zsh
# EN-E3 R-C9-135: rift horror (abomination, kc_bounty13) -- bake EN3-RHPG a onto the 2.0 m prep, export (n24), pack en-abomination
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd); K=en-abomination; N=rifthorror; P=builds/rifthorror_prep20.glb
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
H=../../C-7/conductor_scripts/heavy_lock.py
gate() { local g=$(df -k /System/Volumes/Data | tail -1 | awk '{print int($4/1048576)}'); echo "df ${g} GiB"; if [ $g -lt 21 ]; then echo "HALT disk ${g} GiB < 21"; exit 3; fi; }
gate
python3 $H C-9 -- blender -b -noaudio --python scripts/06a_surface.py -- $P work/surface_$N.npz --sheets ${N}_G --size 2048 2>&1 | grep -i "wrote\|error"
python3 scripts/06b_bake.py work/surface_$N.npz work/tex_${N}_G.png --sheet ${N}_G:views/$N/paint/EN3-RHPG_${RH_VAR:-a}.png 2>&1 | tail -1
python3 scripts/n08_blend_tex.py $P work/surface_$N.npz work/tex_${N}_G.png work/tex_${N}_GT.png --all | tail -1
python3 - <<'PY'
import json
c = json.load(open('work/cfg_rifthorror.json')); c['texture'] = 'work/tex_rifthorror_GT.png'
c['texture_status'] = 'PAINTED (D7): sheet EN3-RHPG baked at the game pitch (52.95 deg, 8 views); Tripo projection of the approved sheet where no camera saw the surface'
json.dump(c, open('work/cfg_rifthorror.json', 'w'), indent=1)
PY
mkdir -p export/$N; cp export/${N}_vfx/* export/$N/
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n24_rig_horror.py -- $P work/cfg_$N.json export/$N/$N.glb 2>&1 | grep '^clip\|wrote\|Error'
blender -b -noaudio --python scripts/n17_fit_canvas.py -- export/$N/$N.glb 0.05 2>&1 | grep '^{'
"
python3 scripts/n12_manifest.py export/$N/$N.glb work/cfg_$N.json export/$N/vfx_$N.json export/$N/${N}_clips.json
python3 work/mk_states_$N.py
python3 scripts/n14_join_kit.py "rift horror" $K export/$N/$N.glb export/$N/${N}_clips.json export/$N/vfx_$N.json work/states_$N.json
python3 - $C9/join1_render/kits/$K.json export/$N/${N}_clips.json <<'PY'
import json, sys
k = json.load(open(sys.argv[1])); m = json.load(open(sys.argv[2])); h = m['h_model_m']; W = m['width_m']; L = m['length_m']
k['texture_status'] = 'PAINTED (D7): sheet EN3-RHPG at the game pitch'
k['true_size'] = dict(base_height_m=h, designed_height_m=2.4, reference_record='kc_bounty13.dbr', reference_scale=1.0,
    note='conductor size call (KP-222): max-fit base mesh (n17: every clip clears the 768 canvas with 5% margin at 2.0 m tall); the runtime scales by factor = true/base when the per-kit ppm allows. true = designed height (sheet brief 2.4 m) x scale(record) / scale(reference). base_height_m = the shipped GLB rest crown-to-sole (n12 manifest). The roster gives no mesh box for this rig (Lap F).',
    records={'kc_bounty13 (champion-hero, w153 p02/p04 pinned; w155 p06)': dict(scale=1.0, true_height_m=2.4, factor=round(2.4 / h, 3) if h else None, e_bodies=0.0724, actorRadius_m=0.5, actorHeight_m=2.0),
             'devotion/chthonianmonstrosity_h01 (champion-hero)': dict(scale=1.0, true_height_m=2.4, factor=round(2.4 / h, 3) if h else None, actorRadius_m=0.5, actorHeight_m=2.0)})
k['radii'] = dict(actor_radius_m=0.5, actor_radius_basis='roster actorRadius 0.5 x scale 1.0 (DATAMINED); the pack draws a body wider than this (arms + tentacle crown), the collision radius is the record\'s',
    rest_half_width_m=round(W / 2, 4), rest_half_length_m=round(L / 2, 4), rest_basis='the shipped GLB rest pose bounding box (n12 manifest width_m / length_m), metres at the base size; multiply by factor for true size')
json.dump(k, open(sys.argv[1], 'w'), indent=1)
PY
gate
mkdir -p $C9/join1_pack/$K work/closure_$K
python3 $H C-9 -- zsh -c "J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E '\[j1\]|ERROR|SCRIPT|WATCHDOG' | tail -2"
python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | tail -4
python3 $C9/join1_render/scripts/validate_sockets.py work/raw_$K.json $C9/join1_render/kits/$K.json work/validate_sockets_$K.json 2>&1 | tail -1
echo "resample exact: $(python3 scripts/j_runtime_resample.py export/$N/$N.glb --clips idle,walk,run,attack_swipe,attack_impale,cast_rift,cast_drain,hit,death --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c 'worst 0.000') of 9"
python3 - $C9/join1_render/manifests/${K}_clips.json $N <<'PY'
import json, sys
m=json.load(open(sys.argv[1])); n=sys.argv[2]
a=json.loads(json.dumps(m)); a['attacks']['attack_impale']['release_s']=4.0; json.dump(a,open('work/_neg_release_%s.json'%n,'w'))
b=json.loads(json.dumps(m)); b['clips']['run']['note_neg']='run lasts 0.9 s'
c=json.loads(json.dumps(m)); c['casts']['cast_rift']['release_s']=4.0; json.dump(c,open('work/_neg_release_cast_%s.json'%n,'w')); json.dump(b,open('work/_neg_prose_%s.json'%n,'w'))
PY
{ echo "== the manifest"; python3 scripts/48_manifest_lint.py $C9/join1_render/manifests/${K}_clips.json export/$N/$N.glb; echo "exit $?"; for n in release release_cast prose; do echo "== negative control: neg_$n"; python3 scripts/48_manifest_lint.py work/_neg_${n}_$N.json export/$N/$N.glb; echo "exit $?"; done; } > work/manifest_lint_$K.txt 2>&1; echo $K lint $(grep exit work/manifest_lint_$K.txt | tr '\n' ' ')
python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb sheet film/${N}_stills_8heading.png idle:idle:0,walk:walk:8,impale:attack_impale:45,rift:cast_rift:35,drain:cast_drain:48,death:death:49 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/$N/$N.glb film film/${N}_playspeed.mp4 idle:1:SE,walk:3:SE,run:5:SW,attack_swipe:1:SE,attack_impale:1:S,cast_rift:1:SW,cast_drain:1:SE,hit:1:E,death:1:SE --speeds walk=1.3,run=3.21 2>&1 | grep -i 'error\|film'
"
echo CHAIN_RH_C_DONE
