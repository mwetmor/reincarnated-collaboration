#!/bin/bash
# E1 FINAL K (R-C9-127): Matt approved the Mixamo set. idle = great sword idle (4), the upright one, made a loop by 58_loop_blend
# (window keys 10..111, 'pre' blend over 10 intervals: the seam closes exactly, foot slide <= 3.75 mm); idle_lean = great sword idle
# (kept, unused); walk; run (2) FORWARD; attack = slash (3); warcry = power up; hit = impact; death = two-handed death; the unarmed
# set. Gear from export/k (rig 3); painted + graded texture; bind order (e47); scaled to 1.96 -> export/final_k.
set -e
cd "$(dirname "$0")/.."
export E1_RGRIP=0.64
M=mixamo/glb
python3 scripts/e40b_mixamo_graft.py graft export/wb3/wl_rigged3.glb work/l_c0.glb idle=$M/great_sword_idle_4.glb+deroot \
  idle_lean=$M/great_sword_idle.glb+loop+deroot walk=$M/great_sword_walk.glb+loop+deroot run=$M/great_sword_run_2.glb+loop+deroot \
  attack=$M/great_sword_slash_3.glb warcry=$M/great_sword_power_up.glb+deroot hit=$M/great_sword_impact.glb+deroot \
  death=$M/two_handed_sword_death.glb --json work/l_graft_mx.json | grep -c "graft:"
python3 scripts/55_clip_graft.py graft work/l_c0.glb work/l_c1.glb idle_unarmed=anims/idle11r3.glb+loop+deroot \
  walk_unarmed=anims/free3_walking.glb+loop+deroot run_unarmed=anims/free3_running.glb+loop+deroot --json work/l_graft_unarmed.json | grep -c "graft:"
python3 scripts/58_loop_blend.py build work/l_c1.glb work/l_c1b.glb idle=10:111:10:pre:0,0,1 --json work/l_idle_blend.json | grep "build:"
ALL=idle,idle_lean,walk,run,attack,warcry,hit,death,idle_unarmed,walk_unarmed,run_unarmed
python3 ../nb_join/scripts/j_joint_lint.py work/l_c1b.glb --clips $ALL --ref hit,warcry --retargets none --layers work/layers_none.json --json work/l_joint_ref.json | grep "^MOVE" | grep FAIL | cut -c1-48 || true
cp work/l_c1b.glb work/l_c2.glb
for c in $(python3 -c "import json;d=json.load(open('work/l_joint_ref.json'))['moves'];print(' '.join(k for k,v in d.items() if v['verdict']=='FAIL'))"); do
  python3 scripts/63_joint_fix.py work/l_c2.glb work/l_c2.glb work/l_joint_ref.json $c --dev-max 38 --json work/l_fix_$c.json | head -1
done
E1_RGRIP=0.64 python3 scripts/e12_weapon.py work/l_c2.glb pieces/mace_rh3.glb work/l_c3.glb pieces/mace3.glb --json work/l_weapon.json | grep -E '"ASSERT"'
mkdir -p export/l
python3 - <<'PY'
import sys, shutil; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre'); W = __import__('52_weapon_bones')
W.snap('pieces/mace3.glb')
js, b = L.load_glb('work/l_c3.glb'); js['animations'] = [a for a in js['animations'] if not a['name'].startswith('Armature|')]
R.write_glb('export/l/wl_body.glb', js, bytearray(b)); shutil.copy('pieces/mace3.glb', 'export/l/wl_mace.glb')
for f in ('wl_pauldrons', 'wl_chest', 'wl_cape', 'wl_helm_violet', 'wl_helm_ice'): shutil.copy('export/k/%s.glb' % f, 'export/l/%s.glb' % f)
PY
python3 scripts/e42_embed_tex.py export/l/wl_body.glb export/l/wl_body.glb work/tex_final_graded.png
python3 scripts/e14_piece_mount.py export/l/wl_pauldrons.glb export/l/wl_chest.glb export/l/wl_cape.glb export/l/wl_helm_violet.glb export/l/wl_helm_ice.glb export/l/wl_mace.glb | grep -v "^  52"
rm -rf export/final_k; mkdir -p export/final_k
python3 scripts/e19_height.py 1.96 export/l/wl_body.glb export/l/wl_mace.glb export/l/wl_helm_violet.glb export/l/wl_helm_ice.glb export/l/wl_pauldrons.glb export/l/wl_chest.glb export/l/wl_cape.glb --out export/final_k | cut -c1-70
mv export/final_k/wl_helm_violet.glb export/final_k/wl_helm.glb
python3 scripts/e47_node_order.py export/final_k/wl_body.glb export/final_k/wl_mace.glb export/final_k/wl_helm.glb export/final_k/wl_helm_ice.glb export/final_k/wl_pauldrons.glb export/final_k/wl_chest.glb export/final_k/wl_cape.glb
