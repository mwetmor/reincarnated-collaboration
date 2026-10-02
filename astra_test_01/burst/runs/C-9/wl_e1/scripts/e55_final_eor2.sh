#!/bin/bash
# E1 FINAL K EOR2 (R-C9-132): final_k with the EXTENDED-ARM Eye of Reckoning spin. One frame of idle@1.0 with named edits (e52:
# elbow opening capped at 166 deg interior so the joint lint keeps >= 2.7 deg of flexion; shoulder aim to az 90 deg, his right side),
# turned rigidly CCW (e48, start 0.200 s / loop 0.300 s), the mace laid through both fists (e12), and the haft slid 0.20 m outward
# through the fists in the two spin clips only (e54) so the pommel clears his chest. Same gear, texture, scale and bind order as final_k.
set -e
cd "$(dirname "$0")/.."
export E1_RGRIP=0.64
python3 scripts/e52_spin_pose.py work/l_c2.glb work/o_dk0.glb --base idle@1.0 --H 1.96 --R 0.895,90,1.27 --L 0.50,90,1.27 --elbow-max 166 --json work/o_dk_pose.json > /dev/null
python3 scripts/e48_spin.py work/o_dk0.glb work/o_dk1.glb --pose spin_pose@0.0 --json work/o_dk_spin.json
python3 scripts/e12_weapon.py work/o_dk1.glb pieces/mace_rh3.glb work/o_dk2.glb pieces/mace3.glb --json work/o_dk_weapon.json | grep -E '"ASSERT"'
python3 scripts/e54_grip_slide.py work/o_dk2.glb work/o_dk3.glb --slide 0.20 --clips eor_spin_start,eor_spin_loop
mkdir -p export/o
python3 - <<'PY'
import sys, shutil; sys.path.insert(0, 'scripts'); L = __import__('21_lint_export'); R = __import__('49_recentre'); W = __import__('52_weapon_bones')
W.snap('pieces/mace3.glb')
js, b = L.load_glb('work/o_dk3.glb'); js['animations'] = [a for a in js['animations'] if not a['name'].startswith('Armature|') and a['name'] != 'spin_pose']
R.write_glb('export/o/wl_body.glb', js, bytearray(b)); shutil.copy('pieces/mace3.glb', 'export/o/wl_mace.glb')
for f in ('wl_pauldrons', 'wl_chest', 'wl_cape', 'wl_helm_violet', 'wl_helm_ice'): shutil.copy('export/l/%s.glb' % f, 'export/o/%s.glb' % f)
PY
python3 scripts/e42_embed_tex.py export/o/wl_body.glb export/o/wl_body.glb work/tex_final_graded.png
python3 scripts/e14_piece_mount.py export/o/wl_pauldrons.glb export/o/wl_chest.glb export/o/wl_cape.glb export/o/wl_helm_violet.glb export/o/wl_helm_ice.glb export/o/wl_mace.glb | grep -v "^  52"
mkdir -p export/final_k_eor2
python3 scripts/e19_height.py 1.96 export/o/wl_body.glb export/o/wl_mace.glb export/o/wl_helm_violet.glb export/o/wl_helm_ice.glb export/o/wl_pauldrons.glb export/o/wl_chest.glb export/o/wl_cape.glb --out export/final_k_eor2 | cut -c1-70
mv export/final_k_eor2/wl_helm_violet.glb export/final_k_eor2/wl_helm.glb
python3 scripts/e47_node_order.py export/final_k_eor2/wl_body.glb export/final_k_eor2/wl_mace.glb export/final_k_eor2/wl_helm.glb export/final_k_eor2/wl_helm_ice.glb export/final_k_eor2/wl_pauldrons.glb export/final_k_eor2/wl_chest.glb export/final_k_eor2/wl_cape.glb
cp export/final_k_eor/eye_sockets.json export/final_k_eor/weapon_mount.json export/final_k_eor2/
