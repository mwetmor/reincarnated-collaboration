#!/bin/zsh
# EN-E3 R-C9-135: the D7 PAINT PASS for the larva + worm (one painted sheet EN3-PZPG a, baked per mesh, then the per-creature grade),
# re-rigged with the n22 emerge fix, rendered as NEW pack roots en-crawlerlarva_p / en-burrowworm_p (the old roots are immutable).
cd /Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/en_e3; C9=$(cd .. && pwd)
export EN3_TMP=/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/60f6998b-1e28-4199-bab2-9be52893d328/scratchpad
H=../../C-7/conductor_scripts/heavy_lock.py
df -h /System/Volumes/Data | tail -1
python3 $H C-9 -- zsh -c "for N in larva worm; do blender -b -noaudio --python scripts/06a_surface.py -- builds/\${N}_prep.glb work/surface_\$N.npz --sheets parasite_G --size 2048 2>&1 | grep -i 'wrote\|error'; done"
for P in larva:en-crawlerlarva:'crawler larva' worm:en-burrowworm:'burrow worm'; do
  N=${P%%:*}; r=${P#*:}; K0=${r%%:*}; K=${K0}_p; NM=${r#*:}
  python3 scripts/06b_bake.py work/surface_$N.npz work/tex_${N}_P.png --sheet parasite_G:views/parasite/paint/EN3-PZPG_a.png 2>&1 | tail -1
  python3 scripts/n08_blend_tex.py builds/${N}_prep.glb work/surface_$N.npz work/tex_${N}_P.png work/tex_${N}_PT.png --all | tail -1
  python3 scripts/n09d_tint.py work/tex_${N}_PT.png work/tex_${N}_PG.png $N
  python3 - $N <<'PY'
import json, sys
n = sys.argv[1]; c = json.load(open('work/cfg_%s.json' % n))
c['texture'] = 'work/tex_%s_PG.png' % n
c['texture_status'] = 'PAINTED (D7): sheet EN3-PZPG a baked at the game pitch (52.95 deg, 8 views), Tripo projection only where no camera saw the surface, then the %s grade (n09d, luminance-preserving: the paint ink/hatching kept)' % n
c['emerge_fix'] = 'n22 2026-10-02: ground-solved clips skip the front-lift floor loop (the emerge f20 head-end curl)'
json.dump(c, open('work/cfg_%s_p.json' % n, 'w'), indent=1)
PY
  mkdir -p export/${N}_p
  python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n22_rig_worm.py -- builds/${N}_prep.glb work/cfg_${N}_p.json export/${N}_p/$N.glb 2>&1 | grep '^clip\|wrote\|Error\|Traceback\|line '
blender -b -noaudio --python scripts/n17_fit_canvas.py -- export/${N}_p/$N.glb 0.05 2>&1 | grep '^{'
"
  python3 scripts/n12_manifest.py export/${N}_p/$N.glb work/cfg_${N}_p.json work/_novfx.json export/${N}_p/${N}_clips.json
  python3 work/mk_states_summon.py $N
  python3 scripts/n14_join_kit.py "$NM" $K export/${N}_p/$N.glb export/${N}_p/${N}_clips.json work/_novfx.json work/states_$N.json
  python3 - $C9/join1_render/kits/$K.json work/cfg_${N}_p.json $N $K0 <<'PY'
import json, sys
k = json.load(open(sys.argv[1])); c = json.load(open(sys.argv[2])); n = sys.argv[3]; k0 = sys.argv[4]
k['texture_status'] = c['texture_status']
k['supersedes'] = dict(pack_root='join1_pack/%s' % k0, kit='kits/%s.json' % k0, why='PROVISIONAL Tripo-projection texture replaced by the D7 paint pass' + (' + the emerge f20 head-end curl fixed (n22)' if n == 'worm' else ''))
k['shared_mesh'] = 'ONE mesh (the parasite sheet EN3-PZ a_r1, one Tripo build) at two scales: en-crawlerlarva_p 0.9 m, en-burrowworm_p 2.8 m; one painted sheet (EN3-PZPG a), two grades'
k['vfx_runtime'] = dict(note='none: the summon arrives with its owner effects (the larva spawns from the owner; the worm from a burrow puff -- reuse the bloom sprout dust)')
if n == 'larva':
    k['true_size'] = dict(base_length_m=0.9, designed_length_m=0.9, note='conductor size call (R-C9-132): built at the record true size (summon r 0.22 m x scale 1.1); factor 1.0 -- no runtime scale needed',
        records={'beetle_maggot01_maggotsummon (summon of sandbeetle01a)': dict(scale=1.1, true_length_m=0.9, factor=1.0)})
else:
    k['true_size'] = dict(base_length_m=2.8, designed_length_m=2.8, note='conductor size call (R-C9-132): built at the record true size (summon r 0.52 m x scale 1.2, all four records one scale); factor 1.0 -- no runtime scale needed',
        records={'aetherialworm_b01/b02/b03/b04_summon (summons of aetherialbloater)': dict(scale=1.2, true_length_m=2.8, factor=1.0)})
json.dump(k, open(sys.argv[1], 'w'), indent=1)
PY
  mkdir -p $C9/join1_pack/$K work/closure_$K
  python3 $H C-9 -- zsh -c "J1_KIT=$C9/join1_render/kits/$K.json J1_OUT=$C9/join1_pack/$K J1_RAW=$PWD/work/raw_$K.json J1_CLOSURE=$PWD/work/closure_$K perl -e 'alarm shift; exec @ARGV' 2700 /Applications/Godot.app/Contents/MacOS/Godot --path $C9/join1_render --resolution 320x180 res://render_cells.tscn 2>&1 | grep -E '\[j1\]|ERROR|SCRIPT|WATCHDOG' | tail -2"
  python3 $C9/join1_render/scripts/index_cells.py $C9/join1_render/kits/$K.json $C9/join1_pack/$K work/raw_$K.json work/closure_$K --sheet $C9/join1_pack/${K}_contact_sheet_1x.png 2>&1 | tail -4
  python3 $C9/join1_render/scripts/validate_sockets.py work/raw_$K.json $C9/join1_render/kits/$K.json work/validate_sockets_$K.json 2>&1 | tail -1
  CL=idle,attack_bite,death,$( [ $N = larva ] && echo crawl || echo emerge )
  echo "resample exact: $(python3 scripts/j_runtime_resample.py export/${N}_p/$N.glb --clips $CL --out work/runtime_resample_$K.json --index $C9/join1_pack/$K/matrix_index.json 2>&1 | grep -c 'worst 0.000') of 4"
  python3 - $C9/join1_render/manifests/${K}_clips.json ${N}_p <<'PY'
import json, sys
m=json.load(open(sys.argv[1])); n=sys.argv[2]
a=json.loads(json.dumps(m)); a['attacks']['attack_bite']['release_s']=4.0; json.dump(a,open('work/_neg_release_%s.json'%n,'w'))
b=json.loads(json.dumps(m)); b['clips']['idle']['note_neg']='idle lasts 0.2 s'; json.dump(b,open('work/_neg_prose_%s.json'%n,'w'))
PY
  { echo "== the manifest"; python3 scripts/48_manifest_lint.py $C9/join1_render/manifests/${K}_clips.json export/${N}_p/$N.glb; echo "exit $?"; for n in release prose; do echo "== negative control: neg_$n"; python3 scripts/48_manifest_lint.py work/_neg_${n}_${N}_p.json export/${N}_p/$N.glb; echo "exit $?"; done; } > work/manifest_lint_$K.txt 2>&1; echo $K lint $(grep exit work/manifest_lint_$K.txt | tr '\n' ' ')
  python3 $H C-9 -- zsh -c "
blender -b -noaudio --python scripts/n05_render.py -- export/${N}_p/$N.glb sheet film/${N}_p_stills_8heading.png 'idle:idle:0,$( [ $N = larva ] && echo crawl:crawl:4 || echo emerge:emerge:20 ),bite:attack_bite:11,death:death:29' 2>&1 | grep -i 'error\|sheet'
blender -b -noaudio --python scripts/n05_render.py -- export/${N}_p/$N.glb film film/${N}_p_playspeed.mp4 '$( [ $N = larva ] && echo idle:1:SE,crawl:6:SW || echo emerge:1:S,idle:1:SE ),attack_bite:1:S,death:1:SE' $( [ $N = larva ] && echo --speeds crawl=3.21 ) 2>&1 | grep -i 'error\|film'
"
done
echo CHAIN_PZ_C_DONE
